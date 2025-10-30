import os
import requests
import urllib.parse
import urllib3
from github import Github, Auth
from github import GithubException
from datetime import datetime
import zoneinfo
import concurrent.futures
import threading
import re
import json
import base64
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -------------------- ЛОГИРОВАНИЕ --------------------
LOGS_BY_FILE: dict[int, list[str]] = defaultdict(list)
_LOG_LOCK = threading.Lock()
_UPDATED_FILES_LOCK = threading.Lock()

_GITHUBMIRROR_INDEX_RE = re.compile(r"githubmirror/(\d+)\.txt")
updated_files = set()

def _extract_index(msg: str) -> int:
    """Пытается извлечь номер файла из строки вида 'githubmirror/12.txt'."""
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

# Получение текущего времени по часовому поясу Европа/Москва
zone = zoneinfo.ZoneInfo("Europe/Moscow")
thistime = datetime.now(zone)
offset = thistime.strftime("%H:%M | %d.%m.%Y")

# Получение GitHub токена из переменных окружения
GITHUB_TOKEN = os.environ.get("MY_TOKEN")
REPO_NAME = "AvenCores/goida-vpn-configs"

if GITHUB_TOKEN:
    g = Github(auth=Auth.Token(GITHUB_TOKEN))
else:
    g = Github()

REPO = g.get_repo(REPO_NAME)

# Проверка лимитов GitHub API
try:
    remaining, limit = g.rate_limiting
    if remaining < 100:
        log(f"⚠️ Внимание: осталось {remaining}/{limit} запросов к GitHub API")
    else:
        log(f"ℹ️ Доступно запросов к GitHub API: {remaining}/{limit}")
except Exception as e:
    log(f"⚠️ Не удалось проверить лимиты GitHub API: {e}")

if not os.path.exists("githubmirror"):
    os.mkdir("githubmirror")

URLS = [
    "https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt", #1
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt", #2
    "https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt", #3
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt", #4
    "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/config.txt", #5
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt", #6
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt", #7
    "https://raw.githubusercontent.com/YasserDivaR/pr0xy/refs/heads/main/ShadowSocks2021.txt", #8
    "https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt", #9
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/vless", #10
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt", #11
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all", #12
    "https://github.com/Kwinshadow/TelegramV2rayCollector/raw/refs/heads/main/sublinks/mix.txt", #13
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes", #14
    "https://raw.githubusercontent.com/miladtahanian/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt", #15
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub", #16
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt", #17
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt", #18
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix", #19
    "https://github.com/Argh94/Proxy-List/raw/refs/heads/main/All_Config.txt", #20
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt", #21
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri", #22
    "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet.txt", #23
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS#STR.BYPASS%F0%9F%91%BE", #24
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt", #25
]

REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]

# Добавляем 26-й файл в пути
REMOTE_PATHS.append("githubmirror/26.txt")
LOCAL_PATHS.append("githubmirror/26.txt")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
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

REQUESTS_SESSION = _build_session(max_pool_size=max(DEFAULT_MAX_WORKERS, len(URLS))) if 'URLS' in globals() else _build_session(DEFAULT_MAX_WORKERS)

def fetch_data(url: str, timeout: int = 10, max_attempts: int = 3, session: requests.Session | None = None) -> str:
    sess = session or REQUESTS_SESSION
    for attempt in range(1, max_attempts + 1):
        try:
            modified_url = url
            verify = True

            if attempt == 2:
                verify = False
            elif attempt == 3:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https":
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

def save_to_local_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    log(f"📁 Данные сохранены локально в {path}")

def extract_source_name(url: str) -> str:
    """Извлекает понятное имя источника из URL"""
    try:
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.split('/')
        if len(path_parts) > 2:
            return f"{path_parts[1]}/{path_parts[2]}"
        return parsed.netloc
    except:
        return "Источник"

def update_readme_table():
    """Обновляет таблицу в README.md с информацией о времени последнего обновления"""
    try:
        # Получаем текущий README.md
        try:
            readme_file = REPO.get_contents("README.md")
            old_content = readme_file.decoded_content.decode("utf-8")
        except GithubException as e:
            if e.status == 404:
                log("❌ README.md не найден в репозитории")
                return
            else:
                log(f"⚠️ Ошибка при получении README.md: {e}")
                return

        # Разделяем время и дату
        time_part, date_part = offset.split(" | ")
        
        # Создаем новую таблицу
        table_header = "| № | Файл | Источник | Время | Дата |\n|--|--|--|--|--|"
        table_rows = []
        
        for i, (remote_path, url) in enumerate(zip(REMOTE_PATHS, URLS + [""]), 1):
            filename = f"{i}.txt"
            
            # Формируем ссылку на raw-файл в репозитории
            raw_file_url = f"https://github.com/{REPO_NAME}/raw/refs/heads/main/githubmirror/{i}.txt"
            
            if i <= 25:
                source_name = extract_source_name(url)
                source_column = f"[{source_name}]({url})"
            else:
                # Для 26-го файла создаем ссылку на сам файл с текстом "Обход SNI белых списков"
                source_name = "Обход SNI белых списков"
                source_column = f"[{source_name}]({raw_file_url})"
            
            # Проверяем, был ли файл обновлен в этом запуске
            if i in updated_files:
                update_time = time_part
                update_date = date_part
            else:
                # Пытаемся найти время и дату из старой таблицы
                pattern = rf"\|\s*{i}\s*\|\s*\[`{filename}`\].*?\|.*?\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
                match = re.search(pattern, old_content)
                if match:
                    update_time = match.group(1).strip() if match.group(1).strip() else "Никогда"
                    update_date = match.group(2).strip() if match.group(2).strip() else "Никогда"
                else:
                    update_time = "Никогда"
                    update_date = "Никогда"
            
            # Для всех файлов делаем ссылку на raw-файл в столбце "Файл"
            table_rows.append(f"| {i} | [`{filename}`]({raw_file_url}) | {source_column} | {update_time} | {update_date} |")

        new_table = table_header + "\n" + "\n".join(table_rows)

        # Заменяем таблицу в README.md
        table_pattern = r"\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?\|--\|--\|--\|--\|--\|[\s\S]*?(\n\n## |$)"
        new_content = re.sub(table_pattern, new_table + r"\1", old_content)

        if new_content != old_content:
            REPO.update_file(
                path="README.md",
                message="📝 Обновление таблицы в README.md",
                content=new_content,
                sha=readme_file.sha
            )
            log("📝 Таблица в README.md обновлена")
        else:
            log("📝 Таблица в README.md не требует изменений")

    except Exception as e:
        log(f"⚠️ Ошибка при обновлении README.md: {e}")

def upload_to_github(local_path, remote_path):
    if not os.path.exists(local_path):
        log(f"❌ Файл {local_path} не найден.")
        return

    repo = REPO

    with open(local_path, "r", encoding="utf-8") as file:
        content = file.read()

    max_retries = 5
    import time

    for attempt in range(1, max_retries + 1):
        try:
            try:
                file_in_repo = repo.get_contents(remote_path)
                current_sha = file_in_repo.sha
            except GithubException as e_get:
                if getattr(e_get, "status", None) == 404:
                    basename = os.path.basename(remote_path)
                    repo.create_file(
                        path=remote_path,
                        message=f"🆕 Первый коммит {basename} по часовому поясу Европа/Москва: {offset}",
                        content=content,
                    )
                    log(f"🆕 Файл {remote_path} создан.")
                    # Добавляем в обновленные файлы
                    file_index = int(remote_path.split('/')[1].split('.')[0])
                    with _UPDATED_FILES_LOCK:
                        updated_files.add(file_index)
                    return
                else:
                    msg = e_get.data.get("message", str(e_get))
                    log(f"⚠️ Ошибка при получении {remote_path}: {msg}")
                    return

            try:
                remote_content = file_in_repo.decoded_content.decode("utf-8", errors="replace")
                if remote_content == content:
                    log(f"🔄 Изменений для {remote_path} нет.")
                    return
            except Exception:
                pass

            basename = os.path.basename(remote_path)
            try:
                repo.update_file(
                    path=remote_path,
                    message=f"🚀 Обновление {basename} по часовому поясу Европа/Москва: {offset}",
                    content=content,
                    sha=current_sha,
                )
                log(f"🚀 Файл {remote_path} обновлён в репозитории.")
                # Добавляем в обновленные файлы
                file_index = int(remote_path.split('/')[1].split('.')[0])
                with _UPDATED_FILES_LOCK:
                    updated_files.add(file_index)
                return
            except GithubException as e_upd:
                if getattr(e_upd, "status", None) == 409:
                    if attempt < max_retries:
                        wait_time = 0.5 * (2 ** (attempt - 1))
                        log(f"⚠️ Конфликт SHA для {remote_path}, попытка {attempt}/{max_retries}, ждем {wait_time} сек")
                        time.sleep(wait_time)
                        continue
                    else:
                        log(f"❌ Не удалось обновить {remote_path} после {max_retries} попыток")
                        return
                else:
                    msg = e_upd.data.get("message", str(e_upd))
                    log(f"⚠️ Ошибка при загрузке {remote_path}: {msg}")
                    return

        except Exception as e_general:
            short_msg = str(e_general)
            if len(short_msg) > 200:
                short_msg = short_msg[:200] + "…"
            log(f"⚠️ Непредвиденная ошибка при обновлении {remote_path}: {short_msg}")
            return

    log(f"❌ Не удалось обновлить {remote_path} после {max_retries} попыток")

def download_and_save(idx):
    url = URLS[idx]
    local_path = LOCAL_PATHS[idx]
    try:
        data = fetch_data(url)

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f_old:
                    old_data = f_old.read()
                if old_data == data:
                    log(f"🔄 Изменений для {local_path} нет (локально). Пропуск загрузки в GitHub.")
                    return None
            except Exception:
                pass

        save_to_local_file(local_path, data)
        return local_path, REMOTE_PATHS[idx]
    except Exception as e:
        short_msg = str(e)
        if len(short_msg) > 200:
            short_msg = short_msg[:200] + "…"
        log(f"⚠️ Ошибка при скачивании {url}: {short_msg}")
        return None

def create_filtered_configs():
    """Создает 26-й файл с конфигами, содержащими указанные SNI домены"""
    sni_domains = [
        "stats.vk-portal.net",
        "sun6-21.userapi.com",
        "sun6-20.userapi.com",
        "avatars.mds.yandex.net",
        "queuev4.vk.com",
        "sun6-22.userapi.com",
        "sync.browser.yandex.net",
        "top-fwz1.mail.ru",
        "ad.mail.ru",
        "eh.vk.com",
        "akashi.vk-portal.net",
        "sun9-38.userapi.com",
        "st.ozone.ru",
        "ir.ozone.ru",
        "vt-1.ozone.ru",
        "io.ozone.ru",
        "ozone.ru",
        "xapi.ozon.ru",
        "top-fwz1.mail.ru",
        "strm-rad-23.strm.yandex.net",
        "online.sberbank.ru",
        "esa-res.online.sberbank.ru",
        "egress.yandex.net",
        "st.okcdn.ru",
        "rs.mail.ru",
        "counter.yadro.ru",
        "742231.ms.ok.ru",
        "splitter.wb.ru",
        "a.wb.ru",
        "user-geo-data.wildberries.ru",
        "banners-website.wildberries.ru",
        "chat-prod.wildberries.ru",
        "servicepipe.ru",
        "alfabank.ru",
        "statad.ru",
        "alfabank.servicecdn.ru",
        "alfabank.st",
        "ad.adriver.ru",
        "privacy-cs.mail.ru",
        "imgproxy.cdn-tinkoff.ru",
        "mddc.tinkoff.ru",
        "le.tbank.ru",
        "hrc.tbank.ru",
        "id.tbank.ru",
        "rap.skcrtxr.com",
        "eye.targetads.io",
        "px.adhigh.net",
        "top-fwz1.mail.ru",
        "nspk.ru",
        "sba.yandex.net",
        "identitystatic.mts.ru",
        "tag.a.mts.ru",
        "login.mts.ru",
        "serving.a.mts.ru",
        "cm.a.mts.ru",
        "login.vk.com",
        "api.a.mts.ru",
        "mtscdn.ru",
        "d5de4k0ri8jba7ucdbt6.apigw.yandexcloud.net",
        "moscow.megafon.ru",
        "api.mindbox.ru",
        "web-static.mindbox.ru",
        "storage.yandexcloud.net",
        "personalization-web-stable.mindbox.ru",
        "www.t2.ru",
        "beeline.api.flocktory.com",
        "static.beeline.ru",
        "moskva.beeline.ru",
        "wcm.weborama-tech.ru",
        "1013a--ma--8935--cp199.stbid.ru",
        "msk.t2.ru",
        "s3.t2.ru",
        "get4click.ru",
        "dzen.ru",
        "yastatic.net",
        "csp.yandex.net",
        "sntr.avito.ru",
        "yabro-wbplugin.edadeal.yandex.ru",
        "cdn.uxfeedback.ru",
        "goya.rutube.ru",
        "api.expf.ru",
        "fb-cdn.premier.one",
        "www.kinopoisk.ru",
        "widgets.kinopoisk.ru",
        "payment-widget.plus.kinopoisk.ru",
        "api.events.plus.yandex.net",
        "tns-counter.ru",
        "speller.yandex.net",
        "widgets.cbonds.ru",
        "www.magnit.com",
        "magnit-ru.injector.3ebra.net",
        "jsons.injector.3ebra.net",
        "2gis.ru",
        "d-assets.2gis.ru",
        "s1.bss.2gis.com",
        "www.tbank.ru",
        "strm-spbmiran-08.strm.yandex.net",
        "id.tbank.ru",
        "tmsg.tbank.ru",
        "vk.com",
        "www.wildberries.ru",
        "www.ozon.ru",
        "ok.ru",
        "yandex.ru",
        "www.unicreditbank.ru",
        "www.gazprombank.ru",
        "cdn.gpb.ru",
        "mkb.ru",
        "www.open.ru",
        "cobrowsing.tbank.ru",
        "cdn.rosbank.ru",
        "www.psbank.ru",
        "www.raiffeisen.ru",
        "www.rzd.ru",
        "st.gismeteo.st",
        "stat-api.gismeteo.net",
        "c.dns-shop.ru",
        "restapi.dns-shop.ru",
        "www.pochta.ru",
        "passport.pochta.ru",
        "chat-ct.pochta.ru",
        "www.x5.ru",
        "www.ivi.ru",
        "api2.ivi.ru",
        "hh.ru",
        "i.hh.ru",
        "hhcdn.ru",
        "sentry.hh.ru",
        "cpa.hh.ru",
        "www.kp.ru",
        "cdnn21.img.ria.ru",
        "lenta.ru",
        "sync.rambler.ru",
        "s.rbk.ru",
        "www.rbc.ru",
        "target.smi2.net",
        "hb-bidder.skcrtxr.com",
        "strm-spbmiran-07.strm.yandex.net",
        "pikabu.ru",
        "www.tutu.ru",
        "cdn1.tu-tu.ru",
        "api.apteka.ru",
        "static.apteka.ru",
        "images.apteka.ru",
        "scitylana.apteka.ru",
        "www.drom.ru",
        "c.rdrom.ru",
        "www.farpost.ru",
        "s11.auto.drom.ru",
        "i.rdrom.ru",
        "yummy.drom.ru",
        "www.drive2.ru",
        "lemanapro.ru"
    ]
    
    all_configs = []

    # Читаем все 25 файлов и собираем конфиги, содержащие указанные домены
    for i in range(1, 26):
        local_path = f"githubmirror/{i}.txt"
        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if any(domain in line for domain in sni_domains):
                            all_configs.append(line)
            except Exception as e:
                log(f"⚠️ Ошибка при чтении файла {local_path}: {e}")

    def _extract_host_port(line: str):
        """Пробует извлечь host и port из строки конфига.
        Поддерживает несколько форматов: vmess://<base64-json>, обычные URI с схемой,
        а также простые вхождения host:port или ip:port через regex.
        Возвращает кортеж (host, port) или None.
        """
        if not line:
            return None

        # vmess://<base64>
        try:
            if line.lower().startswith("vmess://"):
                payload = line[len("vmess://"):]
                # корректируем паддинг и декодируем
                try:
                    payload_bytes = base64.b64decode(payload + '=' * (-len(payload) % 4))
                    decoded = payload_bytes.decode('utf-8', errors='ignore')
                    j = json.loads(decoded)
                    host = j.get('add') or j.get('host') or j.get('ip')
                    port = j.get('port')
                    if host and port:
                        return host, str(port)
                except Exception:
                    pass
        except Exception:
            pass

        # Попытка распарсить как URI (trojan://, vless://, http:// и т.д.)
        try:
            parsed = urllib.parse.urlparse(line if '://' in line else '//' + line)
            if parsed.hostname and parsed.port:
                return parsed.hostname, str(parsed.port)
        except Exception:
            pass

        # Ищем явное вхождение host:port или ip:port
        m = re.search(r'(?P<host>(?:\d{1,3}\.){3}\d{1,3}|[A-Za-z0-9\-_.]+):(?P<port>\d{1,5})', line)
        if m:
            return m.group('host'), m.group('port')

        return None

    # Удаляем дубликаты: сначала проверяем полное совпадение строки, затем
    # считаем дубликатом конфиг с тем же host:port (ip:port)
    seen_full = set()
    seen_hostport = set()
    unique_configs = []

    for cfg in all_configs:
        c = cfg.strip()
        if not c:
            continue

        if c in seen_full:
            continue
        seen_full.add(c)

        hostport = _extract_host_port(c)
        if hostport:
            key = f"{hostport[0].lower()}:{hostport[1]}"
            if key in seen_hostport:
                # уже есть сервер с таким же host:port — считаем дубликатом
                continue
            seen_hostport.add(key)

        unique_configs.append(c)

    # Сохраняем в 26-й файл
    local_path_26 = "githubmirror/26.txt"
    try:
        with open(local_path_26, "w", encoding="utf-8") as file:
            for config in unique_configs:
                file.write(config + "\n")
        log(f"📁 Создан файл {local_path_26} с {len(unique_configs)} конфигами, содержащими указанные SNI домены")
    except Exception as e:
        log(f"⚠️ Ошибка при сохранении {local_path_26}: {e}")

    return local_path_26

def main(dry_run: bool = False):
    max_workers_download = min(DEFAULT_MAX_WORKERS, max(1, len(URLS)))
    max_workers_upload = max(2, min(6, len(URLS)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_download) as download_pool, \
         concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_upload) as upload_pool:

        download_futures = [download_pool.submit(download_and_save, i) for i in range(len(URLS))]
        upload_futures: list[concurrent.futures.Future] = []

        for future in concurrent.futures.as_completed(download_futures):
            result = future.result()
            if result:
                local_path, remote_path = result
                if dry_run:
                    log(f"ℹ️ Dry-run: пропускаем загрузку {remote_path} (локальный путь {local_path})")
                else:
                    upload_futures.append(upload_pool.submit(upload_to_github, local_path, remote_path))

        for uf in concurrent.futures.as_completed(upload_futures):
            _ = uf.result()

    # Создаем 26-й файл с отфильтрованными конфигами
    local_path_26 = create_filtered_configs()
    
    # Загружаем 26-й файл в GitHub
    if not dry_run:
        upload_to_github(local_path_26, "githubmirror/26.txt")

    # Обновляем таблицу в README.md после всех загрузок
    if not dry_run and updated_files:
        update_readme_table()

    # Вывод логов
    ordered_keys = sorted(k for k in LOGS_BY_FILE.keys() if k != 0)
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

    parser = argparse.ArgumentParser(description="Скачивание конфигов и загрузка в GitHub")
    parser.add_argument("--dry-run", action="store_true", help="Только скачивать и сохранять локально, не загружать в GitHub")
    args = parser.parse_args()

    main(dry_run=args.dry_run)