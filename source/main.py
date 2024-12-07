import os
import requests
from github import Github
from datetime import datetime

# Конфигурация
GITHUB_TOKEN = "" # github token https://github.com/settings/tokens
REPO_NAME = ""  # username/repo_name

URL1 = "https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality"
LOCAL_FILE_PATH1 = "one_file_vpn.txt"  # Локальный путь для сохранения файла
REMOTE_FILE_PATH1 = "one_file_vpn.txt"  # Путь файла в репозитории

URL2 = "https://istanbulsydneyhotel.com/blogs/site/sni.php"
LOCAL_FILE_PATH2 = "two_file_vpn.txt"  # Локальный путь для сохранения файла
REMOTE_FILE_PATH2 = "two_file_vpn.txt"  # Путь файла в репозитории

URL3 = "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt"
LOCAL_FILE_PATH3 = "three_file_vpn.txt"  # Локальный путь для сохранения файла
REMOTE_FILE_PATH3 = "three_file_vpn.txt"  # Путь файла в репозитории

def fetch_data():
    """Получение данных с указанного URL"""
    response = requests.get(URL1)
    response.raise_for_status()  # Проверка на ошибки
    return response.text

def save_to_local_file(content):
    """Сохранение данных в локальный файл"""
    with open(LOCAL_FILE_PATH1, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в файл {LOCAL_FILE_PATH1}")

def upload_to_github():
    """Загрузка локального файла в репозиторий GitHub"""
    if not os.path.exists(LOCAL_FILE_PATH1):
        print(f"Файл {LOCAL_FILE_PATH1} не найден. Завершение работы.")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Читаем содержимое локального файла
    with open(LOCAL_FILE_PATH1, "r", encoding="utf-8") as file:
        content = file.read()

    # Проверяем, существует ли файл в репозитории
    try:
        file = repo.get_contents(REMOTE_FILE_PATH1)
        repo.update_file(
            path=REMOTE_FILE_PATH1,
            message=f"Update data: {datetime.now().isoformat()}",
            content=content,
            sha=file.sha
        )
        print(f"Файл {REMOTE_FILE_PATH1} обновлён в репозитории.")
    except Exception as e:
        # Если файла нет, создаём новый
        repo.create_file(
            path=REMOTE_FILE_PATH1,
            message=f"Initial commit: {datetime.now().isoformat()}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH1} создан в репозитории.")



def fetch_data1():
    """Получение данных с указанного URL"""
    response = requests.get(URL2)
    response.raise_for_status()  # Проверка на ошибки
    return response.text

def save_to_local_file1(content):
    """Сохранение данных в локальный файл"""
    with open(LOCAL_FILE_PATH2, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в файл {LOCAL_FILE_PATH2}")

def upload_to_github1():
    """Загрузка локального файла в репозиторий GitHub"""
    if not os.path.exists(LOCAL_FILE_PATH2):
        print(f"Файл {LOCAL_FILE_PATH2} не найден. Завершение работы.")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Читаем содержимое локального файла
    with open(LOCAL_FILE_PATH2, "r", encoding="utf-8") as file:
        content = file.read()

    # Проверяем, существует ли файл в репозитории
    try:
        file = repo.get_contents(REMOTE_FILE_PATH2)
        repo.update_file(
            path=REMOTE_FILE_PATH2,
            message=f"Update data: {datetime.now().isoformat()}",
            content=content,
            sha=file.sha
        )
        print(f"Файл {REMOTE_FILE_PATH2} обновлён в репозитории.")
    except Exception as e:
        # Если файла нет, создаём новый
        repo.create_file(
            path=REMOTE_FILE_PATH2,
            message=f"Initial commit: {datetime.now().isoformat()}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH2} создан в репозитории.")



def fetch_data2():
    """Получение данных с указанного URL"""
    response = requests.get(URL3)
    response.raise_for_status()  # Проверка на ошибки
    return response.text

def save_to_local_file2(content):
    """Сохранение данных в локальный файл"""
    with open(LOCAL_FILE_PATH3, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Данные сохранены локально в файл {LOCAL_FILE_PATH3}")

def upload_to_github2():
    """Загрузка локального файла в репозиторий GitHub"""
    if not os.path.exists(LOCAL_FILE_PATH3):
        print(f"Файл {LOCAL_FILE_PATH3} не найден. Завершение работы.")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Читаем содержимое локального файла
    with open(LOCAL_FILE_PATH3, "r", encoding="utf-8") as file:
        content = file.read()

    # Проверяем, существует ли файл в репозитории
    try:
        file = repo.get_contents(REMOTE_FILE_PATH3)
        repo.update_file(
            path=REMOTE_FILE_PATH3,
            message=f"Update data: {datetime.now().isoformat()}",
            content=content,
            sha=file.sha
        )
        print(f"Файл {REMOTE_FILE_PATH3} обновлён в репозитории.")
    except Exception as e:
        # Если файла нет, создаём новый
        repo.create_file(
            path=REMOTE_FILE_PATH3,
            message=f"Initial commit: {datetime.now().isoformat()}",
            content=content
        )
        print(f"Файл {REMOTE_FILE_PATH3} создан в репозитории.")



def main():
    try:
        # Получаем данные и сохраняем локально
        data = fetch_data()
        save_to_local_file(data)

        data1 = fetch_data1()
        save_to_local_file1(data1)

        data2 = fetch_data2()
        save_to_local_file2(data2)
        
        # Загружаем локальный файл в GitHub
        upload_to_github()

        upload_to_github1()

        upload_to_github2()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
