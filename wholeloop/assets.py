"""Locate bundled skills and reference templates."""

from __future__ import annotations

from pathlib import Path


def assets_root() -> Path:
    """Wheel install uses _bundle; git checkout / editable install uses repo root."""
    package_dir = Path(__file__).resolve().parent
    bundled = package_dir / "_bundle"
    if (bundled / "agents" / "skills").is_dir():
        return bundled
    repo = package_dir.parent
    if (repo / "agents" / "skills").is_dir():
        return repo
    raise FileNotFoundError(
        "WholeLoop assets not found. Reinstall: uv tool install wholeloop-cli"
    )


def skills_src() -> Path:
    return assets_root() / "agents" / "skills"


def references_dir() -> Path:
    return assets_root() / "references"


def product_template_src() -> Path:
    root = assets_root() / "product-template"
    if not root.is_dir():
        raise FileNotFoundError(
            "Product template not found in CLI bundle. Reinstall: "
            "uv tool install wholeloop-cli --upgrade --force"
        )
    return root
