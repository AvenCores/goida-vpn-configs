import os
import requests
import random
import time
from github import Github
from datetime import datetime
import zoneinfo

def is_https_proxy_working(proxy_url, test_url="https://www.google.com", timeout=5):
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }
    try:
        resp = requests.get(test_url, proxies=proxies, timeout=timeout)
        if resp.status_code == 200:
            return True
    except Exception:
        pass
    return False

def fetch_one_working_proxy():
    url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        raw_proxies = [f"http://{line.strip()}" for line in resp.text.splitlines() if line.strip()]
        print(f"🌐 Получено {len(raw_proxies)} прокси из открытого источника. Поиск одного рабочего...")
        for proxy in random.sample(raw_proxies, min(500, len(raw_proxies))):
            if is_https_proxy_working(proxy):
                print(f"✅ Найден рабочий HTTPS прокси: {proxy}")
                return proxy
        print("❌ Не найдено ни одного рабочего HTTPS прокси.")
        return None
    except Exception as e:
        print(f"⚠️ Не удалось получить список прокси: {e}")
        return None

WORKING_PROXY = fetch_one_working_proxy()
zone = zoneinfo.ZoneInfo("Europe/Moscow")
thistime = datetime.now(zone)
offset = thistime.strftime("%H:%M | %d.%m.%Y")
GITHUB_TOKEN = os.environ.get("MY_TOKEN")
REPO_NAME = "AvenCores/goida-vpn-configs"
if not os.path.exists("githubmirror"):
    os.mkdir("githubmirror")
URLS = [
    "https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality", #1
    "https://istanbulsydneyhotel.com/blogs/site/sni.php", #2
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt", #3
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt", #4
    "https://raw.githubusercontent.com/AliDev-ir/FreeVPN/main/pcvpn", #5
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt", #6
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt", #7
    "https://shadowmere.xyz/api/b64sub/", #8
    "https://vpn.fail/free-proxy/v2ray", #9
    "https://raw.githubusercontent.com/Proxydaemitelegram/Proxydaemi44/refs/heads/main/Proxydaemi44", #10
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt", #11
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all", #12
    "https://github.com/Kwinshadow/TelegramV2rayCollector/raw/refs/heads/main/sublinks/mix.txt", #13
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes", #14
    "https://github.com/4n0nymou3/multi-proxy-config-fetcher/raw/refs/heads/main/configs/proxy_configs.txt", #15
    "https://github.com/freefq/free/raw/refs/heads/master/v2", #16
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt", #17
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt", #18
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix", #19
    "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt", #20
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt", #21
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri", #22
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs.txt", #23
]
REMOTE_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]
LOCAL_PATHS = [f"githubmirror/{i+1}.txt" for i in range(len(URLS))]

def fetch_data(url):
    if WORKING_PROXY:
        proxies = {
            'http': WORKING_PROXY,
            'https': WORKING_PROXY,
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=15)
            response.raise_for_status()
            print(f"✅ Получено через рабочий прокси {WORKING_PROXY}")
            return response.text
        except Exception as e:
            print(f"⚠️ Ошибка через рабочий прокси {WORKING_PROXY}: {e}\nПробую без прокси...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print("✅ Получено без прокси.")
        return response.text
    except Exception as e:
        print(f"❌ Ошибка при прямом подключении: {e}")
        raise

def save_to_local_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"📁 Данные сохранены локально в {path}")

def upload_to_github(local_path, remote_path):
    if not os.path.exists(local_path):
        print(f"❌ Файл {local_path} не найден.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    with open(local_path, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        file_in_repo = repo.get_contents(remote_path)
        repo.update_file(
            path=remote_path,
            message=f"🚀 Обновление конфига по часовому поясу Европа/Москва: {offset}",
            content=content,
            sha=file_in_repo.sha
        )
        print(f"🚀 Файл {remote_path} обновлён в репозитории.\n\n")
    except Exception:
        repo.create_file(
            path=remote_path,
            message=f"🆕 Первый коммит по часовому поясу Европа/Москва: {offset}",
            content=content
        )
        print(f"🆕 Файл {remote_path} создан.\n")

def main():
    for url, local_path, remote_path in zip(URLS, LOCAL_PATHS, REMOTE_PATHS):
        try:
            data = fetch_data(url)
            save_to_local_file(local_path, data)
            upload_to_github(local_path, remote_path)
        except Exception as e:
            print(f"⚠️ Ошибка при обработке {url}: {e}\n")

if __name__ == "__main__":
    main()
