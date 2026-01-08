from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import defaultdict
from github import GithubException
from github import Github, Auth
from datetime import datetime
import concurrent.futures
import urllib.parse
import threading
import zoneinfo
import requests
import urllib3
import base64
import html
import json
import re
import os

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

# Источники для 26-го файла (без SNI проверки, только дедупликация)
EXTRA_URLS_FOR_26 = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Cable.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_nolite.txt",
    "https://raw.githubusercontent.com/EtoNeYaProject/etoneyaproject.github.io/refs/heads/main/2",
    "https://s3c3.001.gpucloud.ru/dixsm/htxml",
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
                # Для 26-го файла создаем ссылку на сам файл с текстом "Обход SNI/CIDR белых списков"
                source_name = "Обход SNI/CIDR белых списков"
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
                message="📝 Обновление таблицы в README.md по часовому поясу Европа/Москва: {offset}",
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
        # Распаковываем результат (data, _)
        data, _ = filter_insecure_configs(local_path, data)

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

INSECURE_PATTERN = re.compile(
    r'(?:[?&;]|3%[Bb])(allowinsecure|allow_insecure|insecure)=(?:1|true|yes)(?:[&;#]|$|(?=\s|$))',
    re.IGNORECASE
)

def filter_insecure_configs(local_path, data, log_enabled=True):
    result = []
    splitted = data.splitlines()

    for line in splitted:
        original_line = line
        processed = line.strip()
        processed = urllib.parse.unquote(html.unescape(processed))

        if INSECURE_PATTERN.search(processed):
            continue

        result.append(original_line)

    filtered_count = len(splitted) - len(result)
    
    # Логируем сразу только если это обычные файлы (1-25) и логирование включено
    if filtered_count > 0 and log_enabled:
        log(f"ℹ️ Отфильтровано {filtered_count} небезопасных конфигов для {local_path}")
    
    # Возвращаем и текст, и количество удаленных
    return "\n".join(result), filtered_count

def create_filtered_configs():
    """Создает 26-й файл с конфигами, содержащими указанные SNI домены (Максимальное ускорение)"""
    sni_domains = [
        "00.img.avito.st", "01.img.avito.st", "02.img.avito.st", "03.img.avito.st", "04.img.avito.st",
        "05.img.avito.st", "06.img.avito.st", "07.img.avito.st", "08.img.avito.st", "09.img.avito.st",
        "10.img.avito.st", "1013a--ma--8935--cp199.stbid.ru", "11.img.avito.st", "12.img.avito.st",
        "13.img.avito.st", "14.img.avito.st", "15.img.avito.st", "16.img.avito.st", "17.img.avito.st",
        "18.img.avito.st", "19.img.avito.st", "1l-api.mail.ru", "1l-go.mail.ru", "1l-hit.mail.ru",
        "1l-s2s.mail.ru", "1l-view.mail.ru", "1l.mail.ru", "1link.mail.ru", "20.img.avito.st",
        "2018.mail.ru", "2019.mail.ru", "2020.mail.ru", "2021.mail.ru", "21.img.avito.st",
        "22.img.avito.st", "23.img.avito.st", "23feb.mail.ru", "24.img.avito.st", "25.img.avito.st",
        "26.img.avito.st", "27.img.avito.st", "28.img.avito.st", "29.img.avito.st", "2gis.com",
        "2gis.ru", "30.img.avito.st", "300.ya.ru", "31.img.avito.st", "32.img.avito.st",
        "33.img.avito.st", "34.img.avito.st", "3475482542.mc.yandex.ru", "35.img.avito.st",
        "36.img.avito.st", "37.img.avito.st", "38.img.avito.st", "39.img.avito.st", "40.img.avito.st",
        "41.img.avito.st", "42.img.avito.st", "43.img.avito.st", "44.img.avito.st", "45.img.avito.st",
        "46.img.avito.st", "47.img.avito.st", "48.img.avito.st", "49.img.avito.st", "50.img.avito.st",
        "51.img.avito.st", "52.img.avito.st", "53.img.avito.st", "54.img.avito.st", "55.img.avito.st",
        "56.img.avito.st", "57.img.avito.st", "58.img.avito.st", "59.img.avito.st", "60.img.avito.st",
        "61.img.avito.st", "62.img.avito.st", "63.img.avito.st", "64.img.avito.st", "65.img.avito.st",
        "66.img.avito.st", "67.img.avito.st", "68.img.avito.st", "69.img.avito.st", "70.img.avito.st",
        "71.img.avito.st", "72.img.avito.st", "73.img.avito.st", "74.img.avito.st", "742231.ms.ok.ru",
        "75.img.avito.st", "76.img.avito.st", "77.img.avito.st", "78.img.avito.st", "79.img.avito.st",
        "80.img.avito.st", "81.img.avito.st", "82.img.avito.st", "83.img.avito.st", "84.img.avito.st",
        "85.img.avito.st", "86.img.avito.st", "87.img.avito.st", "88.img.avito.st", "89.img.avito.st",
        "8mar.mail.ru", "8march.mail.ru", "90.img.avito.st", "91.img.avito.st", "92.img.avito.st",
        "93.img.avito.st", "94.img.avito.st", "95.img.avito.st", "96.img.avito.st", "97.img.avito.st",
        "98.img.avito.st", "99.img.avito.st", "9may.mail.ru", "a.auth-nsdi.ru", "a.res-nsdi.ru",
        "a.wb.ru", "aa.mail.ru", "ad.adriver.ru", "ad.mail.ru", "adm.digital.gov.ru", "adm.mp.rzd.ru",
        "admin.cs7777.vk.ru", "admin.tau.vk.ru", "adv.ozon.ru", "ads.vk.ru", "afisha.mail.ru",
        "agent.mail.ru", "akashi.vk-portal.net", "alfabank.ru", "alfabank.servicecdn.ru", "alfabank.st",
        "alpha3.minigames.mail.ru", "alpha4.minigames.mail.ru", "amigo.mail.ru", "ams2-cdn.2gis.com",
        "an.yandex.ru", "analytics.predict.mail.ru", "analytics.vk.ru", "answer.mail.ru",
        "answers.mail.ru", "api-maps.yandex.ru", "api.2gis.ru", "api.a.mts.ru", "api.apteka.ru",
        "api.avito.ru", "api.browser.yandex.com", "api.browser.yandex.ru", "api.cs7777.vk.ru",
        "api.events.plus.yandex.net", "api.expf.ru", "api.max.ru", "api.mindbox.ru", "api.ok.ru",
        "api.photo.2gis.com", "api.plus.kinopoisk.ru", "api.predict.mail.ru", "api.reviews.2gis.com",
        "api.s3.yandex.net", "api.tau.vk.ru", "api.uxfeedback.yandex.net", "api.vk.ru", "api2.ivi.ru",
        "apps.research.mail.ru", "authdl.mail.ru", "auto.mail.ru", "auto.ru", "autodiscover.corp.mail.ru",
        "autodiscover.ord.ozon.ru", "av.mail.ru", "avatars.mds.yandex.com", "avatars.mds.yandex.net",
        "avito.ru", "avito.st", "aw.mail.ru", "away.cs7777.vk.ru", "away.tau.vk.ru", "azt.mail.ru",
        "b.auth-nsdi.ru", "b.res-nsdi.ru", "bank.ozon.ru", "banners-website.wildberries.ru", "bb.mail.ru",
        "bd.mail.ru", "beeline.api.flocktory.com", "beko.dom.mail.ru", "bender.mail.ru", "beta.mail.ru",
        "bfds.sberbank.ru", "bitva.mail.ru", "biz.mail.ru", "blackfriday.mail.ru", "blog.mail.ru",
        "bot.gosuslugi.ru", "botapi.max.ru", "bratva-mr.mail.ru", "bro-bg-store.s3.yandex.com",
        "bro-bg-store.s3.yandex.net", "bro-bg-store.s3.yandex.ru", "brontp-pre.yandex.ru",
        "browser.mail.ru", "browser.yandex.com", "browser.yandex.ru", "business.vk.ru", "c.dns-shop.ru",
        "c.rdrom.ru", "calendar.mail.ru", "capsula.mail.ru", "cargo.rzd.ru", "cars.mail.ru",
        "catalog.api.2gis.com", "cdn.connect.mail.ru", "cdn.gpb.ru", "cdn.lemanapro.ru",
        "cdn.newyear.mail.ru", "cdn.rosbank.ru", "cdn.s3.yandex.net", "cdn.tbank.ru",
        "cdn.uxfeedback.ru", "cdn.yandex.ru", "cdn1.tu-tu.ru", "cdnrhkgfkkpupuotntfj.svc.cdn.yandex.net",
        "cdnn21.img.ria.ru", "cf.mail.ru", "chat-ct.pochta.ru", "chat-prod.wildberries.ru", "chat3.vtb.ru",
        "cloud.cdn.yandex.com", "cloud.cdn.yandex.net", "cloud.cdn.yandex.ru", "cloud.mail.ru",
        "cloud.vk.com", "cloud.vk.ru", "cloudcdn-ams19.cdn.yandex.net", "cloudcdn-m9-10.cdn.yandex.net",
        "cloudcdn-m9-12.cdn.yandex.net", "cloudcdn-m9-13.cdn.yandex.net", "cloudcdn-m9-14.cdn.yandex.net",
        "cloudcdn-m9-15.cdn.yandex.net", "cloudcdn-m9-2.cdn.yandex.net", "cloudcdn-m9-3.cdn.yandex.net",
        "cloudcdn-m9-4.cdn.yandex.net", "cloudcdn-m9-5.cdn.yandex.net", "cloudcdn-m9-6.cdn.yandex.net",
        "cloudcdn-m9-7.cdn.yandex.net", "cloudcdn-m9-9.cdn.yandex.net", "cm.a.mts.ru",
        "cms-res-web.online.sberbank.ru", "cobma.mail.ru", "cobmo.mail.ru", "cobrowsing.tbank.ru",
        "code.mail.ru", "codefest.mail.ru", "cog.mail.ru", "collections.yandex.com",
        "collections.yandex.ru", "comba.mail.ru", "combu.mail.ru", "commba.mail.ru", "company.rzd.ru",
        "compute.mail.ru", "connect.cs7777.vk.ru", "contacts.rzd.ru", "contract.gosuslugi.ru",
        "corp.mail.ru", "counter.yadro.ru", "cpa.hh.ru", "cpg.money.mail.ru", "crazypanda.mail.ru",
        "crowdtest.payment-widget-smarttv.plus.tst.kinopoisk.ru",
        "crowdtest.payment-widget.plus.tst.kinopoisk.ru", "cs.avito.ru", "cs7777.vk.ru", "csp.yandex.net",
        "ctlog.mail.ru", "ctlog2023.mail.ru", "ctlog2024.mail.ru", "cto.mail.ru", "cups.mail.ru",
        "d-assets.2gis.ru", "d5de4k0ri8jba7ucdbt6.apigw.yandexcloud.net", "da-preprod.biz.mail.ru",
        "da.biz.mail.ru", "data.amigo.mail.ru", "dating.ok.ru", "deti.mail.ru", "dev.cs7777.vk.ru",
        "dev.max.ru", "dev.tau.vk.ru", "dev1.mail.ru", "dev2.mail.ru", "dev3.mail.ru", "digital.gov.ru",
        "disk.2gis.com", "disk.rzd.ru", "dk.mail.ru", "dl.mail.ru", "dl.marusia.mail.ru",
        "dmp.dmpkit.lemanapro.ru", "dn.mail.ru", "dnd.wb.ru", "dobro.mail.ru", "doc.mail.ru",
        "dom.mail.ru", "download.max.ru", "dr.yandex.net", "dr2.yandex.net", "dragonpals.mail.ru",
        "ds.mail.ru", "duck.mail.ru", "dzen.ru", "e.mail.ru", "education.mail.ru", "egress.yandex.net",
        "eh.vk.com", "ekmp-a-51.rzd.ru", "enterprise.api-maps.yandex.ru", "esa-res.online.sberbank.ru",
        "esc.predict.mail.ru", "esia.gosuslugi.ru", "et.mail.ru", "expert.vk.ru",
        "external-api.mediabilling.kinopoisk.ru", "external-api.plus.kinopoisk.ru", "eye.targetads.io",
        "favorites.api.2gis.com", "favicon.yandex.com", "favicon.yandex.net", "favicon.yandex.ru",
        "fb-cdn.premier.one", "fe.mail.ru", "filekeeper-vod.2gis.com", "finance.mail.ru", "finance.wb.ru",
        "five.predict.mail.ru", "foto.mail.ru", "frontend.vh.yandex.ru", "fw.wb.ru", "games-bamboo.mail.ru",
        "games-fisheye.mail.ru", "games.mail.ru", "genesis.mail.ru", "geo-apart.predict.mail.ru",
        "get4click.ru", "gibdd.mail.ru", "go.mail.ru", "golos.mail.ru", "gosuslugi.ru",
        "gosweb.gosuslugi.ru", "goya.rutube.ru", "gpb.finance.mail.ru", "graphql-web.kinopoisk.ru",
        "graphql.kinopoisk.ru", "gu-st.ru", "guns.mail.ru", "hb-bidder.skcrtxr.com", "hd.kinopoisk.ru",
        "health.mail.ru", "help.max.ru", "help.mcs.mail.ru", "hh.ru", "hhcdn.ru", "hi-tech.mail.ru",
        "horo.mail.ru", "hrc.tbank.ru", "hs.mail.ru", "http-check-headers.yandex.ru", "i.hh.ru",
        "i.max.ru", "i.rdrom.ru", "i0.photo.2gis.com", "i1.photo.2gis.com", "i2.photo.2gis.com",
        "i3.photo.2gis.com", "i4.photo.2gis.com", "i5.photo.2gis.com", "i6.photo.2gis.com",
        "i7.photo.2gis.com", "i8.photo.2gis.com", "i9.photo.2gis.com", "id.cs7777.vk.ru", "id.sber.ru",
        "id.tau.vk.ru", "id.tbank.ru", "id.vk.ru", "identitystatic.mts.ru", "images.apteka.ru",
        "imperia.mail.ru", "imgproxy.cdn-tinkoff.ru", "informer.yandex.ru", "infra.mail.ru",
        "internet.mail.ru", "invest.ozon.ru", "io.ozone.ru", "ir.ozone.ru", "it.mail.ru", "izbirkom.ru",
        "jam.api.2gis.com", "jd.mail.ru", "jitsi.wb.ru", "journey.mail.ru", "jsons.injector.3ebra.net",
        "juggermobile.mail.ru", "junior.mail.ru", "keys.api.2gis.com", "kicker.mail.ru", "kiks.yandex.com",
        "kiks.yandex.ru", "kingdomrift.mail.ru", "kino.mail.ru", "knights.mail.ru", "kobma.mail.ru",
        "kobmo.mail.ru", "komba.mail.ru", "kombo.mail.ru", "kombu.mail.ru", "kommba.mail.ru",
        "konflikt.mail.ru", "kz.mcs.mail.ru", "la.mail.ru", "lady.mail.ru", "landing.mail.ru",
        "le.tbank.ru", "learning.ozon.ru", "legal.max.ru", "legenda.mail.ru", "legendofheroes.mail.ru",
        "lemanapro.ru", "lenta.ru", "link.max.ru", "link.mp.rzd.ru", "live.ok.ru", "lk.gosuslugi.ru",
        "loa.mail.ru", "log.strm.yandex.ru", "login.cs7777.vk.ru", "login.mts.ru", "login.tau.vk.ru",
        "login.vk.com", "login.vk.ru", "lotro.mail.ru", "love.mail.ru", "m.47news.ru", "m.avito.ru",
        "m.cs7777.vk.ru", "m.ok.ru", "m.tau.vk.ru", "m.vk.ru", "m.vkvideo.cs7777.vk.ru",
        "ma.kinopoisk.ru", "magnit-ru.injector.3ebra.net", "mail.yandex.com", "mail.yandex.ru",
        "mailexpress.mail.ru", "mailer.mail.ru", "man.mail.ru", "map.gosuslugi.ru", "mapgl.2gis.com",
        "mapi.learning.ozon.ru", "maps.mail.ru", "market.rzd.ru", "marusia.mail.ru", "max.ru",
        "mc.yandex.com", "mc.yandex.ru", "mcs.mail.ru", "mddc.tinkoff.ru", "me.cs7777.vk.ru",
        "media-golos.mail.ru", "media.mail.ru", "mediafeeds.yandex.com", "mediafeeds.yandex.ru",
        "mediapro.mail.ru", "merch-cpg.money.mail.ru", "metrics.alfabank.ru", "microapps.kinopoisk.ru",
        "miniapp.internal.myteam.mail.ru", "minigames.mail.ru", "mkb.ru", "mking.mail.ru",
        "mobfarm.mail.ru", "money.mail.ru", "moscow.megafon.ru", "moskva.beeline.ru", "mosqa.mail.ru",
        "mowar.mail.ru", "mozilla.mail.ru", "mp.rzd.ru", "ms.cs7777.vk.ru", "msk.t2.ru", "mtscdn.ru",
        "multitest.ok.ru", "music.vk.ru", "my.mail.ru", "my.rzd.ru", "myteam.mail.ru", "nebogame.mail.ru",
        "net.mail.ru", "neuro.translate.yandex.ru", "new.mail.ru", "news.mail.ru", "newyear.mail.ru",
        "newyear2018.mail.ru", "nonstandard.sales.mail.ru", "notes.mail.ru", "novorossiya.gosuslugi.ru",
        "nspk.ru", "oauth.cs7777.vk.ru", "oauth.tau.vk.ru", "oauth2.cs7777.vk.ru", "octavius.mail.ru",
        "ok.ru", "oneclick-payment.kinopoisk.ru", "online.sberbank.ru", "operator.mail.ru",
        "ord.ozon.ru", "ord.vk.ru", "otvet.mail.ru", "otveti.mail.ru", "otvety.mail.ru", "owa.ozon.ru",
        "ozone.ru", "ozon.ru", "panzar.mail.ru", "park.mail.ru", "partners.gosuslugi.ru",
        "partners.lemanapro.ru", "passport.pochta.ru", "pay.mail.ru", "pay.ozon.ru",
        "payment-widget-smarttv.plus.kinopoisk.ru", "payment-widget.kinopoisk.ru",
        "payment-widget.plus.kinopoisk.ru", "pernatsk.mail.ru", "personalization-web-stable.mindbox.ru",
        "pets.mail.ru", "pic.rutubelist.ru", "pikabu.ru", "pl-res.online.sberbank.ru", "pms.mail.ru",
        "pochtabank.mail.ru", "pogoda.mail.ru", "pokerist.mail.ru", "polis.mail.ru", "pos.gosuslugi.ru",
        "pp.mail.ru", "pptest.userapi.com", "predict.mail.ru", "preview.rutube.ru", "primeworld.mail.ru",
        "privacy-cs.mail.ru", "prodvizhenie.rzd.ru", "ptd.predict.mail.ru", "pubg.mail.ru",
        "public-api.reviews.2gis.com", "public.infra.mail.ru", "pulse.mail.ru", "pulse.mp.rzd.ru",
        "push.vk.ru", "pw.mail.ru", "px.adhigh.net", "quantum.mail.ru", "queuev4.vk.com",
        "quiz.kinopoisk.ru", "r.vk.ru", "r0.mradx.net", "rap.skcrtxr.com", "rate.mail.ru",
        "rebus.calls.mail.ru", "rebus.octavius.mail.ru", "receive-sentry.lmru.tech", "reseach.mail.ru",
        "restapi.dns-shop.ru", "rev.mail.ru", "riot.mail.ru", "rl.mail.ru", "rm.mail.ru", "rs.mail.ru",
        "rt.api.operator.mail.ru", "rutube.ru", "rzd.ru", "s.rbk.ru", "s.vtb.ru", "s0.bss.2gis.com",
        "s1.bss.2gis.com", "s11.auto.drom.ru", "s3.babel.mail.ru", "s3.mail.ru", "s3.media-mobs.mail.ru",
        "s3.t2.ru", "s3.yandex.net", "sales.mail.ru", "sangels.mail.ru", "sba.yandex.com", "sba.yandex.net",
        "sba.yandex.ru", "sberbank.ru", "scitylana.apteka.ru", "sdk.money.mail.ru", "secure-cloud.rzd.ru",
        "secure.rzd.ru", "securepay.ozon.ru", "security.mail.ru", "seller.ozon.ru", "sentry.hh.ru",
        "service.amigo.mail.ru", "servicepipe.ru", "serving.a.mts.ru", "sfd.gosuslugi.ru",
        "shadowbound.mail.ru", "splitter.wb.ru", "sntr.avito.ru", "socdwar.mail.ru",
        "sochi-park.predict.mail.ru", "souz.mail.ru", "speller.yandex.net", "sphere.mail.ru",
        "sport.mail.ru", "ssp.rutube.ru", "sso-app4.vtb.ru", "sso-app5.vtb.ru", "sso.auto.ru",
        "sso.dzen.ru", "sso.kinopoisk.ru", "st-gismeteo.st", "st-im.kinopoisk.ru", "st-ok.cdn-vk.ru",
        "st.avito.ru", "st.gismeteo.st", "st.kinopoisk.ru", "st.max.ru", "st.okcdn.ru", "st.ozone.ru",
        "staging-analytics.predict.mail.ru", "staging-esc.predict.mail.ru",
        "staging-sochi-park.predict.mail.ru", "stand.aoc.mail.ru", "stand.bb.mail.ru", "stand.cb.mail.ru",
        "stand.la.mail.ru", "stand.pw.mail.ru", "startrek.mail.ru", "stat-api.gismeteo.net", "statad.ru",
        "static-mon.yandex.net", "static.apteka.ru", "static.beeline.ru", "static.dl.mail.ru",
        "static.lemanapro.ru", "static.operator.mail.ru", "static.rutube.ru", "stats.avito.ru",
        "stats.vk-portal.net", "status.mcs.mail.ru", "storage.ape.yandex.net", "storage.yandexcloud.net",
        "stormriders.mail.ru", "stream.mail.ru", "street-combats.mail.ru",
        "strm-rad-23.strm.yandex.net", "strm-spbmiran-07.strm.yandex.net", "strm-spbmiran-08.strm.yandex.net",
        "strm.yandex.net", "strm.yandex.ru", "styles.api.2gis.com", "suggest.dzen.ru",
        "suggest.sso.dzen.ru", "sun6-20.userapi.com", "sun6-21.userapi.com", "sun6-22.userapi.com",
        "sun9-101.userapi.com", "sun9-38.userapi.com", "support.biz.mail.ru", "support.mcs.mail.ru",
        "support.tech.mail.ru", "surveys.yandex.ru", "sync.browser.yandex.net", "sync.rambler.ru",
        "tag.a.mts.ru", "tamtam.ok.ru", "target.smi2.net", "target.vk.ru", "team.mail.ru", "team.rzd.ru",
        "tech.mail.ru", "tech.vk.ru", "tera.mail.ru", "ticket.rzd.ru", "tickets.widget.kinopoisk.ru",
        "tidaltrek.mail.ru", "tile0.maps.2gis.com", "tile1.maps.2gis.com", "tile2.maps.2gis.com",
        "tile3.maps.2gis.com", "tile4.maps.2gis.com", "tiles.maps.mail.ru", "tmgame.mail.ru",
        "tmsg.tbank.ru", "tns-counter.ru", "todo.mail.ru", "top-fwz1.mail.ru", "touch.kinopoisk.ru",
        "townwars.mail.ru", "travel.rzd.ru", "travel.yandex.ru", "travel.yastatic.net", "trk.mail.ru",
        "ttbh.mail.ru", "tv.mail.ru", "typewriter.mail.ru", "u.corp.mail.ru", "ufo.mail.ru",
        "ui.cs7777.vk.ru", "ui.tau.vk.ru", "user-geo-data.wildberries.ru", "uslugi.yandex.ru",
        "uxfeedback-cdn.s3.yandex.net", "uxfeedback.yandex.ru", "vk.com", "vk-portal.net", "vk.mail.ru",
        "vkdoc.mail.ru", "vkvideo.cs7777.vk.ru", "voina.mail.ru", "voter.gosuslugi.ru", "vt-1.ozone.ru",
        "wap.yandex.com", "wap.yandex.ru", "warface.mail.ru", "warheaven.mail.ru", "wartune.mail.ru",
        "wb.ru", "wcm.weborama-tech.ru", "web-static.mindbox.ru", "web.max.ru", "webagent.mail.ru",
        "weblink.predict.mail.ru", "webstore.mail.ru", "welcome.mail.ru", "welcome.rzd.ru", "wf.mail.ru",
        "wh-cpg.money.mail.ru", "whatsnew.mail.ru", "widgets.cbonds.ru", "widgets.kinopoisk.ru",
        "wok.mail.ru", "wos.mail.ru", "ws-api.oneme.ru", "ws.seller.ozon.ru", "www.avito.ru",
        "www.avito.st", "www.biz.mail.ru", "www.cikrf.ru", "www.drom.ru", "www.drive2.ru",
        "www.farpost.ru", "www.gazprombank.ru", "www.gosuslugi.ru", "www.ivi.ru", "www.kinopoisk.ru",
        "www.kp.ru", "www.magnit.com", "www.mail.ru", "www.mcs.mail.ru", "www.open.ru", "www.ozon.ru",
        "www.pochta.ru", "www.psbank.ru", "www.pubg.mail.ru", "www.raiffeisen.ru", "www.rbc.ru",
        "www.rzd.ru", "www.sberbank.ru", "www.t2.ru", "www.tbank.ru", "www.tutu.ru",
        "www.unicreditbank.ru", "www.vtb.ru", "www.wf.mail.ru", "www.wildberries.ru", "www.x5.ru",
        "xapi.ozon.ru", "ya.ru", "yabs.yandex.ru", "yabro-wbplugin.edadeal.yandex.ru", "yandex.com",
        "yandex.net", "yandex.ru", "yastatic.net", "yummy.drom.ru",
        "zen-yabro-morda.mediascope.mc.yandex.ru", "zen.yandex.com", "zen.yandex.net", "zen.yandex.ru"
    ]

    # 1. Оптимизация списка доменов
    sorted_domains = sorted(sni_domains, key=len)
    optimized_domains = []
    for d in sorted_domains:
        is_redundant = False
        for existing in optimized_domains:
            if existing in d:
                is_redundant = True
                break
        if not is_redundant:
            optimized_domains.append(d)

    try:
        pattern_str = r"(?:" + "|".join(re.escape(d) for d in optimized_domains) + r")"
        sni_regex = re.compile(pattern_str)
    except Exception as e:
        log(f"❌ Ошибка компиляции Regex: {e}")
        return None

    # Вспомогательные функции внутри
    def _extract_host_port(line: str):
        if not line: return None
        if line.startswith("vmess://"):
            try:
                payload = line[8:]
                rem = len(payload) % 4
                if rem: payload += '=' * (4 - rem)
                decoded = base64.b64decode(payload).decode('utf-8', errors='ignore')
                if decoded.startswith('{'):
                    j = json.loads(decoded)
                    host = j.get('add') or j.get('host') or j.get('ip')
                    port = j.get('port')
                    if host and port: return str(host), str(port)
            except Exception: pass
            return None
        m = re.search(r'(?:@|//)([\w\.-]+):(\d{1,5})', line)
        if m: return m.group(1), m.group(2)
        return None

    def _process_file_filtering(file_idx):
        local_path = f"githubmirror/{file_idx}.txt"
        filtered_lines = []
        if not os.path.exists(local_path):
            return filtered_lines
        try:
            with open(local_path, "r", encoding="utf-8") as file:
                content = file.read()
            content = re.sub(r'(vmess|vless|trojan|ss|ssr|tuic|hysteria|hysteria2)://', r'\n\1://', content)
            lines = content.splitlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                if sni_regex.search(line):
                    filtered_lines.append(line)
        except Exception:
            pass
        return filtered_lines

    all_configs = []

    # 2. Обработка файлов 1-25
    max_workers = min(16, os.cpu_count() + 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_process_file_filtering, i) for i in range(1, 26)]
        for future in concurrent.futures.as_completed(futures):
            all_configs.extend(future.result())

    # 3. Загрузка доп. источников для 26-го файла + ПОДСЧЕТ УДАЛЕННЫХ
    def _load_extra_configs(url):
        count_removed = 0
        configs = []
        try:
            data = fetch_data(url)
            # Вызываем с log_enabled=False, но забираем count
            data, count = filter_insecure_configs("githubmirror/26.txt", data, log_enabled=False)
            count_removed = count
            
            data = re.sub(r'(vmess|vless|trojan|ss|ssr|tuic|hysteria|hysteria2)://', r'\n\1://', data)
            lines = data.splitlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    configs.append(line)
        except Exception as e:
            short_msg = str(e)
            if len(short_msg) > 200:
                short_msg = short_msg[:200] + "…"
            log(f"⚠️ Ошибка при загрузке {url}: {short_msg}")
        
        # Возвращаем конфиги и количество удаленных
        return configs, count_removed
    
    extra_configs = []
    total_insecure_filtered_26 = 0 # Счетчик для 26-го файла

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(EXTRA_URLS_FOR_26))) as executor:
        futures = [executor.submit(_load_extra_configs, url) for url in EXTRA_URLS_FOR_26]
        for future in concurrent.futures.as_completed(futures):
            res_configs, res_count = future.result()
            extra_configs.extend(res_configs)
            total_insecure_filtered_26 += res_count # Суммируем
    
    # ЕДИНСТВЕННЫЙ ЛОГ ДЛЯ 26-го ФАЙЛА
    if total_insecure_filtered_26 > 0:
        log(f"ℹ️  Отфильтровано {total_insecure_filtered_26} небезопасных конфигов для githubmirror/26.txt")

    all_configs.extend(extra_configs)

    # Дедупликация
    seen_full = set()
    seen_hostport = set()
    unique_configs = []

    for cfg in all_configs:
        c = cfg.strip()
        if not c or c in seen_full: continue
        seen_full.add(c)
        hostport = _extract_host_port(c)
        if hostport:
            key = f"{hostport[0].lower()}:{hostport[1]}"
            if key in seen_hostport: continue
            seen_hostport.add(key)
        unique_configs.append(c)

    local_path_26 = "githubmirror/26.txt"
    try:
        with open(local_path_26, "w", encoding="utf-8") as file:
            file.write("\n".join(unique_configs))
        log(f"📁 Создан файл {local_path_26} с {len(unique_configs)} конфигами")
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
