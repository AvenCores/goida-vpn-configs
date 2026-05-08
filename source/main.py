from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import defaultdict
from datetime import datetime
import concurrent.futures
import urllib.parse
import subprocess
import threading
import zoneinfo
import requests
import urllib3
import base64
import html
import json
import re
import os

# -------------------- КОРЕНЬ РЕПОЗИТОРИЯ --------------------
try:
    GIT_ROOT = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        stderr=subprocess.DEVNULL,
    ).decode().strip()
except Exception:
    GIT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GITHUBMIRROR_DIR = os.path.join(GIT_ROOT, "githubmirror")
README_PATH = os.path.join(GIT_ROOT, "README.md")
SNI_DOMAINS_PATH = os.path.join(os.path.dirname(__file__), "sni_domains.json")
URLS_PATH = os.path.join(os.path.dirname(__file__), "urls.json")
URLS_26_PATH = os.path.join(os.path.dirname(__file__), "26_urls.json")

# -------------------- ЗАГРУЗКА КОНФИГУРАЦИИ --------------------
def _load_json_list(path: str, default: list) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                # Сортируем по ключам-числам для сохранения оригинального порядка
                return [data[k] for k in sorted(data.keys(), key=lambda x: int(x))]
            return data
    except Exception:
        return default

URLS = _load_json_list(URLS_PATH, [])
EXTRA_URLS_FOR_26 = _load_json_list(URLS_26_PATH, [])

# -------------------- ЛОГИРОВАНИЕ --------------------
LOGS_BY_FILE: dict[int, list[str]] = defaultdict(list)
_LOG_LOCK = threading.Lock()
_UPDATED_FILES_LOCK = threading.Lock()

_GITHUBMIRROR_INDEX_RE = re.compile(r"(?:githubmirror/)?(\d+)\.txt")
updated_files: set[int] = set()


def _extract_index(msg: str) -> int:
    """Пытается извлечь номер файла из строки вида '19.txt' или 'githubmirror/12.txt'."""
    m = _GITHUBMIRROR_INDEX_RE.search(msg)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            pass
    return 0


def log(message: str):
    """Добавляет сообщение в общий словарь логов потокобезопасно."""
    idx = _extract_index(message)
    with _LOG_LOCK:
        LOGS_BY_FILE[idx].append(message)


# -------------------- ВРЕМЯ --------------------
zone = zoneinfo.ZoneInfo("Europe/Moscow")
thistime = datetime.now(zone)
offset = thistime.strftime("%H:%M | %d.%m.%Y")

# -------------------- GITHUB API (только для статистики) --------------------
GITHUB_TOKEN = os.environ.get("MY_TOKEN")
REPO_NAME = "AvenCores/goida-vpn-configs"

_repo_stats_client = None
REPO = None

if GITHUB_TOKEN:
    try:
        from github import Github, Auth
        _repo_stats_client = Github(auth=Auth.Token(GITHUB_TOKEN))
        REPO = _repo_stats_client.get_repo(REPO_NAME)
        try:
            remaining, limit = _repo_stats_client.rate_limiting
            if remaining < 100:
                log(f"⚠️ Внимание: осталось {remaining}/{limit} запросов к GitHub API")
            else:
                log(f"ℹ️ Доступно запросов к GitHub API: {remaining}/{limit}")
        except Exception as e:
            log(f"⚠️ Не удалось проверить лимиты GitHub API: {e}")
    except ImportError:
        log("⚠️ PyGithub не установлен — статистика репозитория недоступна")
else:
    log("⚠️ MY_TOKEN не задан — статистика репозитория недоступна")

os.makedirs(GITHUBMIRROR_DIR, exist_ok=True)

EXTRA_URL_TIMEOUT = int(os.environ.get("EXTRA_URL_TIMEOUT", "6"))
EXTRA_URL_MAX_ATTEMPTS = int(os.environ.get("EXTRA_URL_MAX_ATTEMPTS", "2"))

LOCAL_PATHS = [os.path.join(GITHUBMIRROR_DIR, f"{i+1}.txt") for i in range(len(URLS))]
LOCAL_PATHS.append(os.path.join(GITHUBMIRROR_DIR, "26.txt"))

# -------------------- HTTP-СЕССИЯ --------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/143.0.0.0 Safari/537.36"
)

DEFAULT_MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "16"))


def _build_session(max_pool_size: int) -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(
        pool_connections=max_pool_size,
        pool_maxsize=max_pool_size,
        max_retries=Retry(
            total=1,
            backoff_factor=0.2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("HEAD", "GET", "OPTIONS"),
        ),
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": CHROME_UA})
    return session


REQUESTS_SESSION = _build_session(max_pool_size=max(DEFAULT_MAX_WORKERS, len(URLS)))

# -------------------- ПОЛУЧЕНИЕ ДАННЫХ --------------------

def fetch_data(
    url: str,
    timeout: int = 10,
    max_attempts: int = 3,
    session: requests.Session | None = None,
    allow_http_downgrade: bool = True,
) -> str:
    sess = session or REQUESTS_SESSION
    last_exc: Exception = RuntimeError("No attempts made")
    for attempt in range(1, max_attempts + 1):
        try:
            modified_url = url
            verify = True

            if attempt == 2:
                verify = False
            elif attempt == 3:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https" and allow_http_downgrade:
                    modified_url = parsed._replace(scheme="http").geturl()
                verify = False

            response = sess.get(modified_url, timeout=timeout, verify=verify)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < max_attempts:
                continue
    raise last_exc


def _format_fetch_error(exc: Exception) -> str:
    if isinstance(exc, requests.exceptions.ConnectTimeout):
        return "Connect timeout"
    if isinstance(exc, requests.exceptions.ReadTimeout):
        return "Read timeout"
    if isinstance(exc, requests.exceptions.Timeout):
        return "Timeout"
    if isinstance(exc, requests.exceptions.SSLError):
        return "TLS error"
    if isinstance(exc, requests.exceptions.HTTPError):
        try:
            return f"HTTP {exc.response.status_code}"
        except Exception:
            return "HTTP error"
    if isinstance(exc, requests.exceptions.ConnectionError):
        return "Connection error"
    msg = str(exc)
    return msg[:160] + "…" if len(msg) > 160 else msg

# -------------------- ФИЛЬТРАЦИЯ --------------------

PROTOCOL_PREFIXES = (
    "vmess://", "vless://", "trojan://", "ss://", "ssr://",
    "tuic://", "hysteria://", "hysteria2://", "hy2://",
    "socks5://", "socks4://", "wireguard://", "ssh://",
    "snell://", "brook://", "juicity://"
)

INSECURE_PATTERN = re.compile(
    r'(?:[?&;]|3%[Bb])(allowinsecure|allow_insecure|insecure)=(?:1|true|yes)(?:[&;#]|$|(?=\s|$))',
    re.IGNORECASE,
)


def try_decode_base64(data: str) -> str:
    """Проверяет, является ли строка списком в Base64, и декодирует её."""
    if "://" not in data:
        try:
            clean_data = "".join(data.split())
            rem = len(clean_data) % 4
            if rem:
                clean_data += "=" * (4 - rem)
            decoded = base64.b64decode(clean_data).decode("utf-8", errors="ignore")
            if any(prefix in decoded.lower() for prefix in PROTOCOL_PREFIXES):
                return decoded
        except Exception:
            pass
    return data


def filter_insecure_configs(local_path: str, data: str, log_enabled: bool = True) -> tuple[str, int]:
    """Декодирует Base64, разделяет конфиги и фильтрует только валидные и безопасные."""
    data = try_decode_base64(data)
    
    # Гарантируем, что протоколы начинаются с новой строки (если они склеены)
    # Используем все префиксы из PROTOCOL_PREFIXES для разделения
    pattern = "|".join(p.replace("://", "") for p in PROTOCOL_PREFIXES)
    data = re.sub(
        rf"({pattern})://",
        r"\n\1://",
        data,
        flags=re.IGNORECASE
    )
    
    result = []
    insecure_count = 0
    splitted = data.splitlines()
    
    for line in splitted:
        line_stripped = line.strip()
        if not line_stripped.lower().startswith(PROTOCOL_PREFIXES):
            continue
            
        processed = urllib.parse.unquote(html.unescape(line_stripped))
        if not INSECURE_PATTERN.search(processed):
            result.append(line_stripped)
        else:
            insecure_count += 1

    if insecure_count > 0 and log_enabled:
        log(f"ℹ️ Отфильтровано {insecure_count} небезопасных конфигов для {os.path.basename(local_path)}")
    return "\n".join(result), insecure_count

# -------------------- ЛОКАЛЬНЫЕ ФАЙЛЫ --------------------

def save_to_local_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    config_count = len([line for line in content.splitlines() if line.strip()])
    log(f"📁 Данные сохранены локально в {os.path.basename(path)} с {config_count} конфигами")


def extract_source_name(url: str) -> str:
    """Извлекает понятное имя источника из URL."""
    try:
        parts = urllib.parse.urlparse(url).path.split("/")
        if len(parts) > 2:
            return f"{parts[1]}/{parts[2]}"
        return urllib.parse.urlparse(url).netloc
    except Exception:
        return "Источник"


def download_and_save(idx: int) -> tuple[str, int] | None:
    """Скачивает файл, фильтрует и сохраняет локально.
    Возвращает (local_path, file_index) если файл изменился, иначе None."""
    url = URLS[idx]
    local_path = LOCAL_PATHS[idx]
    file_index = idx + 1
    try:
        data = fetch_data(url)
        data, _ = filter_insecure_configs(local_path, data)

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    if f.read() == data:
                        config_count = len([line for line in data.splitlines() if line.strip()])
                        log(f"🔄 Изменений для {file_index}.txt нет ({config_count} конфигов).")
                        return None
            except Exception:
                pass

        save_to_local_file(local_path, data)
        return local_path, file_index

    except Exception as e:
        short_msg = str(e)
        if len(short_msg) > 200:
            short_msg = short_msg[:200] + "…"
        # ИСПРАВЛЕНО: добавлен {file_index}.txt, чтобы лог попал в нужную секцию
        log(f"⚠️ Ошибка при скачивании {file_index}.txt ({url}): {short_msg}")
        return None

# -------------------- 26-й ФАЙЛ --------------------

def create_filtered_configs() -> str:
    """Создаёт 26-й файл: конфиги для SNI/CIDR белых списков."""
    try:
        with open(SNI_DOMAINS_PATH, "r", encoding="utf-8") as f:
            sni_domains = json.load(f)
    except Exception as e:
        log(f"❌ Ошибка загрузки {SNI_DOMAINS_PATH}: {e}")
        return os.path.join(GITHUBMIRROR_DIR, "26.txt")

    # Оптимизация: убираем домены, которые являются подстрокой уже добавленных
    sorted_domains = sorted(sni_domains, key=len)
    optimized_domains: list[str] = []
    for d in sorted_domains:
        if not any(existing in d for existing in optimized_domains):
            optimized_domains.append(d)

    try:
        sni_regex = re.compile(r"(?:" + "|".join(re.escape(d) for d in optimized_domains) + r")")
    except Exception as e:
        log(f"❌ Ошибка компиляции Regex: {e}")
        return os.path.join(GITHUBMIRROR_DIR, "26.txt")

    def _extract_host_port(line: str) -> tuple[str, str] | None:
        if not line:
            return None
        if line.startswith("vmess://"):
            try:
                payload = line[8:]
                rem = len(payload) % 4
                if rem:
                    payload += "=" * (4 - rem)
                decoded = base64.b64decode(payload).decode("utf-8", errors="ignore")
                if decoded.startswith("{"):
                    j = json.loads(decoded)
                    host = j.get("add") or j.get("host") or j.get("ip")
                    port = j.get("port")
                    if host and port:
                        return str(host), str(port)
            except Exception:
                pass
            return None
        m = re.search(r"(?:@|//)([\w\.-]+):(\d{1,5})", line)
        return (m.group(1), m.group(2)) if m else None

    def _process_file_filtering(file_idx: int) -> list[str]:
        local_path = os.path.join(GITHUBMIRROR_DIR, f"{file_idx}.txt")
        if not os.path.exists(local_path):
            return []
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()
            return [
                line.strip()
                for line in content.splitlines()
                if line.strip() and sni_regex.search(line.strip())
            ]
        except Exception:
            return []

    all_configs: list[str] = []

    max_workers = min(16, (os.cpu_count() or 1) + 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in concurrent.futures.as_completed(
            [executor.submit(_process_file_filtering, i) for i in range(1, 26)]
        ):
            all_configs.extend(result.result())

    def _load_extra_configs(url: str) -> tuple[list[str], int]:
        count_removed = 0
        configs: list[str] = []
        try:
            data = fetch_data(
                url,
                timeout=EXTRA_URL_TIMEOUT,
                max_attempts=EXTRA_URL_MAX_ATTEMPTS,
                allow_http_downgrade=False,
            )
            data, count_removed = filter_insecure_configs(
                os.path.join(GITHUBMIRROR_DIR, "26.txt"), data, log_enabled=False
            )
            configs = data.splitlines()
        except Exception as e:
            log(f"⚠️ Ошибка при загрузке 26.txt ({url}): {_format_fetch_error(e)}")
        return configs, count_removed

    total_insecure_filtered_26 = 0
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(4, len(EXTRA_URLS_FOR_26))
    ) as executor:
        for future in concurrent.futures.as_completed(
            [executor.submit(_load_extra_configs, u) for u in EXTRA_URLS_FOR_26]
        ):
            res_configs, res_count = future.result()
            all_configs.extend(res_configs)
            total_insecure_filtered_26 += res_count

    if total_insecure_filtered_26 > 0:
        log(f"ℹ️ Отфильтровано {total_insecure_filtered_26} небезопасных конфигов для 26.txt")

    # Дедупликация
    seen_full: set[str] = set()
    seen_hostport: set[str] = set()
    unique_configs: list[str] = []

    for cfg in all_configs:
        c = cfg.strip()
        if not c or c in seen_full:
            continue
        seen_full.add(c)
        hostport = _extract_host_port(c)
        if hostport:
            key = f"{hostport[0].lower()}:{hostport[1]}"
            if key in seen_hostport:
                continue
            seen_hostport.add(key)
        unique_configs.append(c)

    local_path_26 = os.path.join(GITHUBMIRROR_DIR, "26.txt")
    try:
        with open(local_path_26, "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))
        log(f"📁 Создан файл 26.txt с {len(unique_configs)} конфигами")
    except Exception as e:
        log(f"⚠️ Ошибка при сохранении 26.txt: {e}")

    return local_path_26

# -------------------- СТАТИСТИКА РЕПОЗИТОРИЯ --------------------

def _traffic_counts(traffic) -> tuple[int, int]:
    if traffic is None:
        return 0, 0
    if isinstance(traffic, tuple) and len(traffic) >= 2:
        if isinstance(traffic[0], (int, float)) and isinstance(traffic[1], (int, float)):
            return int(traffic[0]), int(traffic[1])
    if isinstance(traffic, dict):
        if "count" in traffic or "uniques" in traffic:
            return int(traffic.get("count", 0)), int(traffic.get("uniques", 0))
        items = traffic.get("views") or traffic.get("clones") or []
        return _sum_traffic_items(items)
    if hasattr(traffic, "count") and hasattr(traffic, "uniques"):
        return int(getattr(traffic, "count", 0) or 0), int(getattr(traffic, "uniques", 0) or 0)
    for attr in ("views", "clones"):
        if hasattr(traffic, attr):
            return _sum_traffic_items(getattr(traffic, attr) or [])
    if hasattr(traffic, "raw_data"):
        raw = getattr(traffic, "raw_data") or {}
        if isinstance(raw, dict):
            if "count" in raw or "uniques" in raw:
                return int(raw.get("count", 0)), int(raw.get("uniques", 0))
            items = raw.get("views") or raw.get("clones") or []
            return _sum_traffic_items(items)
    if isinstance(traffic, (list, tuple)):
        return _sum_traffic_items(traffic)
    return 0, 0


def _sum_traffic_items(items) -> tuple[int, int]:
    total_count = total_uniques = 0
    for item in items or []:
        if isinstance(item, dict):
            total_count += int(item.get("count", 0) or 0)
            total_uniques += int(item.get("uniques", 0) or 0)
        else:
            total_count += int(getattr(item, "count", 0) or 0)
            total_uniques += int(getattr(item, "uniques", 0) or 0)
    return total_count, total_uniques


def _get_repo_stats() -> dict | None:
    if REPO is None:
        return None
    stats: dict[str, int] = {}
    try:
        views_count, views_uniques = _traffic_counts(REPO.get_views_traffic())
        stats["views_count"] = views_count
        stats["views_uniques"] = views_uniques
    except Exception as e:
        log(f"⚠️ Не удалось получить просмотры: {e}")
        return None
    try:
        clones_count, clones_uniques = _traffic_counts(REPO.get_clones_traffic())
        stats["clones_count"] = clones_count
        stats["clones_uniques"] = clones_uniques
    except Exception as e:
        log(f"⚠️ Не удалось получить клоны: {e}")
        return None
    return stats


def _build_repo_stats_table(stats: dict) -> str:
    def _fmt(v) -> str:
        try:
            return f"{int(v):,}"
        except Exception:
            return str(v)

    header = "| Показатель | Значение |\n|--|--|"
    rows = [
        f"| Просмотры (14Д) | {_fmt(stats['views_count'])} |",
        f"| Клоны (14Д) | {_fmt(stats['clones_count'])} |",
        f"| Уникальные клоны (14Д) | {_fmt(stats['clones_uniques'])} |",
        f"| Уникальные посетители (14Д) | {_fmt(stats['views_uniques'])} |",
    ]
    return header + "\n" + "\n".join(rows)


def _insert_repo_stats_section(content: str, stats_section: str) -> str:
    pattern = r"(\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?\|--\|--\|--\|--\|--\|[\s\S]*?\n)(?=\n## )"
    match = re.search(pattern, content)
    if not match:
        return content.rstrip() + "\n\n" + stats_section + "\n"
    return re.sub(pattern, lambda m: m.group(1) + "\n" + stats_section, content, count=1)

# -------------------- ССЫЛКИ НА СКАЧИВАНИЕ --------------------

def fetch_vc_runtime_link() -> str | None:
    """Получить актуальную ссылку на Visual C++ Runtimes с comss.ru"""
    url = 'https://www.comss.ru/download/page.php?id=6271'
    
    try:
        log("🔍 Получение ссылки на Visual C++ Runtimes...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Ищем ссылку на скачивание через regex (без BeautifulSoup для минимизации зависимостей)
        # Ищем URL в формате https://dl.comss.org/download/Visual-C-Runtimes...
        matches = re.findall(r'https://dl\.comss\.org/download/Visual-C-Runtimes[^\s\'"<>]+', response.text)
        
        if matches:
            download_link = matches[0]
            log(f"✅ Visual C++ Runtimes: {os.path.basename(download_link)}")
            return download_link
        else:
            log("⚠️ Не удалось найти ссылку на Visual C++ Runtimes")
            return None
            
    except Exception as e:
        log(f"❌ Ошибка при получении Visual C++ Runtimes: {e}")
        return None


def select_v2rayng_apk(assets):
    """Выбирает обычный universal APK для v2rayNG, а не F-Droid сборку."""
    standard_apk = next(
        (
            asset
            for asset in assets
            if 'universal.apk' in asset.get('name', '').lower()
            and 'f-droid' not in asset.get('name', '').lower()
            and 'fdroid' not in asset.get('name', '').lower()
        ),
        None,
    )
    if standard_apk:
        return standard_apk

    return next(
        (asset for asset in assets if 'universal.apk' in asset.get('name', '').lower()),
        None,
    )


def fetch_latest_release_links() -> dict[str, str]:
    """Получает свежие ссылки на v2rayNG и Throne с GitHub API."""
    links: dict[str, str] = {}

    try:
        # v2rayNG
        log("🔍 Получение v2rayNG...")
        response = requests.get('https://api.github.com/repos/2dust/v2rayNG/releases/latest', timeout=10)
        if response.status_code == 200:
            releases = response.json()
            apk = select_v2rayng_apk(releases.get('assets', []))
            if apk:
                links['v2rayng-apk'] = apk['browser_download_url']
                log(f"✅ v2rayNG: {os.path.basename(apk['browser_download_url'])}")
        else:
            log(f"⚠️ Ошибка GitHub API для v2rayNG: {response.status_code}")
    except Exception as e:
        log(f"❌ Ошибка при получении v2rayNG: {e}")

    try:
        # Throne
        log("🔍 Получение Throne...")
        response = requests.get('https://api.github.com/repos/throneproj/Throne/releases/latest', timeout=10)
        if response.status_code == 200:
            releases = response.json()
            throne_win10 = next((a for a in releases.get('assets', []) if 'windows64' in a['name'] and 'legacy' not in a['name']), None)
            throne_win7 = next((a for a in releases.get('assets', []) if 'windowslegacy64' in a['name']), None)
            throne_linux = next((a for a in releases.get('assets', []) if 'linux-amd64' in a['name']), None)

            if throne_win10:
                links['throne-win10'] = throne_win10['browser_download_url']
                log(f"✅ Throne Win10/11: {os.path.basename(throne_win10['browser_download_url'])}")
            if throne_win7:
                links['throne-win7'] = throne_win7['browser_download_url']
                log(f"✅ Throne Win7/8/8.1: {os.path.basename(throne_win7['browser_download_url'])}")
            if throne_linux:
                links['throne-linux'] = throne_linux['browser_download_url']
                log(f"✅ Throne Linux: {os.path.basename(throne_linux['browser_download_url'])}")
        else:
            log(f"⚠️ Ошибка GitHub API для Throne: {response.status_code}")
    except Exception as e:
        log(f"❌ Ошибка при получении Throne: {e}")

    return links


def update_readme_download_links(links: dict[str, str], vc_runtime_link: str | None = None):
    """Обновляет ссылки на скачивание v2rayNG, Throne и Visual C++ Runtimes в README.md."""
    if not links and not vc_runtime_link:
        log("⚠️ Нет новых ссылок для обновления в README.md")
        return

    if not os.path.exists(README_PATH):
        log("❌ README.md не найден")
        return

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"⚠️ Ошибка при чтении README.md: {e}")
        return

    original_content = content

    # Обновляем ссылку на v2rayNG APK
    if 'v2rayng-apk' in links:
        # Паттерн для поиска ссылки на v2rayNG APK в формате: [Ссылка](https://github.com/.../v2rayNG_..._universal.apk)
        v2rayng_pattern = r'(\*\*1\.\*\* Скачиваем \*\*«v2rayNG»\*.*?\[Ссылка\]\()https://github\.com/2dust/v2rayNG/releases/download/[^)]+(\))'
        if re.search(v2rayng_pattern, content):
            content = re.sub(v2rayng_pattern, rf'\1{links["v2rayng-apk"]}\2', content)
            log(f"✅ Ссылка на v2rayNG обновлена в README.md")
        else:
            log("⚠️ Не найдена ссылка на v2rayNG в README.md")

    # Обновляем ссылки на Throne
    if 'throne-win10' in links:
        throne_pattern = r'(\[Windows 10/11\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_pattern, content):
            content = re.sub(throne_pattern, rf'\1{links["throne-win10"]}\2', content)
            log(f"✅ Ссылка на Throne Win10/11 обновлена в README.md")

    if 'throne-win7' in links:
        throne_win7_pattern = r'(\[Windows 7/8/8\.1\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_win7_pattern, content):
            content = re.sub(throne_win7_pattern, rf'\1{links["throne-win7"]}\2', content)
            log(f"✅ Ссылка на Throne Win7/8/8.1 обновлена в README.md")

    if 'throne-linux' in links:
        throne_linux_pattern = r'(\[Linux\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_linux_pattern, content):
            content = re.sub(throne_linux_pattern, rf'\1{links["throne-linux"]}\2', content)
            log(f"✅ Ссылка на Throne Linux обновлена в README.md")

    # Обновляем ссылку на Visual C++ Runtimes
    if vc_runtime_link:
        vc_runtime_pattern = r'(\*\*4\.\*\* Скачиваем архив и распаковываем.*?\[Ссылка\]\()https://[^\)]+(\))'
        if re.search(vc_runtime_pattern, content):
            content = re.sub(vc_runtime_pattern, rf'\1{vc_runtime_link}\2', content)
            log(f"✅ Ссылка на Visual C++ Runtimes обновлена в README.md")
        else:
            log("⚠️ Не найдена ссылка на Visual C++ Runtimes в README.md")

    if content != original_content:
        try:
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            log("📝 Ссылки на скачивание в README.md обновлены")
        except Exception as e:
            log(f"⚠️ Ошибка при записи README.md: {e}")
    else:
        log("ℹ️ Ссылки на скачивание не требуют изменений")

# -------------------- README --------------------

def update_readme_table():
    """Обновляет таблицы в README.md локально."""
    if not os.path.exists(README_PATH):
        log("❌ README.md не найден")
        return
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            old_content = f.read()
    except Exception as e:
        log(f"⚠️ Ошибка при чтении README.md: {e}")
        return

    time_part, date_part = offset.split(" | ")

    table_header = "| № | Файл | Источник | Время | Дата |\n|--|--|--|--|--|"
    table_rows: list[str] = []

    all_urls_with_26 = URLS + [""]  # 26-й файл без внешнего URL
    for i, url in enumerate(all_urls_with_26, start=1):
        filename = f"{i}.txt"
        raw_file_url = f"https://github.com/{REPO_NAME}/raw/refs/heads/main/githubmirror/{i}.txt"

        if i <= 25:
            source_name = extract_source_name(url)
            source_column = f"[{source_name}]({url})"
        else:
            source_name = "Обход SNI/CIDR белых списков"
            source_column = f"[{source_name}]({raw_file_url})"

        if i in updated_files:
            update_time, update_date = time_part, date_part
        else:
            pattern = rf"\|\s*{i}\s*\|\s*\[`{filename}`\].*?\|.*?\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
            match = re.search(pattern, old_content)
            if match:
                update_time = match.group(1).strip() or "Никогда"
                update_date = match.group(2).strip() or "Никогда"
            else:
                update_time = update_date = "Никогда"

        table_rows.append(
            f"| {i} | [`{filename}`]({raw_file_url}) | {source_column} | {update_time} | {update_date} |"
        )

    new_table = table_header + "\n" + "\n".join(table_rows)

    table_pattern = r"\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?\|--\|--\|--\|--\|--\|[\s\S]*?(\n\n## |$)"
    new_content = re.sub(table_pattern, new_table + r"\1", old_content)

    repo_stats = _get_repo_stats()
    if repo_stats:
        stats_section = "## 📊 Статистика репозитория\n" + _build_repo_stats_table(repo_stats) + "\n"
        stats_pattern = r"## 📊 Статистика репозитория\s*\n[\s\S]*?(?=\n## |\Z)"
        if re.search(stats_pattern, new_content):
            new_content = re.sub(stats_pattern, stats_section, new_content)
        else:
            new_content = _insert_repo_stats_section(new_content, stats_section)
    else:
        log("⚠️ Статистика репозитория недоступна, раздел не обновлён.")

    if new_content == old_content:
        log("📝 README.md не требует изменений")
        return

    try:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        log("📝 README.md обновлён")
    except Exception as e:
        log(f"⚠️ Ошибка при записи README.md: {e}")

# -------------------- GIT --------------------

def git_commit_and_push(dry_run: bool = False):
    """Добавляет изменённые файлы в индекс, делает коммит и пушит."""
    try:
        subprocess.run(
            ["git", "add",
             os.path.relpath(GITHUBMIRROR_DIR, GIT_ROOT),
             os.path.relpath(README_PATH, GIT_ROOT)],
            check=True,
            cwd=GIT_ROOT,
        )

        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=GIT_ROOT,
        )
        if diff.returncode == 0:
            log("ℹ️ Нет изменений для коммита")
            return

        subprocess.run(
            ["git", "commit", "-m", f"🚀 Автообновление репозитория: {offset}"],
            check=True,
            cwd=GIT_ROOT,
        )
        log("✅ Коммит создан")

        if dry_run:
            log("ℹ️ Dry-run: push пропущен")
            return

        subprocess.run(["git", "push"], check=True, cwd=GIT_ROOT)
        log("✅ Изменения запушены в репозиторий")

    except subprocess.CalledProcessError as e:
        log(f"❌ Ошибка git: {e}")

# -------------------- MAIN --------------------

def main(dry_run: bool = False):
    max_workers_download = min(DEFAULT_MAX_WORKERS, max(1, len(URLS)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_download) as pool:
        futures = [pool.submit(download_and_save, i) for i in range(len(URLS))]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                _, file_index = result
                with _UPDATED_FILES_LOCK:
                    updated_files.add(file_index)

    local_path_26 = create_filtered_configs()
    # Определяем, изменился ли 26-й файл
    if os.path.exists(local_path_26):
        with _UPDATED_FILES_LOCK:
            updated_files.add(26)

    # Обновляем ссылки на скачивание v2rayNG, Throne и Visual C++ Runtimes
    release_links = fetch_latest_release_links()
    vc_runtime_link = fetch_vc_runtime_link()
    update_readme_download_links(release_links, vc_runtime_link)

    update_readme_table()
    git_commit_and_push(dry_run=dry_run)

    # Вывод логов
    ordered_keys = sorted(k for k in LOGS_BY_FILE if k != 0)
    output_lines: list[str] = []
    for k in ordered_keys:
        output_lines.append(f"----- {k}.txt -----")
        output_lines.extend(LOGS_BY_FILE[k])
    if LOGS_BY_FILE.get(0):
        output_lines.append("----- Общие сообщения -----")
        output_lines.extend(LOGS_BY_FILE[0])
    print("\n".join(output_lines))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Скачивание репозитория и коммит в GitHub")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Сохранять файлы локально и делать коммит, но не пушить",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
