import os
import urllib.parse
import json
import re
import base64
import concurrent.futures
from src.config import (
    URLS,
    LOCAL_PATHS,
    GITHUBMIRROR_DIR,
    SNI_DOMAINS_PATH,
    EXTRA_URLS_FOR_26,
    EXTRA_URL_TIMEOUT,
    EXTRA_URL_MAX_ATTEMPTS,
)
from src.logger import log
from src.network import fetch_data, _format_fetch_error
from src.parser import filter_insecure_configs

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
        log(f"⚠️ Ошибка при скачивании {file_index}.txt ({url}): {short_msg}")
        return None

# -------------------- 26-й ФАЙЛ --------------------

def create_filtered_configs() -> str:
    """Создаёт 26-й файл: конфиги для SNI/CIDR белых списков."""
    try:
        with open(SNI_DOMAINS_PATH, "r", encoding="utf-8") as f:
            sni_domains = json.load(f)
    except Exception as e:
        log(f"❌ Ошибка загрузки {SNI_DOMAINS_PATH}: {e}")
        return os.path.join(GITHUBMIRROR_DIR, "26.txt")

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
            configs = data.splitlines()
        except Exception as e:
            log(f"⚠️ Ошибка при загрузке 26.txt ({url}): {_format_fetch_error(e)}")
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
