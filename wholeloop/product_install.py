"""Install WholeLoop product-repo template into a target directory."""

from __future__ import annotations

import shutil
from pathlib import Path

from wholeloop.assets import product_template_src

PRODUCT_MARKER = ".wholeloop-product-template"
PRODUCT_SKILLS_REL = Path(".cursor") / "skills"


def is_product_repo(path: Path) -> bool:
    """Heuristic: a scaffolded or in-use WholeLoop product repo."""
    path = path.resolve()
    if (path / PRODUCT_MARKER).exists():
        return True
    return (path / "Features").is_dir() and (path / PRODUCT_SKILLS_REL).is_dir()


def install_product_repo(
    dest: Path,
    *,
    force: bool = False,
    product_name: str | None = None,
) -> list[str]:
    """Copy sanitized product template to dest. Returns log lines."""
    dest = dest.resolve()
    src = product_template_src()

    lines: list[str] = []

    if dest.exists() and any(dest.iterdir()):
        if not force:
            raise FileExistsError(
                f"{dest} is not empty. Use --force or choose an empty directory."
            )
        shutil.rmtree(dest)
        lines.append(f"remove existing {dest}")

    dest.mkdir(parents=True, exist_ok=True)
    # copytree requires dest empty or not exist; we removed dest if force
    for item in src.iterdir():
        s = item
        d = dest / item.name
        if item.is_dir():
            shutil.copytree(item, d)
        else:
            shutil.copy2(item, d)
    n_files = sum(1 for _ in dest.rglob("*") if _.is_file())
    lines.append(f"write product repo template ({n_files} files)")

    if product_name:
        readme = dest / "README.md"
        if readme.is_file():
            text = readme.read_text(encoding="utf-8")
            text = text.replace("{{PRODUCT_REPO}}", product_name)
            readme.write_text(text, encoding="utf-8")
            lines.append(f"patch README.md (product name: {product_name})")

    lines.append("hint  Open in Cursor — no wholeloop CLI required in product repo")
    lines.append("hint  Next: fill Context/icp-profiles.md → synthesize-interview")
    lines.append("hint  App delivery: wholeloop app init in your app repo (separate)")

    return lines


def update_product_skills(dest: Path) -> list[str]:
    """Refresh ONLY the PM agent skills (.cursor/skills) from the CLI bundle.

    Preserves all generated content (Features/, Interviews/, Progress/, inbox/,
    Context/, …). This is the safe counterpart to init-product for existing repos.
    """
    dest = dest.resolve()
    if not is_product_repo(dest):
        raise FileNotFoundError(
            f"{dest} does not look like a WholeLoop product repo "
            f"(no {PRODUCT_MARKER} or Features/+.cursor/skills). "
            f"Scaffold a new one with: wholeloop product init <path>"
        )

    src = product_template_src()
    src_skills = src / PRODUCT_SKILLS_REL
    if not src_skills.is_dir():
        raise FileNotFoundError("Bundled product template has no .cursor/skills/")

    dst_skills = dest / PRODUCT_SKILLS_REL
    if dst_skills.exists():
        shutil.rmtree(dst_skills)
    shutil.copytree(src_skills, dst_skills)
    n_agents = sum(1 for p in dst_skills.iterdir() if p.is_dir())

    lines = [f"write .cursor/skills/ ({n_agents} PM agents refreshed)"]

    src_agents = src / "Agents"
    if src_agents.is_dir():
        dst_agents = dest / "Agents"
        dst_agents.mkdir(exist_ok=True)
        copied = 0
        for item in src_agents.iterdir():
            if item.is_file():
                shutil.copy2(item, dst_agents / item.name)
                copied += 1
        if copied:
            lines.append(f"write Agents/ ({copied} agent docs refreshed)")

    preserved = [
        d
        for d in ("Features", "Interviews", "Progress", "inbox", "Context", "Roadmap")
        if (dest / d).exists()
    ]
    if preserved:
        lines.append("keep  " + ", ".join(f"{d}/" for d in preserved) + " (untouched)")

    return lines
