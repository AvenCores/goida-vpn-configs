import os
import urllib.parse
import threading
import re
from collections import defaultdict
import asyncio
import aiohttp
import hashlib
from github import InputGitTreeElement

# -------------------- ЛОГИРОВАНИЕ --------------------
# Собираем сообщения по каждому номеру файла, чтобы затем вывести их в порядке 1 → N

LOGS_BY_FILE: dict[int, list[str]] = defaultdict(list)
_LOG_LOCK = threading.Lock()


def _extract_index(msg: str) -> int:
    """Пытается извлечь номер файла из строки вида 'githubmirror/12.txt'.
    Если номер не найден, возвращает 0 (для общих сообщений)."""
    m = re.search(r"githubmirror/(\d+)\.txt", msg)
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
offset = thistime.strftime("%H:%M | %d.%m.%Y")  # Формат времени для коммитов

# Получение GitHub токена из переменных окружения
GITHUB_TOKEN = os.environ.get("MY_TOKEN")
# Имя репозитория для загрузки файлов
REPO_NAME = "AvenCores/goida-vpn-configs"

# Создаём объект Github и репозиторий один раз, чтобы не делать это при каждой загрузке
g = Github(GITHUB_TOKEN)
REPO = g.get_repo(REPO_NAME)

# Проверка и создание локальной папки для хранения файлов, если она отсутствует
if not os.path.exists("githubmirror"):
    os.mkdir("githubmirror")

# Список URL-адресов для скачивания конфигов
URLS = [
    "https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality", #1
    "https://istanbulsydneyhotel.com/blogs/site/sni.php", #2
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt", #3
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt", #4
    "https://raw.githubusercontent.com/AliDev-ir/FreeVPN/main/pcvpn", #5
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt", #6
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt", #7
    "https://raw.githubusercontent.com/YasserDivaR/pr0xy/main/mycustom1.txt", #8
    "https://vpn.fail/free-proxy/v2ray", #9
    "https://raw.githubusercontent.com/Proxydaemitelegram/Proxydaemi44/refs/heads/main/Proxydaemi44", #10
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt", #11
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all", #12
    "https://github.com/Kwinshadow/TelegramV2rayCollector/raw/refs/heads/main/sublinks/mix.txt", #13
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes", #14
    "https://github.com/4n0nymou3/multi-proxy-config-fetcher/raw/refs/heads/main/configs/proxy_configs.txt", #15
    "https://github.com/freefq/free/raw/refs/heads/master/v2", #16
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt", #17
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt", #18
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix", #19
    "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt", #20
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt", #21
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri", #22
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs.txt", #23
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS#STR.BYPASS%F0%9F%91%BE", #24
]

# Пути для сохранения файлов локально и в репозитории
REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]

# UA Chrome 124 (Windows 10 x64)
CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)

# -------------------- HTTP SESSION & REMOTE CACHE --------------------
try:
    _remote_contents = REPO.get_contents("githubmirror")
    REMOTE_CACHE = {f.path: f for f in _remote_contents}  # path -> ContentFile
except GithubException:
    REMOTE_CACHE = {}


def _git_blob_sha(content: str) -> str:
    """Вычисляет SHA1 так же, как это делает git для blob."""
    data = content.encode("utf-8")
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()

# -------------------- ASYNC ЗАГРУЗКА --------------------
async def _async_fetch(session: aiohttp.ClientSession, url: str, timeout: int = 10, max_attempts: int = 3) -> str:
    """Асинхронная версия fetch_data с тремя попытками."""
    for attempt in range(1, max_attempts + 1):
        try:
            modified_url = url
            verify_ssl = attempt == 1  # 1-я попытка — verify=True
            if attempt == 3:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https":
                    modified_url = parsed._replace(scheme="http").geturl()
                verify_ssl = False
            elif attempt == 2:
                verify_ssl = False

            async with session.get(modified_url, ssl=verify_ssl, timeout=timeout) as resp:
                resp.raise_for_status()
                return await resp.text()
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts:
                continue
            raise last_exc

async def _download_all() -> list:
    """Скачивает все URL асинхронно и возвращает список результатов (или исключений)."""
    connector = aiohttp.TCPConnector(limit=64, ssl=False)
    async with aiohttp.ClientSession(connector=connector, headers={"User-Agent": CHROME_UA}) as session:
        tasks = [asyncio.create_task(_async_fetch(session, url)) for url in URLS]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Сохраняет полученные данные в локальный файл
def save_to_local_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    log(f"📁 Данные сохранены локально в {path}")

# -------------------- BATCH COMMIT --------------------

def _batch_commit(changed: dict[str, str]):
    """Коммитит все изменённые файлы одним коммитом через GitTrees API."""
    if not changed:
        log("🔄 Нет изменений для коммита.")
        return

    elements: list[InputGitTreeElement] = []
    for path, content in changed.items():
        blob = REPO.create_git_blob(content, "utf-8")
        elements.append(InputGitTreeElement(path=path, mode="100644", type="blob", sha=blob.sha))

    # Базовый коммит/ветка
    branch_name = REPO.default_branch or "main"
    base_commit = REPO.get_branch(branch_name).commit
    base_tree = base_commit.commit.tree

    new_tree = REPO.create_git_tree(elements, base_tree)
    commit_msg = f"🚀 Batch update {len(changed)} files по часовому поясу Европа/Москва: {offset}"
    new_commit = REPO.create_git_commit(commit_msg, new_tree, [base_commit])
    REPO.get_git_ref(f"heads/{branch_name}").edit(new_commit.sha)
    log(f"🚀 Создан batch-коммит: {len(changed)} файлов.")

# -------------------- ОБНОВЛЁННАЯ main --------------------
async def _async_main():
    results = await _download_all()

    changed_files: dict[str, str] = {}

    for idx, result in enumerate(results):
        url = URLS[idx]
        if isinstance(result, Exception):
            short_msg = str(result)
            if len(short_msg) > 200:
                short_msg = short_msg[:200] + "…"
            log(f"⚠️ Ошибка при скачивании {url}: {short_msg}")
            continue

        content: str = result
        local_path = LOCAL_PATHS[idx]
        remote_path = REMOTE_PATHS[idx]

        save_to_local_file(local_path, content)

        # Проверяем по SHA, изменился ли файл
        new_sha = _git_blob_sha(content)
        remote_entry = REMOTE_CACHE.get(remote_path)
        if remote_entry and remote_entry.sha == new_sha:
            log(f"🔄 Изменений для {remote_path} нет (по SHA).")
            continue

        changed_files[remote_path] = content

    _batch_commit(changed_files)

    # ---- Печать логов ----
    ordered_keys = sorted(k for k in LOGS_BY_FILE.keys() if k != 0)
    output_lines: list[str] = []
    for k in ordered_keys:
        output_lines.append(f"----- {k}.txt -----")
        output_lines.extend(LOGS_BY_FILE[k])
    if LOGS_BY_FILE.get(0):
        output_lines.append("----- Общие сообщения -----")
        output_lines.extend(LOGS_BY_FILE[0])
    print("\n".join(output_lines))

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(_async_main())
