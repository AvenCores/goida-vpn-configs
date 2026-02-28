#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import html
import json
import os
import random
import re
import shutil
import socket
import statistics
import subprocess
import tempfile
import time
import urllib.parse
from dataclasses import dataclass
from typing import Any

import requests


SUPPORTED_SCHEMES = {"vless", "vmess", "trojan"}
SUPPORTED_NETWORKS = {"tcp", "ws", "grpc", "xhttp", "httpupgrade"}
CONFIG_SPLIT_RE = re.compile(r"(vmess|vless|trojan|ss|ssr|tuic|hysteria2?|hy2)://", re.IGNORECASE)
DEFAULT_PROBE_URLS = (
    "https://cp.cloudflare.com/generate_204",
    "https://ya.ru/generate_204",
    "https://www.rbc.ru",
)


@dataclass
class Candidate:
    key: str
    raw: str
    scheme: str
    host: str
    port: int
    endpoint_key: str
    params: dict[str, Any]


@dataclass
class ValidationResult:
    ok: bool
    l0_ok: bool
    l1_ok: bool
    l2_ok: bool
    l2_skipped: bool
    attempts_ok: int
    attempts_total: int
    avg_latency_ms: float | None
    error: str = ""


@dataclass
class ValidatorConfig:
    source: str
    output: str
    state_path: str
    target_count: int
    max_candidates: int
    recheck_minutes: int
    retry_failed_minutes: int
    max_age_hours: int
    max_fail_streak: int
    tcp_timeout: float
    probe_timeout: float
    attempts: int
    attempt_success_threshold: int
    probe_success_per_attempt: int
    startup_wait_seconds: float
    pause_between_attempts: float
    xray_bin: str
    allow_tcp_only_fallback: bool
    dry_run: bool
    random_seed: int | None
    probe_urls: list[str]


def log(message: str) -> None:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{stamp}] {message}")


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def to_iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def parse_iso(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except Exception:
        return None


def ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def load_state(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {"configs": {}, "last_run": None}
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            return {"configs": {}, "last_run": None}
        data.setdefault("configs", {})
        return data
    except Exception:
        return {"configs": {}, "last_run": None}


def save_state(path: str, data: dict[str, Any]) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)


def load_source_text(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=15)
        response.raise_for_status()
        return response.text
    with open(source, "r", encoding="utf-8") as file:
        return file.read()


def normalize_line(line: str) -> str:
    cleaned = (line or "").strip()
    if not cleaned:
        return ""
    cleaned = cleaned.strip("`")
    cleaned = cleaned.strip(" ,")
    if cleaned.startswith(("'", '"')) and cleaned.endswith(("'", '"')) and len(cleaned) >= 2:
        cleaned = cleaned[1:-1]
    cleaned = cleaned.replace("\\u0026", "&").replace("\\u003d", "=").replace("\\/", "/")
    cleaned = html.unescape(cleaned)
    cleaned = cleaned.strip("`")
    cleaned = cleaned.strip(" ,")

    match = re.search(r"(vmess|vless|trojan|ss|ssr|tuic|hysteria2?|hy2)://", cleaned, re.IGNORECASE)
    if match:
        cleaned = cleaned[match.start():]
    return cleaned.strip()


def extract_raw_configs(raw_text: str) -> list[str]:
    expanded = CONFIG_SPLIT_RE.sub(lambda m: "\n" + m.group(0).lower(), raw_text.replace("\r", "\n"))
    lines = expanded.splitlines()
    result: list[str] = []
    seen: set[str] = set()

    for line in lines:
        item = normalize_line(line)
        if not item or item.startswith("#"):
            continue
        if "://" not in item:
            continue
        if item in seen:
            continue
        seen.add(item)
        result.append(item)

    return result


def candidate_key(raw: str) -> str:
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()


def parse_candidate(raw: str) -> Candidate | None:
    scheme = raw.split("://", 1)[0].lower()
    if scheme not in SUPPORTED_SCHEMES:
        return None

    if scheme == "vmess":
        return parse_vmess_candidate(raw)
    return parse_url_candidate(raw, scheme)


def parse_url_candidate(raw: str, scheme: str) -> Candidate | None:
    try:
        parsed = urllib.parse.urlsplit(raw)
        host = parsed.hostname
        port = parsed.port
    except Exception:
        return None

    if not host or not port or not (1 <= int(port) <= 65535):
        return None

    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

    def q(name: str, default: str = "") -> str:
        values = query.get(name)
        if not values:
            return default
        return values[0]

    network = q("type", "tcp").lower()
    security = q("security", "none").lower()
    sni = q("sni", "")
    host_header = q("host", "")
    path = q("path", "")
    service_name = q("serviceName", q("service_name", ""))
    mode = q("mode", "")
    flow = q("flow", "")
    fingerprint = q("fp", "")
    pbk = q("pbk", "")
    sid = q("sid", "")
    spx = q("spx", q("spiderX", ""))
    alpn = q("alpn", "")

    params: dict[str, Any] = {
        "network": network,
        "security": security,
        "sni": sni,
        "host_header": host_header,
        "path": path,
        "service_name": service_name,
        "mode": mode,
        "flow": flow,
        "fingerprint": fingerprint,
        "pbk": pbk,
        "sid": sid,
        "spx": spx,
        "alpn": alpn,
    }

    if scheme == "vless":
        user_id = urllib.parse.unquote(parsed.username or "")
        if not user_id:
            return None
        params["id"] = user_id
        params["encryption"] = q("encryption", "none")
    elif scheme == "trojan":
        password = urllib.parse.unquote(parsed.username or "")
        if not password:
            return None
        params["password"] = password
    else:
        return None

    return Candidate(
        key=candidate_key(raw),
        raw=raw,
        scheme=scheme,
        host=host,
        port=int(port),
        endpoint_key=f"{host.lower()}:{int(port)}",
        params=params,
    )


def parse_vmess_candidate(raw: str) -> Candidate | None:
    payload = raw[len("vmess://"):]
    payload = payload.split("#", 1)[0].strip()
    if not payload:
        return None

    try:
        padding = "=" * ((4 - len(payload) % 4) % 4)
        decoded = base64.urlsafe_b64decode(payload + padding).decode("utf-8", errors="ignore")
        config = json.loads(decoded)
    except Exception:
        return None

    host = str(config.get("add") or config.get("host") or "").strip()
    port_raw = config.get("port")
    user_id = str(config.get("id") or "").strip()
    if not host or not user_id:
        return None

    try:
        port = int(str(port_raw))
    except Exception:
        return None
    if not (1 <= port <= 65535):
        return None

    network = str(config.get("net") or config.get("type") or "tcp").lower()
    transport_security = str(config.get("tls") or config.get("security") or "none").lower()
    params: dict[str, Any] = {
        "id": user_id,
        "aid": int(str(config.get("aid", 0)) or 0),
        "network": network,
        "security": transport_security,
        "sni": str(config.get("sni") or ""),
        "host_header": str(config.get("host") or ""),
        "path": str(config.get("path") or ""),
        "service_name": str(config.get("serviceName") or ""),
        "mode": str(config.get("mode") or ""),
        "fingerprint": str(config.get("fp") or ""),
        "pbk": str(config.get("pbk") or ""),
        "sid": str(config.get("sid") or ""),
        "spx": str(config.get("spx") or config.get("spiderX") or ""),
        "alpn": str(config.get("alpn") or ""),
        "user_security": str(config.get("scy") or "auto"),
    }

    return Candidate(
        key=candidate_key(raw),
        raw=raw,
        scheme="vmess",
        host=host,
        port=port,
        endpoint_key=f"{host.lower()}:{port}",
        params=params,
    )


def tcp_reachable(host: str, port: int, timeout: float) -> bool:
    try:
        addr_info = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError:
        return False

    for family, socktype, proto, _, sockaddr in addr_info:
        try:
            with socket.socket(family, socktype, proto) as sock:
                sock.settimeout(timeout)
                sock.connect(sockaddr)
            return True
        except OSError:
            continue
    return False


def build_stream_settings(candidate: Candidate) -> tuple[dict[str, Any] | None, str]:
    params = candidate.params
    network = str(params.get("network", "tcp") or "tcp").lower()
    if network not in SUPPORTED_NETWORKS:
        return None, f"unsupported network={network}"

    security = str(params.get("security", "none") or "none").lower()
    sni = str(params.get("sni", "") or "")
    host_header = str(params.get("host_header", "") or "")
    path = str(params.get("path", "") or "")
    service_name = str(params.get("service_name", "") or "")
    mode = str(params.get("mode", "") or "")
    fingerprint = str(params.get("fingerprint", "") or "")
    pbk = str(params.get("pbk", "") or "")
    sid = str(params.get("sid", "") or "")
    spx = str(params.get("spx", "") or "")
    alpn = str(params.get("alpn", "") or "")

    stream: dict[str, Any] = {"network": network}

    if security == "reality":
        if not pbk:
            return None, "missing pbk for reality"
        if not sni:
            return None, "missing sni for reality"
        reality_settings: dict[str, Any] = {"serverName": sni, "publicKey": pbk}
        if fingerprint:
            reality_settings["fingerprint"] = fingerprint
        if sid:
            reality_settings["shortId"] = sid
        if spx:
            reality_settings["spiderX"] = spx
        stream["security"] = "reality"
        stream["realitySettings"] = reality_settings
    elif security in {"tls", "xtls"}:
        tls_settings: dict[str, Any] = {"serverName": sni or candidate.host, "allowInsecure": False}
        if fingerprint:
            tls_settings["fingerprint"] = fingerprint
        if alpn:
            tls_settings["alpn"] = [part for part in alpn.split(",") if part]
        stream["security"] = "tls"
        stream["tlsSettings"] = tls_settings
    else:
        stream["security"] = "none"

    if network == "ws":
        ws_settings: dict[str, Any] = {"path": path or "/"}
        if host_header:
            ws_settings["headers"] = {"Host": host_header}
        stream["wsSettings"] = ws_settings
    elif network == "grpc":
        grpc_settings: dict[str, Any] = {}
        if service_name:
            grpc_settings["serviceName"] = service_name
        if mode.lower() == "multi":
            grpc_settings["multiMode"] = True
        stream["grpcSettings"] = grpc_settings
    elif network == "xhttp":
        xhttp_settings: dict[str, Any] = {}
        if path:
            xhttp_settings["path"] = path
        if host_header:
            xhttp_settings["host"] = host_header
        stream["xhttpSettings"] = xhttp_settings
    elif network == "httpupgrade":
        httpupgrade_settings: dict[str, Any] = {"path": path or "/"}
        if host_header:
            httpupgrade_settings["host"] = host_header
        stream["httpupgradeSettings"] = httpupgrade_settings

    return stream, ""


def build_outbound(candidate: Candidate) -> tuple[dict[str, Any] | None, str]:
    stream_settings, reason = build_stream_settings(candidate)
    if stream_settings is None:
        return None, reason

    if candidate.scheme == "vless":
        user: dict[str, Any] = {
            "id": candidate.params["id"],
            "encryption": str(candidate.params.get("encryption", "none") or "none"),
        }
        flow = str(candidate.params.get("flow", "") or "")
        if flow:
            user["flow"] = flow
        outbound = {
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": candidate.host,
                        "port": candidate.port,
                        "users": [user],
                    }
                ]
            },
            "streamSettings": stream_settings,
        }
        return outbound, ""

    if candidate.scheme == "trojan":
        outbound = {
            "protocol": "trojan",
            "settings": {
                "servers": [
                    {
                        "address": candidate.host,
                        "port": candidate.port,
                        "password": candidate.params["password"],
                    }
                ]
            },
            "streamSettings": stream_settings,
        }
        return outbound, ""

    if candidate.scheme == "vmess":
        outbound = {
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": candidate.host,
                        "port": candidate.port,
                        "users": [
                            {
                                "id": candidate.params["id"],
                                "alterId": int(candidate.params.get("aid", 0)),
                                "security": str(candidate.params.get("user_security", "auto")),
                            }
                        ],
                    }
                ]
            },
            "streamSettings": stream_settings,
        }
        return outbound, ""

    return None, "unsupported scheme"


def allocate_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def terminate_process(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=2)
        return
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            return


def probe_url_via_socks(socks_port: int, url: str, timeout: float) -> tuple[bool, float | None, str]:
    cmd = [
        "curl",
        "--socks5-hostname",
        f"127.0.0.1:{socks_port}",
        "--connect-timeout",
        str(timeout),
        "--max-time",
        str(timeout),
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--write-out",
        "%{http_code} %{time_total}",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        return False, None, f"curl error ({proc.returncode}): {stderr[:140]}"

    output = (proc.stdout or "").strip().split()
    if len(output) != 2:
        return False, None, "unexpected curl output"
    code_raw, time_raw = output
    try:
        code = int(code_raw)
        latency_ms = float(time_raw) * 1000.0
    except ValueError:
        return False, None, "invalid curl metrics"

    success = 200 <= code < 500 and code != 407
    return success, latency_ms, ""


def run_l2_checks(candidate: Candidate, outbound: dict[str, Any], cfg: ValidatorConfig) -> ValidationResult:
    xray_path = shutil.which(cfg.xray_bin)
    if not xray_path:
        if cfg.allow_tcp_only_fallback:
            return ValidationResult(
                ok=True,
                l0_ok=True,
                l1_ok=True,
                l2_ok=False,
                l2_skipped=True,
                attempts_ok=0,
                attempts_total=0,
                avg_latency_ms=None,
                error="xray binary not found; tcp-only fallback",
            )
        return ValidationResult(
            ok=False,
            l0_ok=True,
            l1_ok=True,
            l2_ok=False,
            l2_skipped=False,
            attempts_ok=0,
            attempts_total=0,
            avg_latency_ms=None,
            error=f"xray binary not found: {cfg.xray_bin}",
        )

    attempt_ok = 0
    attempt_total = cfg.attempts
    successful_latencies: list[float] = []
    errors: list[str] = []

    for attempt in range(cfg.attempts):
        socks_port = allocate_free_port()
        runtime_config = {
            "log": {"loglevel": "warning"},
            "inbounds": [
                {
                    "tag": "socks-in",
                    "listen": "127.0.0.1",
                    "port": socks_port,
                    "protocol": "socks",
                    "settings": {"udp": False},
                }
            ],
            "outbounds": [
                {"tag": "proxy", **outbound},
                {"tag": "direct", "protocol": "freedom"},
            ],
        }

        temp_config_path = ""
        proc: subprocess.Popen[str] | None = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as temp_file:
                json.dump(runtime_config, temp_file, ensure_ascii=False)
                temp_config_path = temp_file.name

            proc = subprocess.Popen(
                [xray_path, "run", "-config", temp_config_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            time.sleep(cfg.startup_wait_seconds)

            if proc.poll() is not None:
                stderr = (proc.stderr.read() if proc.stderr else "")[:240].strip()
                errors.append(f"xray exited early: {stderr or 'no stderr'}")
                continue

            success_count = 0
            per_attempt_latencies: list[float] = []

            for url in cfg.probe_urls:
                success, latency_ms, err = probe_url_via_socks(socks_port, url, cfg.probe_timeout)
                if success:
                    success_count += 1
                    if latency_ms is not None:
                        per_attempt_latencies.append(latency_ms)
                elif err:
                    errors.append(err)

            if success_count >= cfg.probe_success_per_attempt:
                attempt_ok += 1
                if per_attempt_latencies:
                    successful_latencies.append(statistics.mean(per_attempt_latencies))
        except Exception as exc:
            errors.append(str(exc)[:200])
        finally:
            if proc is not None:
                terminate_process(proc)
            if temp_config_path and os.path.exists(temp_config_path):
                try:
                    os.remove(temp_config_path)
                except OSError:
                    pass

        if attempt < cfg.attempts - 1 and cfg.pause_between_attempts > 0:
            time.sleep(cfg.pause_between_attempts)

    l2_ok = attempt_ok >= cfg.attempt_success_threshold
    avg_latency = statistics.mean(successful_latencies) if successful_latencies else None
    return ValidationResult(
        ok=l2_ok,
        l0_ok=True,
        l1_ok=True,
        l2_ok=l2_ok,
        l2_skipped=False,
        attempts_ok=attempt_ok,
        attempts_total=attempt_total,
        avg_latency_ms=avg_latency,
        error="; ".join(errors[:3]) if errors and not l2_ok else "",
    )


def validate_candidate(candidate: Candidate, cfg: ValidatorConfig) -> ValidationResult:
    if not candidate:
        return ValidationResult(False, False, False, False, False, 0, 0, None, "parse failed")

    l1_ok = tcp_reachable(candidate.host, candidate.port, cfg.tcp_timeout)
    if not l1_ok:
        return ValidationResult(False, True, False, False, False, 0, 0, None, "tcp unreachable")

    outbound, reason = build_outbound(candidate)
    if outbound is None:
        return ValidationResult(False, True, True, False, False, 0, 0, None, reason)

    return run_l2_checks(candidate, outbound, cfg)


def minutes_since(iso_time: str | None, now: dt.datetime) -> float | None:
    parsed = parse_iso(iso_time)
    if not parsed:
        return None
    return (now - parsed).total_seconds() / 60.0


def hours_since(iso_time: str | None, now: dt.datetime) -> float | None:
    parsed = parse_iso(iso_time)
    if not parsed:
        return None
    return (now - parsed).total_seconds() / 3600.0


def is_entry_healthy(entry: dict[str, Any], now: dt.datetime, cfg: ValidatorConfig) -> bool:
    fail_streak = int(entry.get("fail_streak", 0) or 0)
    if fail_streak > cfg.max_fail_streak:
        return False
    age_hours = hours_since(entry.get("last_success"), now)
    if age_hours is None:
        return False
    return age_hours <= cfg.max_age_hours


def entry_needs_recheck(entry: dict[str, Any], now: dt.datetime, cfg: ValidatorConfig) -> bool:
    delta_minutes = minutes_since(entry.get("last_checked"), now)
    if delta_minutes is None:
        return True
    return delta_minutes >= cfg.recheck_minutes


def calculate_score(entry: dict[str, Any]) -> float:
    checks_total = max(1, int(entry.get("checks_total", 0) or 0))
    checks_ok = int(entry.get("checks_ok", 0) or 0)
    success_rate = checks_ok / checks_total

    l2_checks = max(1, int(entry.get("l2_checks", 0) or 0))
    l2_passes = int(entry.get("l2_passes", 0) or 0)
    l2_rate = l2_passes / l2_checks

    latency_ms = entry.get("last_latency_ms")
    if isinstance(latency_ms, (int, float)):
        latency_score = max(0.0, 1.0 - min(float(latency_ms), 3000.0) / 3000.0)
    else:
        latency_score = 0.45

    fail_streak = int(entry.get("fail_streak", 0) or 0)
    stability = max(0.0, 1.0 - min(fail_streak, 4) * 0.2)

    raw_score = (success_rate * 0.5 + l2_rate * 0.25 + latency_score * 0.15 + stability * 0.10) * 100.0
    return round(raw_score, 2)


def update_entry(state: dict[str, Any], candidate: Candidate, result: ValidationResult, now: dt.datetime) -> None:
    configs = state.setdefault("configs", {})
    entry = configs.get(candidate.key, {})

    entry["raw"] = candidate.raw
    entry["scheme"] = candidate.scheme
    entry["host"] = candidate.host
    entry["port"] = candidate.port
    entry["endpoint_key"] = candidate.endpoint_key
    entry["last_checked"] = to_iso(now)
    entry["checks_total"] = int(entry.get("checks_total", 0) or 0) + 1

    if not result.l2_skipped and result.attempts_total > 0:
        entry["l2_checks"] = int(entry.get("l2_checks", 0) or 0) + 1
        if result.l2_ok:
            entry["l2_passes"] = int(entry.get("l2_passes", 0) or 0) + 1
    else:
        entry.setdefault("l2_checks", int(entry.get("l2_checks", 0) or 0))
        entry.setdefault("l2_passes", int(entry.get("l2_passes", 0) or 0))

    if result.ok:
        entry["checks_ok"] = int(entry.get("checks_ok", 0) or 0) + 1
        entry["fail_streak"] = 0
        entry["last_success"] = to_iso(now)
        entry["last_error"] = ""
        if result.avg_latency_ms is not None:
            entry["last_latency_ms"] = round(result.avg_latency_ms, 2)
    else:
        entry.setdefault("checks_ok", int(entry.get("checks_ok", 0) or 0))
        entry["fail_streak"] = int(entry.get("fail_streak", 0) or 0) + 1
        entry["last_error"] = result.error[:240]

    entry["score"] = calculate_score(entry)
    entry.setdefault("active", False)
    configs[candidate.key] = entry


def select_final_pool(state: dict[str, Any], cfg: ValidatorConfig, now: dt.datetime) -> list[tuple[str, dict[str, Any]]]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for key, entry in state.get("configs", {}).items():
        if is_entry_healthy(entry, now, cfg):
            candidates.append((key, entry))

    candidates.sort(
        key=lambda item: (
            float(item[1].get("score", 0.0) or 0.0),
            item[1].get("last_success") or "",
        ),
        reverse=True,
    )

    selected: list[tuple[str, dict[str, Any]]] = []
    used_endpoints: set[str] = set()

    for key, entry in candidates:
        endpoint = str(entry.get("endpoint_key") or "")
        if endpoint and endpoint in used_endpoints:
            continue
        selected.append((key, entry))
        if endpoint:
            used_endpoints.add(endpoint)
        if len(selected) >= cfg.target_count:
            return selected

    if len(selected) < cfg.target_count:
        selected_keys = {key for key, _ in selected}
        for key, entry in candidates:
            if key in selected_keys:
                continue
            selected.append((key, entry))
            if len(selected) >= cfg.target_count:
                break

    return selected


def run_cycle(cfg: ValidatorConfig) -> int:
    if cfg.random_seed is not None:
        random.seed(cfg.random_seed)

    now = now_utc()
    state = load_state(cfg.state_path)
    configs_state = state.setdefault("configs", {})

    source_text = load_source_text(cfg.source)
    raw_configs = extract_raw_configs(source_text)

    parsed_candidates: dict[str, Candidate] = {}
    for raw in raw_configs:
        candidate = parse_candidate(raw)
        if candidate is None:
            continue
        parsed_candidates[candidate.key] = candidate

    log(
        f"loaded {len(raw_configs)} raw configs, {len(parsed_candidates)} parsed candidates; "
        f"state entries={len(configs_state)}"
    )

    validated_keys: set[str] = set()

    recheck_budget = max(cfg.target_count * 3, cfg.target_count)
    active_keys = [key for key, entry in configs_state.items() if entry.get("active")]
    active_keys.sort(
        key=lambda key: (
            minutes_since(configs_state.get(key, {}).get("last_checked"), now) or 10**9,
            float(configs_state.get(key, {}).get("score", 0.0) or 0.0),
        ),
        reverse=True,
    )

    rechecked = 0
    for key in active_keys:
        if rechecked >= recheck_budget:
            break
        entry = configs_state.get(key)
        if not entry or not entry_needs_recheck(entry, now, cfg):
            continue

        candidate = parse_candidate(str(entry.get("raw", "") or ""))
        if candidate is None:
            continue

        result = validate_candidate(candidate, cfg)
        update_entry(state, candidate, result, now)
        validated_keys.add(candidate.key)
        rechecked += 1
        status = "PASS" if result.ok else "FAIL"
        log(f"recheck {status} {candidate.endpoint_key} score={state['configs'][candidate.key].get('score')}")

    selected = select_final_pool(state, cfg, now)
    selected_keys = {key for key, _ in selected}
    selected_endpoints = {str(entry.get("endpoint_key") or "") for _, entry in selected}

    if len(selected) < cfg.target_count:
        needed = cfg.target_count - len(selected)
        log(f"need {needed} additional working configs")

        candidates_list = list(parsed_candidates.values())
        random.shuffle(candidates_list)
        candidates_list.sort(
            key=lambda item: float(state["configs"].get(item.key, {}).get("score", 0.0) or 0.0),
            reverse=True,
        )

        checked_new = 0
        for candidate in candidates_list:
            if checked_new >= cfg.max_candidates:
                break
            if candidate.key in validated_keys:
                continue
            if candidate.key in selected_keys:
                continue

            entry = state["configs"].get(candidate.key, {})
            failed_recently = (
                int(entry.get("fail_streak", 0) or 0) > 0
                and (minutes_since(entry.get("last_checked"), now) or 10**9) < cfg.retry_failed_minutes
            )
            if failed_recently:
                continue

            if candidate.endpoint_key in selected_endpoints:
                continue

            result = validate_candidate(candidate, cfg)
            update_entry(state, candidate, result, now)
            validated_keys.add(candidate.key)
            checked_new += 1

            if result.ok and is_entry_healthy(state["configs"][candidate.key], now, cfg):
                selected_keys.add(candidate.key)
                selected_endpoints.add(candidate.endpoint_key)
                selected = select_final_pool(state, cfg, now)
                if len(selected) >= cfg.target_count:
                    break

            status = "PASS" if result.ok else "FAIL"
            log(f"new    {status} {candidate.endpoint_key} score={state['configs'][candidate.key].get('score')}")

    selected = select_final_pool(state, cfg, now)
    selected_keys = {key for key, _ in selected}

    for key, entry in state.get("configs", {}).items():
        entry["active"] = key in selected_keys

    output_lines = [entry["raw"] for _, entry in selected]
    output_text = "\n".join(output_lines).strip()
    if output_text:
        output_text += "\n"

    if not cfg.dry_run:
        ensure_parent(cfg.output)
        with open(cfg.output, "w", encoding="utf-8") as file:
            file.write(output_text)

    state["last_run"] = to_iso(now)
    save_state(cfg.state_path, state)

    log(
        f"cycle complete: active={len(selected)} output={cfg.output} "
        f"state={cfg.state_path} dry_run={cfg.dry_run}"
    )
    return len(selected)


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Builds a stable pool of working configs from source list using multi-step validation."
    )
    parser.add_argument("--source", default="../githubmirror/26.txt")
    parser.add_argument("--output", default="../githubmirror/26.stable.txt")
    parser.add_argument("--state", dest="state_path", default="./stable_pool_state.json")
    parser.add_argument("--target-count", type=int, default=10)
    parser.add_argument("--max-candidates", type=int, default=180)
    parser.add_argument("--recheck-minutes", type=int, default=180)
    parser.add_argument("--retry-failed-minutes", type=int, default=90)
    parser.add_argument("--max-age-hours", type=int, default=36)
    parser.add_argument("--max-fail-streak", type=int, default=2)
    parser.add_argument("--tcp-timeout", type=float, default=2.2)
    parser.add_argument("--probe-timeout", type=float, default=8.0)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--attempt-success-threshold", type=int, default=2)
    parser.add_argument("--probe-success-per-attempt", type=int, default=2)
    parser.add_argument("--startup-wait-seconds", type=float, default=0.6)
    parser.add_argument("--pause-between-attempts", type=float, default=0.6)
    parser.add_argument("--xray-bin", default="xray")
    parser.add_argument("--allow-tcp-only-fallback", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--interval-minutes", type=int, default=0)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--probe-url", action="append", dest="probe_urls")
    return parser


def build_config(args: argparse.Namespace) -> ValidatorConfig:
    probe_urls = args.probe_urls if args.probe_urls else list(DEFAULT_PROBE_URLS)
    attempt_success_threshold = max(1, min(args.attempt_success_threshold, args.attempts))
    probe_success_per_attempt = max(1, min(args.probe_success_per_attempt, len(probe_urls)))

    return ValidatorConfig(
        source=args.source,
        output=args.output,
        state_path=args.state_path,
        target_count=max(1, args.target_count),
        max_candidates=max(1, args.max_candidates),
        recheck_minutes=max(5, args.recheck_minutes),
        retry_failed_minutes=max(1, args.retry_failed_minutes),
        max_age_hours=max(1, args.max_age_hours),
        max_fail_streak=max(0, args.max_fail_streak),
        tcp_timeout=max(0.3, args.tcp_timeout),
        probe_timeout=max(0.5, args.probe_timeout),
        attempts=max(1, args.attempts),
        attempt_success_threshold=attempt_success_threshold,
        probe_success_per_attempt=probe_success_per_attempt,
        startup_wait_seconds=max(0.05, args.startup_wait_seconds),
        pause_between_attempts=max(0.0, args.pause_between_attempts),
        xray_bin=args.xray_bin,
        allow_tcp_only_fallback=bool(args.allow_tcp_only_fallback),
        dry_run=bool(args.dry_run),
        random_seed=args.random_seed,
        probe_urls=probe_urls,
    )


def main() -> int:
    parser = build_cli()
    args = parser.parse_args()
    config = build_config(args)

    if args.interval_minutes <= 0:
        run_cycle(config)
        return 0

    interval_seconds = max(60, args.interval_minutes * 60)
    log(f"starting daemon mode, interval={args.interval_minutes} minutes")
    while True:
        try:
            run_cycle(config)
        except Exception as exc:
            log(f"cycle failed: {exc}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
