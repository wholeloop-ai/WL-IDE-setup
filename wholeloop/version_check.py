"""Best-effort 'a newer WholeLoop is available' notice.

Mirrors how gh / npm behave: cached, non-blocking, never fails a command, easy
to opt out. The PyPI query runs at most once per `CHECK_INTERVAL_HOURS` and only
on status-style commands; everything else reads the cached result.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

from wholeloop import __version__, config as cfg
from wholeloop.product_install import is_product_repo

PYPI_JSON_URL = "https://pypi.org/pypi/wholeloop-cli/json"
CHECK_INTERVAL_HOURS = 24.0
NETWORK_TIMEOUT_S = 1.5


def _opted_out() -> bool:
    if os.environ.get("WHOLELOOP_NO_UPDATE_CHECK"):
        return True
    # Keep CI / piped output clean.
    return not sys.stdout.isatty()


def parse_version(s: str | None) -> tuple[int, ...]:
    if not s:
        return ()
    head = s.strip().split("+", 1)[0]
    parts: list[int] = []
    for chunk in head.split("."):
        num = ""
        for ch in chunk:
            if ch.isdigit():
                num += ch
            else:
                break
        if num == "":
            break
        parts.append(int(num))
    return tuple(parts)


def is_newer(latest: str | None, current: str) -> bool:
    lv, cv = parse_version(latest), parse_version(current)
    return bool(lv) and lv > cv


def fetch_latest_version() -> str | None:
    try:
        req = urllib.request.Request(
            PYPI_JSON_URL, headers={"User-Agent": f"wholeloop-cli/{__version__}"}
        )
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT_S) as resp:
            data = json.load(resp)
        return (data.get("info") or {}).get("version")
    except Exception:  # noqa: BLE001 — never let a version check break the CLI
        return None


def cli_upgrade_command() -> str:
    exe = str(Path(sys.executable).resolve())
    if "pipx" in exe:
        return "pipx upgrade wholeloop-cli"
    return "uv tool install wholeloop-cli --upgrade --force"


def repo_update_command(repo_path: Path | None) -> str:
    """Pick the right per-repo update command for where the user is."""
    if repo_path is not None:
        p = repo_path.resolve()
        if is_product_repo(p):
            return "wholeloop product update"
        if (p / ".agents" / "skills").is_dir():
            return "wholeloop app update"
    return "wholeloop app update   (or: wholeloop product update)"


def _resolve_latest(allow_network: bool) -> str | None:
    if allow_network:
        age = cfg.update_check_age_hours()
        if age is None or age >= CHECK_INTERVAL_HOURS:
            latest = fetch_latest_version()
            cfg.record_update_check(latest)
            if latest:
                return latest
    return cfg.get_cached_latest()


def upgrade_notice_lines(repo_path: Path | None, *, allow_network: bool) -> list[str]:
    """Return hint lines if a newer version exists, else []. Never raises."""
    try:
        if _opted_out():
            return []
        latest = _resolve_latest(allow_network)
        if not is_newer(latest, __version__):
            return []
        return [
            "",
            f"  ↑ WholeLoop {latest} is available (you have {__version__}).",
            f"    Upgrade the CLI:   {cli_upgrade_command()}",
            f"    Then in your repo: {repo_update_command(repo_path)}",
            "    (silence: WHOLELOOP_NO_UPDATE_CHECK=1 · details: wholeloop --help)",
        ]
    except Exception:  # noqa: BLE001
        return []


def print_upgrade_notice(repo_path: Path | None = None, *, allow_network: bool = True) -> None:
    for line in upgrade_notice_lines(repo_path, allow_network=allow_network):
        print(line)
