import requests
import re
import os
from src.logger import log

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
