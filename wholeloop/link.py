"""Connect an app repo to its product repo — the discovery↔delivery loop.

Writes the product reference into the app's project-conventions.md so that
spec-review can find product spec in the product `inbox/` and handoff knows where
to append `delivery_notes`. Also records the pair in ~/.wholeloop/config.json.
"""

from __future__ import annotations

from pathlib import Path

from wholeloop import config as cfg
from wholeloop.conventions import normalize_product_ref, set_product_link


def link_app_to_product(app: Path, product_ref: str) -> list[str]:
    app = app.resolve()
    _, changed = set_product_link(app, product_ref)

    config_value, _, _ = normalize_product_ref(app, product_ref)
    cfg.set_product_repo(config_value)
    cfg.add_app_repo(str(app))

    lines = [f"link  {l}" for l in changed]
    lines.append(f"link  registered in {cfg.config_path()}")
    return lines
