"""Per-machine WholeLoop config at ~/.wholeloop/config.json.

Local to each user. Stores the product repo and known app repos so wizards can
suggest paths and `doctor --global` can report the loop. Never committed; never
contains secrets. The per-repo source of truth for agents stays in
`project-conventions.md` — this file only helps the CLI be smart about defaults.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

CONFIG_VERSION = 1


def config_dir() -> Path:
    override = os.environ.get("WHOLELOOP_CONFIG_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".wholeloop"


def config_path() -> Path:
    return config_dir() / "config.json"


def _empty() -> dict:
    return {"version": CONFIG_VERSION, "product_repo": None, "app_repos": []}


def load_config() -> dict:
    path = config_path()
    if not path.is_file():
        return _empty()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return _empty()
    if not isinstance(data, dict):
        return _empty()
    data.setdefault("version", CONFIG_VERSION)
    data.setdefault("product_repo", None)
    data.setdefault("app_repos", [])
    return data


def save_config(data: dict) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data["version"] = CONFIG_VERSION
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def set_product_repo(ref: str) -> None:
    data = load_config()
    data["product_repo"] = ref
    save_config(data)


def get_product_repo() -> str | None:
    return load_config().get("product_repo")


def add_app_repo(path: str) -> None:
    data = load_config()
    apps = list(data.get("app_repos") or [])
    if path not in apps:
        apps.append(path)
    data["app_repos"] = apps
    save_config(data)


def mark_setup_complete() -> None:
    data = load_config()
    data["setup_completed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_config(data)


def record_update_check(latest: str | None) -> None:
    data = load_config()
    data["last_update_check"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if latest:
        data["latest_known_version"] = latest
    save_config(data)


def get_cached_latest() -> str | None:
    return load_config().get("latest_known_version")


def update_check_age_hours() -> float | None:
    """Hours since the last PyPI check, or None if never checked."""
    raw = load_config().get("last_update_check")
    if not raw:
        return None
    try:
        last = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - last
    return delta.total_seconds() / 3600.0
