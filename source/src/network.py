import urllib.parse
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.config import URLS, DEFAULT_MAX_WORKERS

# -------------------- HTTP-СЕССИЯ --------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/148.0.0.0 Safari/537.36"
)


def _build_session(max_pool_size: int) -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(
        pool_connections=max_pool_size,
        pool_maxsize=max_pool_size,
        max_retries=Retry(
            total=1,
            backoff_factor=0.2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("HEAD", "GET", "OPTIONS"),
        ),
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": CHROME_UA})
    return session


REQUESTS_SESSION = _build_session(max_pool_size=max(DEFAULT_MAX_WORKERS, len(URLS)))

# -------------------- ПОЛУЧЕНИЕ ДАННЫХ --------------------

def fetch_data(
    url: str,
    timeout: int = 10,
    max_attempts: int = 3,
    session: requests.Session | None = None,
    allow_http_downgrade: bool = True,
) -> str:
    sess = session or REQUESTS_SESSION
    last_exc: Exception = RuntimeError("No attempts made")
    for attempt in range(1, max_attempts + 1):
        try:
            modified_url = url
            verify = True

            if attempt == 2:
                verify = False
            elif attempt == 3:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https" and allow_http_downgrade:
                    modified_url = parsed._replace(scheme="http").geturl()
                verify = False

            response = sess.get(modified_url, timeout=timeout, verify=verify)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < max_attempts:
                continue
    raise last_exc


def _format_fetch_error(exc: Exception) -> str:
    if isinstance(exc, requests.exceptions.ConnectTimeout):
        return "Connect timeout"
    if isinstance(exc, requests.exceptions.ReadTimeout):
        return "Read timeout"
    if isinstance(exc, requests.exceptions.Timeout):
        return "Timeout"
    if isinstance(exc, requests.exceptions.SSLError):
        return "TLS error"
    if isinstance(exc, requests.exceptions.HTTPError):
        try:
            return f"HTTP {exc.response.status_code}"
        except Exception:
            return "HTTP error"
    if isinstance(exc, requests.exceptions.ConnectionError):
        return "Connection error"
    msg = str(exc)
    return msg[:160] + "…" if len(msg) > 160 else msg
