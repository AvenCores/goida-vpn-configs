import os
import subprocess
import json

SOURCE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -------------------- КОРЕНЬ РЕПОЗИТОРИЯ --------------------
try:
    GIT_ROOT = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        stderr=subprocess.DEVNULL,
    ).decode().strip()
except Exception:
    GIT_ROOT = os.path.abspath(os.path.join(SOURCE_ROOT, ".."))

GITHUBMIRROR_DIR = os.path.join(GIT_ROOT, "githubmirror")
README_PATH = os.path.join(GIT_ROOT, "README.md")
SNI_DOMAINS_PATH = os.path.join(SOURCE_ROOT, "config", "sni_domains.json")
URLS_PATH = os.path.join(SOURCE_ROOT, "config", "urls.json")
URLS_26_PATH = os.path.join(SOURCE_ROOT, "config", "26_urls.json")

# -------------------- ЗАГРУЗКА КОНФИГУРАЦИИ --------------------
def _load_json_list(path: str, default: list) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                # Сортируем по ключам-числам для сохранения оригинального порядка
                return [data[k] for k in sorted(data.keys(), key=lambda x: int(x))]
            return data
    except Exception:
        return default

URLS = _load_json_list(URLS_PATH, [])
EXTRA_URLS_FOR_26 = _load_json_list(URLS_26_PATH, [])

# Создаём папку зеркала, если она не существует
os.makedirs(GITHUBMIRROR_DIR, exist_ok=True)

GITHUB_TOKEN = os.environ.get("MY_TOKEN")
REPO_NAME = "AvenCores/goida-vpn-configs"

EXTRA_URL_TIMEOUT = int(os.environ.get("EXTRA_URL_TIMEOUT", "6"))
EXTRA_URL_MAX_ATTEMPTS = int(os.environ.get("EXTRA_URL_MAX_ATTEMPTS", "2"))

LOCAL_PATHS = [os.path.join(GITHUBMIRROR_DIR, f"{i+1}.txt") for i in range(len(URLS))]
LOCAL_PATHS.append(os.path.join(GITHUBMIRROR_DIR, "26.txt"))

DEFAULT_MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "16"))
