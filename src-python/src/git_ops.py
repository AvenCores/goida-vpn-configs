import subprocess
import os
from src.config import GITHUBMIRROR_DIR, README_PATH, GIT_ROOT
from src.logger import log, offset

# -------------------- GIT --------------------

def git_commit_and_push(dry_run: bool = False):
    """Добавляет изменённые файлы в индекс, делает коммит и пушит."""
    try:
        subprocess.run(
            ["git", "add",
             os.path.relpath(GITHUBMIRROR_DIR, GIT_ROOT),
             os.path.relpath(README_PATH, GIT_ROOT)],
            check=True,
            cwd=GIT_ROOT,
        )

        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=GIT_ROOT,
        )
        if diff.returncode == 0:
            log("ℹ️ Нет изменений для коммита")
            return

        subprocess.run(
            ["git", "commit", "-m", f"🚀 Автообновление репозитория: {offset}"],
            check=True,
            cwd=GIT_ROOT,
        )
        log("✅ Коммит создан")

        if dry_run:
            log("ℹ️ Dry-run: push пропущен")
            return

        subprocess.run(["git", "push"], check=True, cwd=GIT_ROOT)
        log("✅ Изменения запушены в репозиторий")

    except subprocess.CalledProcessError as e:
        log(f"❌ Ошибка git: {e}")
