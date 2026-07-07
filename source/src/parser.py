import re
import base64
import urllib.parse
import html
import os
from src.logger import log

# -------------------- ФИЛЬТРАЦИЯ --------------------

PROTOCOL_PREFIXES = (
    "vmess://", "vless://", "trojan://", "ss://", "ssr://",
    "tuic://", "hysteria://", "hysteria2://", "hy2://",
    "socks5://", "socks4://", "wireguard://", "ssh://",
    "snell://", "brook://", "juicity://"
)

INSECURE_PATTERN = re.compile(
    r'(?:[?&;]|3%[Bb])(allowinsecure|allow_insecure|insecure)=(?:1|true|yes)(?:[&;#]|$|(?=\s|$))',
    re.IGNORECASE,
)


def try_decode_base64(data: str) -> str:
    """Проверяет, является ли строка списком в Base64, и декодирует её."""
    if "://" not in data:
        try:
            clean_data = "".join(data.split())
            rem = len(clean_data) % 4
            if rem:
                clean_data += "=" * (4 - rem)
            decoded = base64.b64decode(clean_data).decode("utf-8", errors="ignore")
            if any(prefix in decoded.lower() for prefix in PROTOCOL_PREFIXES):
                return decoded
        except Exception:
            pass
    return data


def filter_insecure_configs(local_path: str, data: str, log_enabled: bool = True) -> tuple[str, int]:
    """Декодирует Base64, разделяет конфиги и фильтрует только валидные и безопасные."""
    data = try_decode_base64(data)
    
    # Гарантируем, что протоколы начинаются с новой строки (если они склеены)
    # Используем все префиксы из PROTOCOL_PREFIXES для разделения
    pattern = "|".join(p.replace("://", "") for p in PROTOCOL_PREFIXES)
    data = re.sub(
        rf"({pattern})://",
        r"\n\1://",
        data,
        flags=re.IGNORECASE
    )
    
    result = []
    insecure_count = 0
    splitted = data.splitlines()
    
    for line in splitted:
        line_stripped = line.strip()
        if not line_stripped.lower().startswith(PROTOCOL_PREFIXES):
            continue
            
        processed = urllib.parse.unquote(html.unescape(line_stripped))
        if not INSECURE_PATTERN.search(processed):
            result.append(line_stripped)
        else:
            insecure_count += 1

    if insecure_count > 0 and log_enabled:
        log(f"ℹ️ Отфильтровано {insecure_count} небезопасных конфигов для {os.path.basename(local_path)}")
    return "\n".join(result), insecure_count
