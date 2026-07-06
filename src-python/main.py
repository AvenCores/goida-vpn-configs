import argparse
import concurrent.futures
import os
import sys
from src.config import URLS, DEFAULT_MAX_WORKERS
from src.logger import updated_files, _UPDATED_FILES_LOCK, LOGS_BY_FILE
from src.file_manager import download_and_save, create_filtered_configs
from src.release_fetcher import fetch_latest_release_links, fetch_vc_runtime_link
from src.readme_updater import update_readme_download_links, update_readme_table
from src.git_ops import git_commit_and_push

# Настройка кодировки вывода для избежания ошибок UnicodeEncodeError на Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

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
    parser = argparse.ArgumentParser(description="Скачивание репозитория и коммит в GitHub")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Сохранять файлы локально и делать коммит, но не пушить",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
