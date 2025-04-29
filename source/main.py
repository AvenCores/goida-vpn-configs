import os
import requests
from github import Github
from datetime import datetime
import zoneinfo

# Определение времени по МСК
zone = zoneinfo.ZoneInfo("Europe/Moscow")
thistime = datetime.now(zone)
offset = thistime.strftime("%Y-%m-%d | %H:%M:%S")

GITHUB_TOKEN = "" # GitHub токен
REPO_NAME_1 = ""  # Репозиторий для основных файлов

# Если локальная папка не существует, создаём её
if not os.path.exists("githubmirror"):
    os.mkdir("githubmirror")

# URL и пути для файлов (в репозитории файлы будут лежать в папке githubmirror)
URL1 = "https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality"
REMOTE_FILE_PATH1 = "githubmirror/1.txt"  
LOCAL_FILE_PATH1 = "githubmirror/1.txt"

URL2 = "https://istanbulsydneyhotel.com/blogs/site/sni.php"
REMOTE_FILE_PATH2 = "githubmirror/2.txt"
LOCAL_FILE_PATH2 = "githubmirror/2.txt"

URL3 = "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt"
REMOTE_FILE_PATH3 = "githubmirror/3.txt"
LOCAL_FILE_PATH3 = "githubmirror/3.txt"

URL4 = "https://xray.abvpn.ru/vless/588f094b-431b-422c-b80b-007945037072/6542271205.json#abvpn"
REMOTE_FILE_PATH4 = "githubmirror/4.txt"
LOCAL_FILE_PATH4 = "githubmirror/4.txt"

URL5 = "https://hideshots.eu/sub.txt"
REMOTE_FILE_PATH5 = "githubmirror/5.txt"
LOCAL_FILE_PATH5 = "githubmirror/5.txt"

URL6 = "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt"
REMOTE_FILE_PATH6 = "githubmirror/6.txt"
LOCAL_FILE_PATH6 = "githubmirror/6.txt"

URL7 = "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt"
REMOTE_FILE_PATH7 = "githubmirror/7.txt"
LOCAL_FILE_PATH7 = "githubmirror/7.txt"

URL8 = "https://shadowmere.xyz/api/b64sub/"
REMOTE_FILE_PATH8 = "githubmirror/8.txt"
LOCAL_FILE_PATH8 = "githubmirror/8.txt"

URL9 = "https://vpn.fail/free-proxy/v2ray"
REMOTE_FILE_PATH9 = "githubmirror/9.txt"
LOCAL_FILE_PATH9 = "githubmirror/9.txt"

URL10 = "https://raw.githubusercontent.com/Proxydaemitelegram/Proxydaemi44/refs/heads/main/Proxydaemi44"
REMOTE_FILE_PATH10 = "githubmirror/10.txt"
LOCAL_FILE_PATH10 = "githubmirror/10.txt"

# Функции для обработки 10 URL
def fetch_data():
    response = requests.get(URL1)
    response.raise_for_status()
    return response.text

def save_to_local_file(content):
    with open(LOCAL_FILE_PATH1, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH1}")

def upload_to_github():
    if not os.path.exists(LOCAL_FILE_PATH1):
        print(f"Файл {LOCAL_FILE_PATH1} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH1, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH1)
        repo.update_file(
            path=REMOTE_FILE_PATH1,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH1} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH1,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH1} создан.")

def fetch_data1():
    response = requests.get(URL2)
    response.raise_for_status()
    return response.text

def save_to_local_file1(content):
    with open(LOCAL_FILE_PATH2, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH2}")

def upload_to_github1():
    if not os.path.exists(LOCAL_FILE_PATH2):
        print(f"Файл {LOCAL_FILE_PATH2} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH2, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH2)
        repo.update_file(
            path=REMOTE_FILE_PATH2,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH2} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH2,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH2} создан.")

def fetch_data2():
    response = requests.get(URL3)
    response.raise_for_status()
    return response.text

def save_to_local_file2(content):
    with open(LOCAL_FILE_PATH3, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH3}")

def upload_to_github2():
    if not os.path.exists(LOCAL_FILE_PATH3):
        print(f"Файл {LOCAL_FILE_PATH3} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH3, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH3)
        repo.update_file(
            path=REMOTE_FILE_PATH3,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH3} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH3,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH3} создан.")

def fetch_data3():
    response = requests.get(URL4)
    response.raise_for_status()
    return response.text

def save_to_local_file3(content):
    with open(LOCAL_FILE_PATH4, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH4}")

def upload_to_github3():
    if not os.path.exists(LOCAL_FILE_PATH4):
        print(f"Файл {LOCAL_FILE_PATH4} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH4, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH4)
        repo.update_file(
            path=REMOTE_FILE_PATH4,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH4} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH4,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH4} создан.")

def fetch_data4():
    response = requests.get(URL5)
    response.raise_for_status()
    return response.text

def save_to_local_file4(content):
    with open(LOCAL_FILE_PATH5, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH5}")

def upload_to_github4():
    if not os.path.exists(LOCAL_FILE_PATH5):
        print(f"Файл {LOCAL_FILE_PATH5} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH5, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH5)
        repo.update_file(
            path=REMOTE_FILE_PATH5,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH5} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH5,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH5} создан.")

def fetch_data5():
    response = requests.get(URL6)
    response.raise_for_status()
    return response.text

def save_to_local_file5(content):
    with open(LOCAL_FILE_PATH6, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH6}")

def upload_to_github5():
    if not os.path.exists(LOCAL_FILE_PATH6):
        print(f"Файл {LOCAL_FILE_PATH6} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH6, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH6)
        repo.update_file(
            path=REMOTE_FILE_PATH6,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH6} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH6,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH6} создан.")

def fetch_data6():
    response = requests.get(URL7)
    response.raise_for_status()
    return response.text

def save_to_local_file6(content):
    with open(LOCAL_FILE_PATH7, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH7}")

def upload_to_github6():
    if not os.path.exists(LOCAL_FILE_PATH7):
        print(f"Файл {LOCAL_FILE_PATH7} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH7, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH7)
        repo.update_file(
            path=REMOTE_FILE_PATH7,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH7} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH7,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH7} создан.")

def fetch_data7():
    response = requests.get(URL8)
    response.raise_for_status()
    return response.text

def save_to_local_file7(content):
    with open(LOCAL_FILE_PATH8, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH8}")

def upload_to_github7():
    if not os.path.exists(LOCAL_FILE_PATH8):
        print(f"Файл {LOCAL_FILE_PATH8} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH8, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH8)
        repo.update_file(
            path=REMOTE_FILE_PATH8,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH8} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH8,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH8} создан.")

def fetch_data8():
    response = requests.get(URL9)
    response.raise_for_status()
    return response.text

def save_to_local_file8(content):
    with open(LOCAL_FILE_PATH9, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH9}")

def upload_to_github8():
    if not os.path.exists(LOCAL_FILE_PATH9):
        print(f"Файл {LOCAL_FILE_PATH9} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH9, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH9)
        repo.update_file(
            path=REMOTE_FILE_PATH9,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH9} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH9,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH9} создан.")

def fetch_data9():
    response = requests.get(URL10)
    response.raise_for_status()
    return response.text

def save_to_local_file9(content):
    with open(LOCAL_FILE_PATH10, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в {LOCAL_FILE_PATH10}")

def upload_to_github9():
    if not os.path.exists(LOCAL_FILE_PATH10):
        print(f"Файл {LOCAL_FILE_PATH10} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME_1)
    with open(LOCAL_FILE_PATH10, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(REMOTE_FILE_PATH10)
        repo.update_file(
            path=REMOTE_FILE_PATH10,
            message=f"Update time Europe/Moscow: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"Файл {REMOTE_FILE_PATH10} обновлён.")
    except Exception as e:
        repo.create_file(
            path=REMOTE_FILE_PATH10,
            message=f"Initial commit {offset}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH10} создан.")

#############################
# Главная функция: обработка всех файлов
#############################

def main():
    try:
        # Обработка 8 URL
        data = fetch_data()
        save_to_local_file(data)
        upload_to_github()

        data1 = fetch_data1()
        save_to_local_file1(data1)
        upload_to_github1()

        data2 = fetch_data2()
        save_to_local_file2(data2)
        upload_to_github2()

        data3 = fetch_data3()
        save_to_local_file3(data3)
        upload_to_github3()

        data4 = fetch_data4()
        save_to_local_file4(data4)
        upload_to_github4()

        data5 = fetch_data5()
        save_to_local_file5(data5)
        upload_to_github5()

        data6 = fetch_data6()
        save_to_local_file6(data6)
        upload_to_github6()

        data7 = fetch_data7()
        save_to_local_file7(data7)
        upload_to_github7()

        data8 = fetch_data8()
        save_to_local_file8(data8)
        upload_to_github8()

        data9 = fetch_data9()
        save_to_local_file9(data9)
        upload_to_github9()

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
