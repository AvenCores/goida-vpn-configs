from src.logger import log
from src.config import GITHUB_TOKEN, REPO_NAME

# -------------------- GITHUB API (только для статистики) --------------------
_repo_stats_client = None
REPO = None

if GITHUB_TOKEN:
    try:
        from github import Github, Auth
        _repo_stats_client = Github(auth=Auth.Token(GITHUB_TOKEN))
        REPO = _repo_stats_client.get_repo(REPO_NAME)
        try:
            remaining, limit = _repo_stats_client.rate_limiting
            if remaining < 100:
                log(f"⚠️ Внимание: осталось {remaining}/{limit} запросов к GitHub API")
            else:
                log(f"ℹ️ Доступно запросов к GitHub API: {remaining}/{limit}")
        except Exception as e:
            log(f"⚠️ Не удалось проверить лимиты GitHub API: {e}")
    except ImportError:
        log("⚠️ PyGithub не установлен — статистика репозитория недоступна")
else:
    log("⚠️ MY_TOKEN не задан — статистика репозитория недоступна")


def _traffic_counts(traffic) -> tuple[int, int]:
    if traffic is None:
        return 0, 0
    if isinstance(traffic, tuple) and len(traffic) >= 2:
        if isinstance(traffic[0], (int, float)) and isinstance(traffic[1], (int, float)):
            return int(traffic[0]), int(traffic[1])
    if isinstance(traffic, dict):
        if "count" in traffic or "uniques" in traffic:
            return int(traffic.get("count", 0)), int(traffic.get("uniques", 0))
        items = traffic.get("views") or traffic.get("clones") or []
        return _sum_traffic_items(items)
    if hasattr(traffic, "count") and hasattr(traffic, "uniques"):
        return int(getattr(traffic, "count", 0) or 0), int(getattr(traffic, "uniques", 0) or 0)
    for attr in ("views", "clones"):
        if hasattr(traffic, attr):
            return _sum_traffic_items(getattr(traffic, attr) or [])
    if hasattr(traffic, "raw_data"):
        raw = getattr(traffic, "raw_data") or {}
        if isinstance(raw, dict):
            if "count" in raw or "uniques" in raw:
                return int(raw.get("count", 0)), int(raw.get("uniques", 0))
            items = raw.get("views") or raw.get("clones") or []
            return _sum_traffic_items(items)
    if isinstance(traffic, (list, tuple)):
        return _sum_traffic_items(traffic)
    return 0, 0


def _sum_traffic_items(items) -> tuple[int, int]:
    total_count = total_uniques = 0
    for item in items or []:
        if isinstance(item, dict):
            total_count += int(item.get("count", 0) or 0)
            total_uniques += int(item.get("uniques", 0) or 0)
        else:
            total_count += int(getattr(item, "count", 0) or 0)
            total_uniques += int(getattr(item, "uniques", 0) or 0)
    return total_count, total_uniques


def get_repo_stats() -> dict | None:
    if REPO is None:
        return None
    stats: dict[str, int] = {}
    try:
        views_count, views_uniques = _traffic_counts(REPO.get_views_traffic())
        stats["views_count"] = views_count
        stats["views_uniques"] = views_uniques
    except Exception as e:
        log(f"⚠️ Не удалось получить просмотры: {e}")
        return None
    try:
        clones_count, clones_uniques = _traffic_counts(REPO.get_clones_traffic())
        stats["clones_count"] = clones_count
        stats["clones_uniques"] = clones_uniques
    except Exception as e:
        log(f"⚠️ Не удалось получить клоны: {e}")
        return None
    return stats


def build_repo_stats_table(stats: dict) -> str:
    def _fmt(v) -> str:
        try:
            return f"{int(v):,}"
        except Exception:
            return str(v)

    header = "| Показатель | Значение |\n|--|--|"
    rows = [
        f"| Просмотры (14Д) | {_fmt(stats['views_count'])} |",
        f"| Клоны (14Д) | {_fmt(stats['clones_count'])} |",
        f"| Уникальные клоны (14Д) | {_fmt(stats['clones_uniques'])} |",
        f"| Уникальные посетители (14Д) | {_fmt(stats['views_uniques'])} |",
    ]
    return header + "\n" + "\n".join(rows)
