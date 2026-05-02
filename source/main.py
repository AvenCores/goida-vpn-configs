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

# -------------------- ИСТОЧНИКИ --------------------
URLS = [
    "https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt",       # 1
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt",                # 2
    "https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt",        # 3
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt",                 # 4
    "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/sub.txt",      # 5
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",               # 6
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt",         # 7
    "https://raw.githubusercontent.com/CidVpn/cid-vpn-config/refs/heads/main/general.txt",        # 8
    "https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt", # 9
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/vless",                   # 10
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt",           # 11
    "https://github.com/VOID-Anonymity/V.O.I.D-VPN_Bypass/raw/refs/heads/main/url_work.txt",      # 12
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt", # 13
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes",                   # 14
    "https://raw.githubusercontent.com/miladtahanian/Config-Collector/refs/heads/main/mixed_iran.txt", # 15
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",                 # 16
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt",         # 17
    "https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt",                        # 18
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix",                    # 19
    "https://github.com/Argh94/Proxy-List/raw/refs/heads/main/All_Config.txt",                     # 20
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt",                      # 21
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri",  # 22
    "https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/BLACK_VLESS_RUS.txt",   # 23
    "https://github.com/Mr-Meshky/vify/raw/refs/heads/main/configs/vless.txt",                     # 24
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt",   # 25
]

# Источники для 26-го файла (без SNI-фильтрации, только дедупликация)
EXTRA_URLS_FOR_26 = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://raw.githubusercontent.com/EtoNeYaProject/etoneyaproject.github.io/refs/heads/main/2",
    "https://raw.githubusercontent.com/ByeWhiteLists/ByeWhiteLists2/refs/heads/main/ByeWhiteLists2.txt",
    "https://wlrus.lol/confs/selected.txt",
]

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

INSECURE_PATTERN = re.compile(
    r'(?:[?&;]|3%[Bb])(allowinsecure|allow_insecure|insecure)=(?:1|true|yes)(?:[&;#]|$|(?=\s|$))',
    re.IGNORECASE,
)


def filter_insecure_configs(local_path: str, data: str, log_enabled: bool = True) -> tuple[str, int]:
    result = []
    splitted = data.splitlines()
    for line in splitted:
        processed = urllib.parse.unquote(html.unescape(line.strip()))
        if not INSECURE_PATTERN.search(processed):
            result.append(line)

    filtered_count = len(splitted) - len(result)
    if filtered_count > 0 and log_enabled:
        log(f"ℹ️ Отфильтровано {filtered_count} небезопасных конфигов для {os.path.basename(local_path)}")
    return "\n".join(result), filtered_count

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
    sni_domains = [
        "00.img.avito.st", "01.img.avito.st", "02.img.avito.st", "03.img.avito.st",
        "04.img.avito.st", "05.img.avito.st", "06.img.avito.st", "07.img.avito.st",
        "08.img.avito.st", "09.img.avito.st", "10.img.avito.st", "1013a--ma--8935--cp199.stbid.ru",
        "11.img.avito.st", "12.img.avito.st", "13.img.avito.st", "14.img.avito.st",
        "15.img.avito.st", "16.img.avito.st", "17.img.avito.st", "18.img.avito.st",
        "19.img.avito.st", "1l-api.mail.ru", "1l-go.mail.ru", "1l-hit.mail.ru", "1l-s2s.mail.ru",
        "1l-view.mail.ru", "1l.mail.ru", "1link.mail.ru", "20.img.avito.st", "2018.mail.ru",
        "2019.mail.ru", "2020.mail.ru", "2021.mail.ru", "21.img.avito.st", "22.img.avito.st",
        "23.img.avito.st", "23feb.mail.ru", "24.img.avito.st", "25.img.avito.st",
        "26.img.avito.st", "27.img.avito.st", "28.img.avito.st", "29.img.avito.st", "2gis.com",
        "2gis.ru", "30.img.avito.st", "300.ya.ru", "31.img.avito.st", "32.img.avito.st",
        "33.img.avito.st", "34.img.avito.st", "3475482542.mc.yandex.ru", "35.img.avito.st",
        "36.img.avito.st", "37.img.avito.st", "38.img.avito.st", "39.img.avito.st",
        "40.img.avito.st", "41.img.avito.st", "42.img.avito.st", "43.img.avito.st",
        "44.img.avito.st", "45.img.avito.st", "46.img.avito.st", "47.img.avito.st",
        "48.img.avito.st", "49.img.avito.st", "50.img.avito.st", "51.img.avito.st",
        "52.img.avito.st", "53.img.avito.st", "54.img.avito.st", "55.img.avito.st",
        "56.img.avito.st", "57.img.avito.st", "58.img.avito.st", "59.img.avito.st",
        "60.img.avito.st", "61.img.avito.st", "62.img.avito.st", "63.img.avito.st",
        "64.img.avito.st", "65.img.avito.st", "66.img.avito.st", "67.img.avito.st",
        "68.img.avito.st", "69.img.avito.st", "70.img.avito.st", "71.img.avito.st",
        "72.img.avito.st", "73.img.avito.st", "74.img.avito.st", "742231.ms.ok.ru",
        "75.img.avito.st", "76.img.avito.st", "77.img.avito.st", "78.img.avito.st",
        "79.img.avito.st", "80.img.avito.st", "81.img.avito.st", "82.img.avito.st",
        "83.img.avito.st", "84.img.avito.st", "85.img.avito.st", "86.img.avito.st",
        "87.img.avito.st", "88.img.avito.st", "89.img.avito.st", "8mar.mail.ru", "8march.mail.ru",
        "90.img.avito.st", "91.img.avito.st", "92.img.avito.st", "93.img.avito.st",
        "94.img.avito.st", "95.img.avito.st", "96.img.avito.st", "97.img.avito.st",
        "98.img.avito.st", "99.img.avito.st", "9may.mail.ru", "a.auth-nsdi.ru", "a.res-nsdi.ru",
        "a.wb.ru", "aa.mail.ru", "ad.adriver.ru", "ad.mail.ru", "adm.digital.gov.ru",
        "adm.mp.rzd.ru", "admin.cs7777.vk.ru", "admin.tau.vk.ru", "ads.vk.ru", "adv.ozon.ru",
        "afisha.mail.ru", "agent.mail.ru", "akashi.vk-portal.net", "alfabank.ru",
        "alfabank.servicecdn.ru", "alfabank.st", "alpha3.minigames.mail.ru",
        "alpha4.minigames.mail.ru", "amigo.mail.ru", "ams2-cdn.2gis.com", "an.yandex.ru",
        "analytics.predict.mail.ru", "analytics.vk.ru", "answer.mail.ru", "answers.mail.ru",
        "api-maps.yandex.ru", "api.2gis.ru", "api.a.mts.ru", "api.apteka.ru", "api.avito.ru",
        "api.browser.yandex.com", "api.browser.yandex.ru", "api.cs7777.vk.ru",
        "api.events.plus.yandex.net", "api.expf.ru", "api.max.ru", "api.mindbox.ru", "api.ok.ru",
        "api.photo.2gis.com", "api.plus.kinopoisk.ru", "api.predict.mail.ru",
        "api.reviews.2gis.com", "api.s3.yandex.net", "api.tau.vk.ru", "api.uxfeedback.yandex.net",
        "api.vk.ru", "api2.ivi.ru", "apps.research.mail.ru", "authdl.mail.ru", "auto.mail.ru",
        "auto.ru", "autodiscover.corp.mail.ru", "autodiscover.ord.ozon.ru", "av.mail.ru",
        "avatars.mds.yandex.com", "avatars.mds.yandex.net", "avito.ru", "avito.st", "aw.mail.ru",
        "away.cs7777.vk.ru", "away.tau.vk.ru", "azt.mail.ru", "b.auth-nsdi.ru", "b.res-nsdi.ru",
        "bank.ozon.ru", "banners-website.wildberries.ru", "bb.mail.ru", "bd.mail.ru",
        "beeline.api.flocktory.com", "beko.dom.mail.ru", "bender.mail.ru", "beta.mail.ru",
        "bfds.sberbank.ru", "bitva.mail.ru", "biz.mail.ru", "blackfriday.mail.ru", "blog.mail.ru",
        "bot.gosuslugi.ru", "botapi.max.ru", "bratva-mr.mail.ru", "bro-bg-store.s3.yandex.com",
        "bro-bg-store.s3.yandex.net", "bro-bg-store.s3.yandex.ru", "brontp-pre.yandex.ru",
        "browser.mail.ru", "browser.yandex.com", "browser.yandex.ru", "business.vk.ru",
        "c.dns-shop.ru", "c.rdrom.ru", "calendar.mail.ru", "capsula.mail.ru", "cargo.rzd.ru",
        "cars.mail.ru", "catalog.api.2gis.com", "cdn.connect.mail.ru", "cdn.gpb.ru",
        "cdn.lemanapro.ru", "cdn.newyear.mail.ru", "cdn.rosbank.ru", "cdn.s3.yandex.net",
        "cdn.tbank.ru", "cdn.uxfeedback.ru", "cdn.yandex.ru", "cdn1.tu-tu.ru", "cdnn21.img.ria.ru",
        "cdnrhkgfkkpupuotntfj.svc.cdn.yandex.net", "cf.mail.ru", "chat-ct.pochta.ru",
        "chat-prod.wildberries.ru", "chat3.vtb.ru", "cloud.cdn.yandex.com", "cloud.cdn.yandex.net",
        "cloud.cdn.yandex.ru", "cloud.mail.ru", "cloud.vk.com", "cloud.vk.ru",
        "cloudcdn-ams19.cdn.yandex.net", "cloudcdn-m9-10.cdn.yandex.net",
        "cloudcdn-m9-12.cdn.yandex.net", "cloudcdn-m9-13.cdn.yandex.net",
        "cloudcdn-m9-14.cdn.yandex.net", "cloudcdn-m9-15.cdn.yandex.net",
        "cloudcdn-m9-2.cdn.yandex.net", "cloudcdn-m9-3.cdn.yandex.net",
        "cloudcdn-m9-4.cdn.yandex.net", "cloudcdn-m9-5.cdn.yandex.net",
        "cloudcdn-m9-6.cdn.yandex.net", "cloudcdn-m9-7.cdn.yandex.net",
        "cloudcdn-m9-9.cdn.yandex.net", "cm.a.mts.ru", "cms-res-web.online.sberbank.ru",
        "cobma.mail.ru", "cobmo.mail.ru", "cobrowsing.tbank.ru", "code.mail.ru",
        "codefest.mail.ru", "cog.mail.ru", "collections.yandex.com", "collections.yandex.ru",
        "comba.mail.ru", "combu.mail.ru", "commba.mail.ru", "company.rzd.ru", "compute.mail.ru",
        "connect.cs7777.vk.ru", "contacts.rzd.ru", "contract.gosuslugi.ru", "corp.mail.ru",
        "counter.yadro.ru", "cpa.hh.ru", "cpg.money.mail.ru", "crazypanda.mail.ru",
        "crowdtest.payment-widget-smarttv.plus.tst.kinopoisk.ru",
        "crowdtest.payment-widget.plus.tst.kinopoisk.ru", "cs.avito.ru", "cs7777.vk.ru",
        "csp.yandex.net", "ctlog.mail.ru", "ctlog2023.mail.ru", "ctlog2024.mail.ru", "cto.mail.ru",
        "cups.mail.ru", "d-assets.2gis.ru", "d5de4k0ri8jba7ucdbt6.apigw.yandexcloud.net",
        "da-preprod.biz.mail.ru", "da.biz.mail.ru", "data.amigo.mail.ru", "dating.ok.ru",
        "deti.mail.ru", "dev.cs7777.vk.ru", "dev.max.ru", "dev.tau.vk.ru", "dev1.mail.ru",
        "dev2.mail.ru", "dev3.mail.ru", "digital.gov.ru", "disk.2gis.com", "disk.rzd.ru",
        "dk.mail.ru", "dl.mail.ru", "dl.marusia.mail.ru", "dmp.dmpkit.lemanapro.ru", "dn.mail.ru",
        "dnd.wb.ru", "dobro.mail.ru", "doc.mail.ru", "dom.mail.ru", "download.max.ru",
        "dr.yandex.net", "dr2.yandex.net", "dragonpals.mail.ru", "ds.mail.ru", "duck.mail.ru",
        "duma.gov.ru", "dzen.ru", "e.mail.ru", "education.mail.ru", "egress.yandex.net",
        "eh.vk.com", "ekmp-a-51.rzd.ru", "enterprise.api-maps.yandex.ru", "epp.genproc.gov.ru",
        "esa-res.online.sberbank.ru", "esc.predict.mail.ru", "esia.gosuslugi.ru", "et.mail.ru",
        "expert.vk.ru", "external-api.mediabilling.kinopoisk.ru", "external-api.plus.kinopoisk.ru",
        "eye.targetads.io", "favicon.yandex.com", "favicon.yandex.net", "favicon.yandex.ru",
        "favorites.api.2gis.com", "fb-cdn.premier.one", "fe.mail.ru", "filekeeper-vod.2gis.com",
        "finance.mail.ru", "finance.wb.ru", "five.predict.mail.ru", "foto.mail.ru",
        "frontend.vh.yandex.ru", "fw.wb.ru", "games-bamboo.mail.ru", "games-fisheye.mail.ru",
        "games.mail.ru", "gazeta.ru", "genesis.mail.ru", "geo-apart.predict.mail.ru",
        "get4click.ru", "gibdd.mail.ru", "go.mail.ru", "golos.mail.ru", "gosuslugi.ru",
        "gosweb.gosuslugi.ru", "government.ru", "goya.rutube.ru", "gpb.finance.mail.ru",
        "graphql-web.kinopoisk.ru", "graphql.kinopoisk.ru", "gu-st.ru", "guns.mail.ru",
        "hb-bidder.skcrtxr.com", "hd.kinopoisk.ru", "health.mail.ru", "help.max.ru",
        "help.mcs.mail.ru", "hh.ru", "hhcdn.ru", "hi-tech.mail.ru", "horo.mail.ru", "hrc.tbank.ru",
        "hs.mail.ru", "http-check-headers.yandex.ru", "i.hh.ru", "i.max.ru", "i.rdrom.ru",
        "i0.photo.2gis.com", "i1.photo.2gis.com", "i2.photo.2gis.com", "i3.photo.2gis.com",
        "i4.photo.2gis.com", "i5.photo.2gis.com", "i6.photo.2gis.com", "i7.photo.2gis.com",
        "i8.photo.2gis.com", "i9.photo.2gis.com", "id.cs7777.vk.ru", "id.sber.ru", "id.tau.vk.ru",
        "id.tbank.ru", "id.vk.ru", "identitystatic.mts.ru", "images.apteka.ru",
        "imgproxy.cdn-tinkoff.ru", "imperia.mail.ru", "informer.yandex.ru", "infra.mail.ru",
        "internet.mail.ru", "invest.ozon.ru", "io.ozone.ru", "ir.ozone.ru", "it.mail.ru",
        "izbirkom.ru", "jam.api.2gis.com", "jd.mail.ru", "jitsi.wb.ru", "journey.mail.ru",
        "jsons.injector.3ebra.net", "juggermobile.mail.ru", "junior.mail.ru", "keys.api.2gis.com",
        "kicker.mail.ru", "kiks.yandex.com", "kiks.yandex.ru", "kingdomrift.mail.ru",
        "kino.mail.ru", "knights.mail.ru", "kobma.mail.ru", "kobmo.mail.ru", "komba.mail.ru",
        "kombo.mail.ru", "kombu.mail.ru", "kommba.mail.ru", "konflikt.mail.ru", "kp.ru",
        "kremlin.ru", "kz.mcs.mail.ru", "la.mail.ru", "lady.mail.ru", "landing.mail.ru",
        "le.tbank.ru", "learning.ozon.ru", "legal.max.ru", "legenda.mail.ru",
        "legendofheroes.mail.ru", "lemanapro.ru", "lenta.ru", "link.max.ru", "link.mp.rzd.ru",
        "live.ok.ru", "lk.gosuslugi.ru", "loa.mail.ru", "log.strm.yandex.ru", "login.cs7777.vk.ru",
        "login.mts.ru", "login.tau.vk.ru", "login.vk.com", "login.vk.ru", "lotro.mail.ru",
        "love.mail.ru", "m.47news.ru", "m.avito.ru", "m.cs7777.vk.ru", "m.ok.ru", "m.tau.vk.ru",
        "m.vk.ru", "m.vkvideo.cs7777.vk.ru", "ma.kinopoisk.ru", "magnit-ru.injector.3ebra.net",
        "mail.yandex.com", "mail.yandex.ru", "mailer.mail.ru", "mailexpress.mail.ru",
        "man.mail.ru", "map.gosuslugi.ru", "mapgl.2gis.com", "mapi.learning.ozon.ru",
        "maps.mail.ru", "market.rzd.ru", "marusia.mail.ru", "max.ru", "mc.yandex.com",
        "mc.yandex.ru", "mcs.mail.ru", "mddc.tinkoff.ru", "me.cs7777.vk.ru", "media-golos.mail.ru",
        "media.mail.ru", "mediafeeds.yandex.com", "mediafeeds.yandex.ru", "mediapro.mail.ru",
        "merch-cpg.money.mail.ru", "metrics.alfabank.ru", "microapps.kinopoisk.ru",
        "miniapp.internal.myteam.mail.ru", "minigames.mail.ru", "mkb.ru", "mking.mail.ru",
        "mobfarm.mail.ru", "money.mail.ru", "moscow.megafon.ru", "moskva.beeline.ru",
        "moskva.taximaxim.ru", "mosqa.mail.ru", "mowar.mail.ru", "mozilla.mail.ru", "mp.rzd.ru",
        "ms.cs7777.vk.ru", "msk.t2.ru", "mtscdn.ru", "multitest.ok.ru", "music.vk.ru",
        "my.mail.ru", "my.rzd.ru", "myteam.mail.ru", "nebogame.mail.ru", "net.mail.ru",
        "neuro.translate.yandex.ru", "new.mail.ru", "news.mail.ru", "newyear.mail.ru",
        "newyear2018.mail.ru", "nonstandard.sales.mail.ru", "notes.mail.ru",
        "novorossiya.gosuslugi.ru", "nspk.ru", "oauth.cs7777.vk.ru", "oauth.tau.vk.ru",
        "oauth2.cs7777.vk.ru", "octavius.mail.ru", "ok.ru", "oneclick-payment.kinopoisk.ru",
        "online.sberbank.ru", "operator.mail.ru", "ord.ozon.ru", "ord.vk.ru", "otvet.mail.ru",
        "otveti.mail.ru", "otvety.mail.ru", "owa.ozon.ru", "ozon.ru", "ozone.ru", "panzar.mail.ru",
        "park.mail.ru", "partners.gosuslugi.ru", "partners.lemanapro.ru", "passport.pochta.ru",
        "pay.mail.ru", "pay.ozon.ru", "payment-widget-smarttv.plus.kinopoisk.ru",
        "payment-widget.kinopoisk.ru", "payment-widget.plus.kinopoisk.ru", "pernatsk.mail.ru",
        "personalization-web-stable.mindbox.ru", "pets.mail.ru", "pic.rutubelist.ru", "pikabu.ru",
        "pl-res.online.sberbank.ru", "pms.mail.ru", "pochta.ru", "pochtabank.mail.ru",
        "pogoda.mail.ru", "pokerist.mail.ru", "polis.mail.ru", "pos.gosuslugi.ru", "pp.mail.ru",
        "pptest.userapi.com", "predict.mail.ru", "preview.rutube.ru", "primeworld.mail.ru",
        "privacy-cs.mail.ru", "prodvizhenie.rzd.ru", "ptd.predict.mail.ru", "pubg.mail.ru",
        "public-api.reviews.2gis.com", "public.infra.mail.ru", "pulse.mail.ru", "pulse.mp.rzd.ru",
        "push.vk.ru", "pw.mail.ru", "px.adhigh.net", "quantum.mail.ru", "queuev4.vk.com",
        "quiz.kinopoisk.ru", "r.vk.ru", "r0.mradx.net", "rambler.ru", "rap.skcrtxr.com",
        "rate.mail.ru", "rbc.ru", "rebus.calls.mail.ru", "rebus.octavius.mail.ru",
        "receive-sentry.lmru.tech", "reseach.mail.ru", "restapi.dns-shop.ru", "rev.mail.ru",
        "riot.mail.ru", "rl.mail.ru", "rm.mail.ru", "rs.mail.ru", "rt.api.operator.mail.ru",
        "rutube.ru", "rzd.ru", "s.rbk.ru", "s.vtb.ru", "s0.bss.2gis.com", "s1.bss.2gis.com",
        "s11.auto.drom.ru", "s3.babel.mail.ru", "s3.mail.ru", "s3.media-mobs.mail.ru", "s3.t2.ru",
        "s3.yandex.net", "sales.mail.ru", "sangels.mail.ru", "sba.yandex.com", "sba.yandex.net",
        "sba.yandex.ru", "sberbank.ru", "scitylana.apteka.ru", "sdk.money.mail.ru",
        "secure-cloud.rzd.ru", "secure.rzd.ru", "securepay.ozon.ru", "security.mail.ru",
        "seller.ozon.ru", "sentry.hh.ru", "service.amigo.mail.ru", "servicepipe.ru",
        "serving.a.mts.ru", "sfd.gosuslugi.ru", "shadowbound.mail.ru", "sntr.avito.ru",
        "socdwar.mail.ru", "sochi-park.predict.mail.ru", "souz.mail.ru", "speller.yandex.net",
        "sphere.mail.ru", "splitter.wb.ru", "sport.mail.ru", "sso-app4.vtb.ru", "sso-app5.vtb.ru",
        "sso.auto.ru", "sso.dzen.ru", "sso.kinopoisk.ru", "ssp.rutube.ru", "st-gismeteo.st",
        "st-im.kinopoisk.ru", "st-ok.cdn-vk.ru", "st.avito.ru", "st.gismeteo.st",
        "st.kinopoisk.ru", "st.max.ru", "st.okcdn.ru", "st.ozone.ru",
        "staging-analytics.predict.mail.ru", "staging-esc.predict.mail.ru",
        "staging-sochi-park.predict.mail.ru", "stand.aoc.mail.ru", "stand.bb.mail.ru",
        "stand.cb.mail.ru", "stand.la.mail.ru", "stand.pw.mail.ru", "startrek.mail.ru",
        "stat-api.gismeteo.net", "statad.ru", "static-mon.yandex.net", "static.apteka.ru",
        "static.beeline.ru", "static.dl.mail.ru", "static.lemanapro.ru", "static.operator.mail.ru",
        "static.rutube.ru", "stats.avito.ru", "stats.vk-portal.net", "status.mcs.mail.ru",
        "storage.ape.yandex.net", "storage.yandexcloud.net", "stormriders.mail.ru",
        "stream.mail.ru", "street-combats.mail.ru", "strm-rad-23.strm.yandex.net",
        "strm-spbmiran-07.strm.yandex.net", "strm-spbmiran-08.strm.yandex.net", "strm.yandex.net",
        "strm.yandex.ru", "styles.api.2gis.com", "suggest.dzen.ru", "suggest.sso.dzen.ru",
        "sun6-20.userapi.com", "sun6-21.userapi.com", "sun6-22.userapi.com",
        "sun9-101.userapi.com", "sun9-38.userapi.com", "support.biz.mail.ru",
        "support.mcs.mail.ru", "support.tech.mail.ru", "surveys.yandex.ru",
        "sync.browser.yandex.net", "sync.rambler.ru", "tag.a.mts.ru", "tamtam.ok.ru",
        "target.smi2.net", "target.vk.ru", "team.mail.ru", "team.rzd.ru", "tech.mail.ru",
        "tech.vk.ru", "tera.mail.ru", "ticket.rzd.ru", "tickets.widget.kinopoisk.ru",
        "tidaltrek.mail.ru", "tile0.maps.2gis.com", "tile1.maps.2gis.com", "tile2.maps.2gis.com",
        "tile3.maps.2gis.com", "tile4.maps.2gis.com", "tiles.maps.mail.ru", "tmgame.mail.ru",
        "tmsg.tbank.ru", "tns-counter.ru", "todo.mail.ru", "top-fwz1.mail.ru",
        "touch.kinopoisk.ru", "townwars.mail.ru", "travel.rzd.ru", "travel.yandex.ru",
        "travel.yastatic.net", "trk.mail.ru", "ttbh.mail.ru", "tutu.ru", "tv.mail.ru",
        "typewriter.mail.ru", "u.corp.mail.ru", "ufo.mail.ru", "ui.cs7777.vk.ru", "ui.tau.vk.ru",
        "user-geo-data.wildberries.ru", "uslugi.yandex.ru", "uxfeedback-cdn.s3.yandex.net",
        "uxfeedback.yandex.ru", "vk-portal.net", "vk.com", "vk.mail.ru", "vkdoc.mail.ru",
        "vkvideo.cs7777.vk.ru", "voina.mail.ru", "voter.gosuslugi.ru", "vt-1.ozone.ru",
        "wap.yandex.com", "wap.yandex.ru", "warface.mail.ru", "warheaven.mail.ru",
        "wartune.mail.ru", "wb.ru", "wcm.weborama-tech.ru", "web-static.mindbox.ru", "web.max.ru",
        "webagent.mail.ru", "weblink.predict.mail.ru", "webstore.mail.ru", "welcome.mail.ru",
        "welcome.rzd.ru", "wf.mail.ru", "wh-cpg.money.mail.ru", "whatsnew.mail.ru",
        "widgets.cbonds.ru", "widgets.kinopoisk.ru", "wok.mail.ru", "wos.mail.ru",
        "ws-api.oneme.ru", "ws.seller.ozon.ru", "www.avito.ru", "www.avito.st", "www.biz.mail.ru",
        "www.cikrf.ru", "www.drive2.ru", "www.drom.ru", "www.farpost.ru", "www.gazprombank.ru",
        "www.gosuslugi.ru", "www.ivi.ru", "www.kinopoisk.ru", "www.kp.ru", "www.magnit.com",
        "www.mail.ru", "www.mcs.mail.ru", "www.open.ru", "www.ozon.ru", "www.pochta.ru",
        "www.psbank.ru", "www.pubg.mail.ru", "www.raiffeisen.ru", "www.rbc.ru", "www.rzd.ru",
        "www.sberbank.ru", "www.t2.ru", "www.tbank.ru", "www.tutu.ru", "www.unicreditbank.ru",
        "www.vtb.ru", "www.wf.mail.ru", "www.wildberries.ru", "www.x5.ru", "xapi.ozon.ru",
        "xn--80ajghhoc2aj1c8b.xn--p1ai", "ya.ru", "yabro-wbplugin.edadeal.yandex.ru",
        "yabs.yandex.ru", "yandex.com", "yandex.net", "yandex.ru", "yastatic.net", "yummy.drom.ru",
        "zen-yabro-morda.mediascope.mc.yandex.ru", "zen.yandex.com", "zen.yandex.net",
        "zen.yandex.ru", "честныйзнак.рф",
    ]

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
            content = re.sub(
                r"(vmess|vless|trojan|ss|ssr|tuic|hysteria|hysteria2)://",
                r"\n\1://",
                content,
            )
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
            data = re.sub(
                r"(vmess|vless|trojan|ss|ssr|tuic|hysteria|hysteria2)://",
                r"\n\1://",
                data,
            )
            configs = [
                line.strip()
                for line in data.splitlines()
                if line.strip() and not line.startswith("#")
            ]
        except Exception as e:
            log(f"⚠️ Ошибка при загрузке ({url}): {_format_fetch_error(e)}")
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
