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
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -------------------- SNI домены --------------------
# Список доменов для фильтрации, комментарии игнорируются
SNI_DOMAINS_RAW = """
stats.vk-portal.net - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
sun6-21.userapi.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
sun6-20.userapi.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
avatars.mds.yandex.net
queuev4.vk.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
sun6-22.userapi.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
sync.browser.yandex.net
top-fwz1.mail.ru
ad.mail.ru
eh.vk.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
akashi.vk-portal.net - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
sun9-38.userapi.com
st.ozone.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
ir.ozone.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
vt-1.ozone.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
io.ozone.ru
ozone.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
xapi.ozon.ru
top-fwz1.mail.ru
strm-rad-23.strm.yandex.net
online.sberbank.ru
esa-res.online.sberbank.ru
egress.yandex.net
st.okcdn.ru
rs.mail.ru
counter.yadro.ru
742231.ms.ok.ru
splitter.wb.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
a.wb.ru - работает на МТС.
user-geo-data.wildberries.ru
banners-website.wildberries.ru
chat-prod.wildberries.ru
servicepipe.ru
alfabank.ru - работает на МТС, Мегафон, Т2, Yota.
statad.ru
alfabank.servicecdn.ru
alfabank.st
ad.adriver.ru
privacy-cs.mail.ru
imgproxy.cdn-tinkoff.ru
mddc.tinkoff.ru
le.tbank.ru
hrc.tbank.ru
id.tbank.ru
rap.skcrtxr.com
eye.targetads.io
px.adhigh.net
top-fwz1.mail.ru
nspk.ru
sba.yandex.net - работает на МТС, Мегафон.
identitystatic.mts.ru
tag.a.mts.ru
login.mts.ru
serving.a.mts.ru
cm.a.mts.ru
login.vk.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК.
api.a.mts.ru
mtscdn.ru
d5de4k0ri8jba7ucdbt6.apigw.yandexcloud.net
moscow.megafon.ru
api.mindbox.ru
web-static.mindbox.ru
storage.yandexcloud.net
personalization-web-stable.mindbox.ru
www.t2.ru
beeline.api.flocktory.com
static.beeline.ru
moskva.beeline.ru
wcm.weborama-tech.ru
1013a--ma--8935--cp199.stbid.ru
msk.t2.ru
s3.t2.ru
get4click.ru
dzen.ru - работает на Мегафон, Т2.
yastatic.net
csp.yandex.net
sntr.avito.ru
yabro-wbplugin.edadeal.yandex.ru
cdn.uxfeedback.ru
goya.rutube.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК.
api.expf.ru
fb-cdn.premier.one
www.kinopoisk.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
widgets.kinopoisk.ru
payment-widget.plus.kinopoisk.ru
api.events.plus.yandex.net
tns-counter.ru
speller.yandex.net - работает на МТС, Мегафон, Т2, Тмобайл, РТК, Yota.
widgets.cbonds.ru
www.magnit.com
magnit-ru.injector.3ebra.net
jsons.injector.3ebra.net
2gis.ru
d-assets.2gis.ru
s1.bss.2gis.com
www.tbank.ru
strm-spbmiran-08.strm.yandex.net
id.tbank.ru
tmsg.tbank.ru
vk.com - работает на МТС, Мегафон, Т2, Тмобайл, РТК.
www.wildberries.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК.
www.ozon.ru - работает на МТС, Мегафон, Т2, Тмобайл, РТК.
ok.ru - работает на МТС, Мегафон.
yandex.ru - работает на МТС, Мегафон, Т2.
www.unicreditbank.ru
www.gazprombank.ru
cdn.gpb.ru
mkb.ru
www.open.ru
cobrowsing.tbank.ru
cdn.rosbank.ru
www.psbank.ru - будет работать только на серверах в RU локациях
www.raiffeisen.ru
www.rzd.ru - будет работать только на серверах в RU локациях
st.gismeteo.st
stat-api.gismeteo.net
c.dns-shop.ru
restapi.dns-shop.ru
www.pochta.ru
passport.pochta.ru
chat-ct.pochta.ru
www.x5.ru
www.ivi.ru
api2.ivi.ru
hh.ru
i.hh.ru
hhcdn.ru
sentry.hh.ru
cpa.hh.ru
www.kp.ru
cdnn21.img.ria.ru
lenta.ru
sync.rambler.ru
s.rbk.ru
www.rbc.ru
target.smi2.net
hb-bidder.skcrtxr.com
strm-spbmiran-07.strm.yandex.net
pikabu.ru
www.tutu.ru
cdn1.tu-tu.ru
api.apteka.ru
static.apteka.ru
images.apteka.ru
scitylana.apteka.ru
www.drom.ru
c.rdrom.ru
www.farpost.ru
s11.auto.drom.ru
i.rdrom.ru
yummy.drom.ru
www.drive2.ru
lemanapro.ru
"""
SNI_DOMAINS = {line.split('-')[0].strip() for line in SNI_DOMAINS_RAW.strip().split('\n') if line.strip()}


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
# Добавляем "источник" для 26-го файла, который будет сгенерирован локально
URLS.append("local://filtered-by-sni")

REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]

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
        if parsed.scheme == "local":
            return "Filtered by SNI"
        path_parts = parsed.path.split('/')
        if len(path_parts) > 2:
            return f"{path_parts[1]}/{path_parts[2]}"
        return parsed.netloc
    except:
        return "Источник"

def update_readme_table():
    """Обновляет таблицу в README.md с информацией о времени последнего обновления"""
    try:
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

        time_part, date_part = offset.split(" | ")
        
        table_header = "| № | Файл | Источник | Время | Дата |\n|--|--|--|--|--|"
        table_rows = []
        
        for i, url in enumerate(URLS, 1):
            filename = f"{i}.txt"
            source_name = extract_source_name(url)
            
            if i in updated_files:
                update_time = time_part
                update_date = date_part
            else:
                pattern = rf"\|\s*{i}\s*\|\s*`{filename}`.*?\|\s*.*?\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
                match = re.search(pattern, old_content)
                if match:
                    update_time = match.group(1).strip() if match.group(1) and match.group(1).strip() else "Никогда"
                    update_date = match.group(2).strip() if match.group(2) and match.group(2).strip() else "Никогда"
                else:
                    update_time = "Никогда"
                    update_date = "Никогда"
            
            source_link = f"[{source_name}]({url})" if url.startswith("http") else source_name
            table_rows.append(f"| {i} | `{filename}` | {source_link} | {update_time} | {update_date} |")

        new_table = table_header + "\n" + "\n".join(table_rows)

        table_pattern = r"\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?(\n\n## |$)"
        if re.search(table_pattern, old_content):
            new_content = re.sub(table_pattern, new_table + r"\1", old_content, 1)
        else:
            new_content = old_content + "\n\n" + new_table

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
                    file_index = int(re.search(r'(\d+)', remote_path).group(1))
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
                file_index = int(re.search(r'(\d+)', remote_path).group(1))
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

    log(f"❌ Не удалось обновить {remote_path} после {max_retries} попыток")

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
                    log(f"🔄 Изменений для {local_path} нет (локально).")
                    return
            except Exception:
                pass

        save_to_local_file(local_path, data)
    except Exception as e:
        short_msg = str(e)
        if len(short_msg) > 200:
            short_msg = short_msg[:200] + "…"
        log(f"⚠️ Ошибка при скачивании {url}: {short_msg}")

def process_and_create_26th_file():
    """
    Собирает конфиги с определенными SNI доменами из файлов 1-25
    и сохраняет их в файл 26.txt.
    """
    log("🔄 Начало обработки файлов для создания githubmirror/26.txt")
    found_configs = set()
    
    for i in range(1, 26):
        local_path = f"githubmirror/{i}.txt"
        if not os.path.exists(local_path):
            continue

        try:
            with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if any(domain in line for domain in SNI_DOMAINS):
                        found_configs.add(line.strip())
        except Exception as e:
            log(f"⚠️ Ошибка при чтении файла {local_path}: {e}")

    if not found_configs:
        log("ℹ️ Не найдено конфигов с указанными SNI. Файл githubmirror/26.txt не будет создан/обновлен.")
        return

    output_path = "githubmirror/26.txt"
    new_content = "\n".join(sorted(list(found_configs)))

    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f_old:
                old_content = f_old.read()
            if old_content.strip() == new_content.strip():
                log(f"🔄 Изменений для {output_path} нет (локально).")
                return
        except Exception:
            pass 

    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(new_content)
    log(f"✅ Файл {output_path} создан/обновлен с {len(found_configs)} уникальными конфигами.")


def main(dry_run: bool = False):
    max_workers_download = min(DEFAULT_MAX_WORKERS, max(1, len(URLS) - 1))
    max_workers_upload = max(2, min(6, len(URLS)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_download) as download_pool, \
         concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_upload) as upload_pool:

        # --- ФАЗА СКАЧИВАНИЯ ---
        download_futures = [download_pool.submit(download_and_save, i) for i in range(len(URLS) - 1)]
        concurrent.futures.wait(download_futures)
        
        # --- ФАЗА ОБРАБОТКИ ---
        process_and_create_26th_file()

        # --- ФАЗА ЗАГРУЗКИ ---
        upload_futures: list[concurrent.futures.Future] = []
        if not dry_run:
            for i in range(len(LOCAL_PATHS)):
                local_path = LOCAL_PATHS[i]
                remote_path = REMOTE_PATHS[i]
                if os.path.exists(local_path):
                    upload_futures.append(upload_pool.submit(upload_to_github, local_path, remote_path))

        for uf in concurrent.futures.as_completed(upload_futures):
            _ = uf.result()

    if not dry_run and updated_files:
        update_readme_table()

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

    # Принудительно включаем dry-run, если токен GitHub не найден
    is_dry_run = args.dry_run or not GITHUB_TOKEN
    if not GITHUB_TOKEN:
        print("Переменная окружения MY_TOKEN не найдена. Запуск в режиме dry-run.")

    main(dry_run=is_dry_run)