import os
import requests
from github import Github
from datetime import datetime
import zoneinfo

# Определение времени по МСК
zone = zoneinfo.ZoneInfo("Europe/Moscow")
thistime = datetime.now(zone)
offset = thistime.strftime("%Y-%m-%d | %H:%M:%S")

GITHUB_TOKEN = os.environ.get("MY_TOKEN")  # GitHub токен
REPO_NAME_1 = "AvenCores/goida-vpn-configs"  # Репозиторий для основных файлов

# Если локальная папка не существует, создаём её
if not os.path.exists("githubmirror"):
    os.mkdir("githubmirror")

# Список URL и локальных/удалённых путей
URLS = [
    "https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality",
    "https://istanbulsydneyhotel.com/blogs/site/sni.php",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt",
    "https://hideshots.eu/sub.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://shadowmere.xyz/api/b64sub/",
    "https://vpn.fail/free-proxy/v2ray",
    "https://raw.githubusercontent.com/Proxydaemitelegram/Proxydaemi44/refs/heads/main/Proxydaemi44",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/mixed",
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY.txt",
]

REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_to_local_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {path}")


def upload_to_github(local_path, remote_path):
    if not os.path.exists(local_path):
        print(f"Файл {local_path} не найден.")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)

    with open(local_path, "r", encoding="utf-8") as file:
        content = file.read()

    try:
        file_in_repo = repo.get_contents(remote_path)
        repo.update_file(
            path=remote_path,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {remote_path} обновлён.")
    except Exception:
        repo.create_file(
            path=remote_path,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {remote_path} создан.")


def main():
    try:
        for url, local_path, remote_path in zip(URLS, LOCAL_PATHS, REMOTE_PATHS):
            data = fetch_data(url)
            save_to_local_file(local_path, data)
            upload_to_github(local_path, remote_path)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
