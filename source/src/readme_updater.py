import os
import re
from src.config import README_PATH, URLS, REPO_NAME
from src.logger import log, offset, updated_files
from src.file_manager import extract_source_name
from src.github_api import get_repo_stats, build_repo_stats_table

# -------------------- README --------------------

def _insert_repo_stats_section(content: str, stats_section: str) -> str:
    pattern = r"(\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?\|--\|--\|--\|--\|--\|[\s\S]*?\n)(?=\n## )"
    match = re.search(pattern, content)
    if not match:
        return content.rstrip() + "\n\n" + stats_section + "\n"
    return re.sub(pattern, lambda m: m.group(1) + "\n" + stats_section, content, count=1)


def update_readme_download_links(links: dict[str, str], vc_runtime_link: str | None = None):
    """Обновляет ссылки на скачивание v2rayNG, Throne и Visual C++ Runtimes в README.md."""
    if not links and not vc_runtime_link:
        log("⚠️ Нет новых ссылок для обновления в README.md")
        return

    if not os.path.exists(README_PATH):
        log("❌ README.md не найден")
        return

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"⚠️ Ошибка при чтении README.md: {e}")
        return

    original_content = content

    # Обновляем ссылку на v2rayNG APK
    if 'v2rayng-apk' in links:
        # Паттерн для поиска ссылки на v2rayNG APK в формате: [Ссылка](https://github.com/.../v2rayNG_..._universal.apk)
        v2rayng_pattern = r'(\*\*1\.\*\* Скачиваем \*\*«v2rayNG»\*.*?\[Ссылка\]\()https://github\.com/2dust/v2rayNG/releases/download/[^)]+(\))'
        if re.search(v2rayng_pattern, content):
            content = re.sub(v2rayng_pattern, rf'\1{links["v2rayng-apk"]}\2', content)
            log(f"✅ Ссылка на v2rayNG обновлена в README.md")
        else:
            log("⚠️ Не найдена ссылка на v2rayNG в README.md")

    # Обновляем ссылки на Throne
    if 'throne-win10' in links:
        throne_pattern = r'(\[Windows 10/11\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_pattern, content):
            content = re.sub(throne_pattern, rf'\1{links["throne-win10"]}\2', content)
            log(f"✅ Ссылка на Throne Win10/11 обновлена в README.md")

    if 'throne-win7' in links:
        throne_win7_pattern = r'(\[Windows 7/8/8\.1\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_win7_pattern, content):
            content = re.sub(throne_win7_pattern, rf'\1{links["throne-win7"]}\2', content)
            log(f"✅ Ссылка на Throne Win7/8/8.1 обновлена в README.md")

    if 'throne-linux' in links:
        throne_linux_pattern = r'(\[Linux\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))'
        if re.search(throne_linux_pattern, content):
            content = re.sub(throne_linux_pattern, rf'\1{links["throne-linux"]}\2', content)
            log(f"✅ Ссылка на Throne Linux обновлена в README.md")

    # Обновляем ссылку на Visual C++ Runtimes
    if vc_runtime_link:
        vc_runtime_pattern = r'(\*\*4\.\*\* Скачиваем архив и распаковываем.*?\[Ссылка\]\()https://[^\)]+(\))'
        if re.search(vc_runtime_pattern, content):
            content = re.sub(vc_runtime_pattern, rf'\1{vc_runtime_link}\2', content)
            log(f"✅ Ссылка на Visual C++ Runtimes обновлена в README.md")
        else:
            log("⚠️ Не найдена ссылка на Visual C++ Runtimes в README.md")

    if content != original_content:
        try:
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            log("📝 Ссылки на скачивание в README.md обновлены")
        except Exception as e:
            log(f"⚠️ Ошибка при записи README.md: {e}")
    else:
        log("ℹ️ Ссылки на скачивание не требуют изменений")


def update_readme_table():
    """Обновляет таблицы в README.md локально."""
    if not os.path.exists(README_PATH):
        log("❌ README.md не найден")
        return
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            old_content = f.read()
    except Exception as e:
        log(f"⚠️ Ошибка при чтении README.md: {e}")
        return

    time_part, date_part = offset.split(" | ")

    table_header = "| № | Файл | Источник | Время | Дата |\n|--|--|--|--|--|"
    table_rows: list[str] = []

    all_urls_with_26 = URLS + [""]  # 26-й файл без внешнего URL
    for i, url in enumerate(all_urls_with_26, start=1):
        filename = f"{i}.txt"
        raw_file_url = f"https://github.com/{REPO_NAME}/raw/refs/heads/main/githubmirror/{i}.txt"

        if i <= 25:
            source_name = extract_source_name(url)
            source_column = f"[{source_name}]({url})"
        else:
            source_name = "Обход SNI/CIDR белых списков"
            source_column = f"[{source_name}]({raw_file_url})"

        if i in updated_files:
            update_time, update_date = time_part, date_part
        else:
            pattern = rf"\|\s*{i}\s*\|\s*\[`{filename}`\].*?\|.*?\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
            match = re.search(pattern, old_content)
            if match:
                update_time = match.group(1).strip() or "Никогда"
                update_date = match.group(2).strip() or "Никогда"
            else:
                update_time = update_date = "Никогда"

        table_rows.append(
            f"| {i} | [`{filename}`]({raw_file_url}) | {source_column} | {update_time} | {update_date} |"
        )

    new_table = table_header + "\n" + "\n".join(table_rows)

    table_pattern = r"\| № \| Файл \| Источник \| Время \| Дата \|[\s\S]*?\|--\|--\|--\|--\|--\|[\s\S]*?(\n\n## |$)"
    new_content = re.sub(table_pattern, new_table + r"\1", old_content)

    repo_stats = get_repo_stats()
    if repo_stats:
        stats_section = "## 📊 Статистика репозитория\n" + build_repo_stats_table(repo_stats) + "\n"
        stats_pattern = r"## 📊 Статистика репозитория\s*\n[\s\S]*?(?=\n## |\Z)"
        if re.search(stats_pattern, new_content):
            new_content = re.sub(stats_pattern, stats_section, new_content)
        else:
            new_content = _insert_repo_stats_section(new_content, stats_section)
    else:
        log("⚠️ Статистика репозитория недоступна, раздел не обновлён.")

    if new_content == old_content:
        log("📝 README.md не требует изменений")
        return

    try:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        log("📝 README.md обновлён")
    except Exception as e:
        log(f"⚠️ Ошибка при записи README.md: {e}")
