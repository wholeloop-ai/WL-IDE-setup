"""Project-specific naming derived from product metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path

PRODUCT_CONFIG = "wholeloop-product.json"


def artifact_prefix(product_name: str) -> str:
    """Derive a 3–4 letter spec/ticket prefix from the product name.

    Examples: Walliu→WAL, HAYAverse→HAYA, acme→ACM
    """
    name = product_name.strip()
    if not name:
        return "SPEC"
    caps = "".join(c for c in name if c.isupper())
    if len(caps) >= 3:
        return caps[:4]
    slug = re.sub(r"[^a-z0-9]", "", name.lower())
    if not slug:
        return "SPEC"
    return slug[:3].upper()


def spec_id_pattern(prefix: str) -> str:
    return f"ARTIFACT-{prefix}-{{NNN}}"


def write_product_config(dest: Path, product_name: str) -> dict:
    prefix = artifact_prefix(product_name)
    data = {
        "product_name": product_name,
        "artifact_prefix": prefix,
        "spec_id_pattern": spec_id_pattern(prefix),
    }
    (dest / PRODUCT_CONFIG).write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return data


def read_product_config(product_repo: Path) -> dict | None:
    path = product_repo.expanduser().resolve() / PRODUCT_CONFIG
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def read_artifact_prefix(product_repo: Path) -> str | None:
    cfg = read_product_config(product_repo)
    if not cfg:
        return None
    prefix = cfg.get("artifact_prefix")
    return str(prefix) if prefix else None
