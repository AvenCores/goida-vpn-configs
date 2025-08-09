import os
import requests
import urllib.parse
import urllib3
from github import Github
from github import GithubException
from datetime import datetime
import zoneinfo
import concurrent.futures
import threading
import re
from collections import defaultdict

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
    "https://raw.githubusercontent.com/miladtahanian/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt", #15
    "https://github.com/freefq/free/raw/refs/heads/master/v2", #16
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt", #17
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt", #18
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix", #19
    "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt", #20
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt", #21
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri", #22
    "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet.txt", #23
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS#STR.BYPASS%F0%9F%91%BE", #24
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs.txt", #25
]

# Пути для сохранения файлов локально и в репозитории
REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]

# Отключаем предупреждения, если будем использовать verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UA Chrome 124 (Windows 10 x64)
CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)


# Функция для скачивания данных по URL
def fetch_data(url: str, timeout: int = 10, max_attempts: int = 3) -> str:
    """Пытается скачать данные по URL, делая несколько попыток.

    Логика попыток:
    1. Первая попытка — как есть (verify=True).
    2. Вторая попытка — verify=False (игнорируем SSL-сертификат).
    3. Третья попытка — меняем протокол https → http и verify=False.
    """

    headers = {"User-Agent": CHROME_UA}

    for attempt in range(1, max_attempts + 1):
        try:
            # Определяем параметры для конкретной попытки
            modified_url = url
            verify = True

            if attempt == 2:
                # Попытка 2: отключаем проверку сертификата
                verify = False
            elif attempt == 3:
                # Попытка 3: пробуем http вместо https
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https":
                    modified_url = parsed._replace(scheme="http").geturl()
                verify = False

            response = requests.get(modified_url, timeout=timeout, verify=verify, headers=headers)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as exc:
            last_exc = exc  # запоминаем последнюю ошибку
            # Если не последняя попытка — пробуем ещё раз
            if attempt < max_attempts:
                continue
            # Если все попытки исчерпаны — пробрасываем исключение
            raise last_exc

# Сохраняет полученные данные в локальный файл
def save_to_local_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    log(f"📁 Данные сохранены локально в {path}")

# Загружает файл в репозиторий GitHub (обновляет или создаёт новый)
def upload_to_github(local_path, remote_path):
    """Загружает или обновляет файл в репозитории GitHub.

    1. Если файл отсутствует – создаёт его.
    2. Если файл уже есть и содержимое изменилось – обновляет его.
    3. Если изменений нет – пропускает загрузку.
    """

    # Проверка наличия локального файла
    if not os.path.exists(local_path):
        log(f"❌ Файл {local_path} не найден.")
        return

    # Используем уже созданный объект репозитория
    repo = REPO

    # Чтение содержимого локального файла
    with open(local_path, "r", encoding="utf-8") as file:
        content = file.read()

    try:
        # Пытаемся получить файл из репозитория
        file_in_repo = repo.get_contents(remote_path)

        # Получаем содержимое удалённого файла, если возможно
        remote_content = None
        if getattr(file_in_repo, "encoding", None) == "base64":
            try:
                remote_content = file_in_repo.decoded_content.decode("utf-8")
            except Exception:
                remote_content = None

        # Обновляем файл, только если содержимое изменилось
        if remote_content is None or remote_content != content:
            # Добавляем название файла (например, 1.txt) в сообщение коммита
            basename = os.path.basename(remote_path)
            repo.update_file(
                path=remote_path,
                message=f"🚀 Обновление {basename} по часовому поясу Европа/Москва: {offset}",
                content=content,
                sha=file_in_repo.sha
            )
            log(f"🚀 Файл {remote_path} обновлён в репозитории.")
        else:
            log(f"🔄 Изменений для {remote_path} нет.")
    except GithubException as e:
        if e.status == 404:
            # Файл не найден – создаём новый
            basename = os.path.basename(remote_path)
            repo.create_file(
                path=remote_path,
                message=f"🆕 Первый коммит {basename} по часовому поясу Европа/Москва: {offset}",
                content=content
            )
            log(f"🆕 Файл {remote_path} создан.")
        else:
            # Любая другая ошибка
            log(f"⚠️ Ошибка при загрузке {remote_path}: {e.data.get('message', e)}")

# Функция для параллельного скачивания и сохранения файла
def download_and_save(idx):
    url = URLS[idx]
    local_path = LOCAL_PATHS[idx]
    try:
        data = fetch_data(url)
        save_to_local_file(local_path, data)
        return local_path, REMOTE_PATHS[idx]
    except Exception as e:
        short_msg = str(e)
        if len(short_msg) > 200:
            short_msg = short_msg[:200] + "…"
        log(f"⚠️ Ошибка при скачивании {url}: {short_msg}")
        return None

# Основная функция: скачивает, сохраняет и загружает все конфиги
def main():
    # Параллельно скачиваем файлы и сохраняем их локально
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(URLS))) as executor:
        futures = [executor.submit(download_and_save, i) for i in range(len(URLS))]

        # По мере завершения скачивания — загружаем файл в GitHub
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                local_path, remote_path = result
                upload_to_github(local_path, remote_path)

    # -------------------- ПЕЧАТЬ СОБРАННЫХ ЛОГОВ --------------------
    ordered_keys = sorted(k for k in LOGS_BY_FILE.keys() if k != 0)

    output_lines: list[str] = []

    # Сначала выводим логи по конкретным файлам в порядке номера
    for k in ordered_keys:
        output_lines.append(f"----- {k}.txt -----")
        output_lines.extend(LOGS_BY_FILE[k])

    # Далее выводим общие/непривязанные сообщения (ключ 0)
    if LOGS_BY_FILE.get(0):
        output_lines.append("----- Общие сообщения -----")
        output_lines.extend(LOGS_BY_FILE[0])

    print("\n".join(output_lines))

# Точка входа в программу
if __name__ == "__main__":
    main()
