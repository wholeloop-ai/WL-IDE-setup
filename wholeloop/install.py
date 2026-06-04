"""Install WholeLoop into a target application repository."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from wholeloop.assets import references_dir, skills_src
from wholeloop.conventions import (
    bootstrap_conventions,
    ensure_conventions_layout,
    import_conventions,
)
from wholeloop.pipeline import PIPELINE_LINE, audit_skills, list_installed_skills

IDE_REFERENCE_FILES: tuple[tuple[str, str], ...] = (
    ("WHOLELOOP.md", "WHOLELOOP.template.md"),
    ("CLAUDE.md", "CLAUDE.template.md"),
    (".github/copilot-instructions.md", "copilot-instructions.template.md"),
    (".cursor/rules/wholeloop.mdc", "WHOLELOOP_CURSOR_RULE.template.mdc"),
)

WORKSPACE_GITIGNORE_BLOCK = "\n# WholeLoop ephemeral runs\nworkspace/\n"


def _install_file(
    dest: Path, src: Path, *, force: bool, label: str
) -> str:
    if dest.exists() and not force:
        return f"keep  {label}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return f"write {label}"


def _ensure_gitignore(app: Path) -> str:
    gitignore = app / ".gitignore"
    pattern = re.compile(r"^workspace/?\s*$", re.MULTILINE)
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8")
        if pattern.search(text):
            return "keep  .gitignore (workspace/ already listed)"
        gitignore.write_text(text.rstrip() + WORKSPACE_GITIGNORE_BLOCK, encoding="utf-8")
        return "patch .gitignore (added workspace/)"
    gitignore.write_text("# WholeLoop ephemeral runs\nworkspace/\n", encoding="utf-8")
    return "write .gitignore"


def _link_ide_skills(app: Path, parent: str, *, force: bool, copy_fallback: bool) -> str:
    """Symlink .cursor/skills or .claude/skills → .agents/skills."""
    parent_dir = app / parent
    link = parent_dir / "skills"
    target = app / ".agents" / "skills"
    parent_dir.mkdir(parents=True, exist_ok=True)

    if link.exists() or link.is_symlink():
        if link.is_symlink():
            link.unlink()
        elif force:
            if link.is_dir():
                shutil.rmtree(link)
            else:
                link.unlink()
        else:
            return f"skip  {parent}/skills (exists; use --force)"

    rel = os.path.relpath(target, parent_dir)
    try:
        link.symlink_to(rel, target_is_directory=True)
        return f"link  {parent}/skills → .agents/skills"
    except OSError:
        if not copy_fallback:
            return (
                f"warn  {parent}/skills — symlink failed "
                f"(try --copy-ide-skills or Developer Mode on Windows)"
            )
        if link.exists():
            shutil.rmtree(link) if link.is_dir() else link.unlink()
        shutil.copytree(target, link, dirs_exist_ok=True)
        return f"copy  {parent}/skills (symlink unavailable)"


def sync_reference_files(app: Path, *, force: bool = True) -> list[str]:
    """Refresh WHOLELOOP.md, IDE instructions, and Cursor rules from the CLI bundle."""
    refs = references_dir()
    lines: list[str] = []
    for dest_rel, src_name in IDE_REFERENCE_FILES:
        src = refs / src_name
        if not src.is_file():
            lines.append(f"warn  missing bundle template {src_name}")
            continue
        dest = app / dest_rel
        if dest.exists() and not force:
            lines.append(f"keep  {dest_rel}")
            continue
        lines.append(_install_file(dest, src, force=True, label=dest_rel))
    return lines


def _skills_audit_lines(dest: Path) -> list[str]:
    missing, legacy, _ = audit_skills(dest)
    lines: list[str] = []
    if missing:
        lines.append(f"warn  missing expected skills: {', '.join(missing)}")
    if legacy:
        lines.append(
            f"warn  legacy v0.1 skills still present: {', '.join(legacy)}"
        )
    return lines


def install_app(
    app: Path,
    *,
    force: bool = False,
    copy_ide_skills: bool = False,
    conventions_from: Path | None = None,
) -> list[str]:
    """Install skills and IDE wiring. Returns human-readable log lines."""
    app = app.resolve()
    if not app.exists():
        app.mkdir(parents=True, exist_ok=True)
    if not app.is_dir():
        raise NotADirectoryError(f"Not a directory: {app}")

    dest = app / ".agents" / "skills"
    if dest.exists() and not force:
        raise FileExistsError(
            f"{dest} already exists. Re-run with --force or run: wholeloop update"
        )

    lines: list[str] = []
    src = skills_src()

    app.joinpath(".agents").mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    lines.append(
        f"write .agents/skills/ ({len(list_installed_skills(dest))} skills)"
    )
    lines.extend(_skills_audit_lines(dest))

    ensure_conventions_layout(app)
    try:
        if conventions_from is not None:
            _, conv_line = import_conventions(app, conventions_from, force=True)
        else:
            _, conv_line = bootstrap_conventions(app, force=True)
        lines.append(conv_line)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not set project-conventions.md: {e}") from e
    except ValueError:
        raise

    runs = app / "workspace" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    (runs / ".gitkeep").touch(exist_ok=True)
    lines.append("write workspace/runs/")

    lines.append(_ensure_gitignore(app))

    refs = references_dir()
    lines.append(
        _install_file(app / "WHOLELOOP.md", refs / "WHOLELOOP.template.md", force=force, label="WHOLELOOP.md")
    )
    lines.append(
        _install_file(app / "CLAUDE.md", refs / "CLAUDE.template.md", force=force, label="CLAUDE.md")
    )
    lines.append(
        _install_file(
            app / ".github" / "copilot-instructions.md",
            refs / "copilot-instructions.template.md",
            force=force,
            label=".github/copilot-instructions.md",
        )
    )

    cursor_rule = app / ".cursor" / "rules" / "wholeloop.mdc"
    if not cursor_rule.exists() or force:
        cursor_rule.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(refs / "WHOLELOOP_CURSOR_RULE.template.mdc", cursor_rule)
        lines.append("write .cursor/rules/wholeloop.mdc")
    else:
        lines.append("keep  .cursor/rules/wholeloop.mdc")

    for parent in (".cursor", ".claude"):
        lines.append(
            _link_ide_skills(
                app, parent, force=force, copy_fallback=copy_ide_skills
            )
        )

    lines.append(f"hint  Pipeline v0.2: {PIPELINE_LINE}")
    lines.append("hint  Run project-conventions agent in IDE to confirm and complete conventions")

    return lines


def update_skills(
    app: Path,
    *,
    keep_conventions: bool = True,
    copy_ide_skills: bool = False,
    refresh_docs: bool = True,
) -> list[str]:
    """Refresh .agents/skills from the CLI bundle; optionally keep project-conventions.md."""
    app = app.resolve()
    dest = app / ".agents" / "skills"
    if not dest.is_dir():
        raise FileNotFoundError(f"{dest} not found — run: wholeloop init")

    conventions = dest / "references" / "project-conventions.md"
    backup = (
        conventions.read_text(encoding="utf-8")
        if keep_conventions and conventions.exists()
        else None
    )

    shutil.rmtree(dest)
    shutil.copytree(skills_src(), dest)
    lines = [
        f"write .agents/skills/ ({len(list_installed_skills(dest))} skills refreshed)"
    ]
    lines.extend(_skills_audit_lines(dest))

    if refresh_docs:
        lines.extend(sync_reference_files(app, force=True))

    # Self-heal scaffolding that older installs (or update-only repos) may lack.
    runs = app / "workspace" / "runs"
    if not runs.is_dir():
        runs.mkdir(parents=True, exist_ok=True)
        (runs / ".gitkeep").touch(exist_ok=True)
        lines.append("write workspace/runs/")
    lines.append(_ensure_gitignore(app))

    ensure_conventions_layout(app)
    if backup is not None:
        conventions.write_text(backup, encoding="utf-8")
        lines.append("keep  project-conventions.md")
    else:
        try:
            _, conv_line = bootstrap_conventions(app, force=True)
            lines.append(conv_line)
        except FileNotFoundError:
            lines.append("warn  run: wholeloop conventions bootstrap")

    for parent in (".cursor", ".claude"):
        lines.append(
            _link_ide_skills(
                app, parent, force=True, copy_fallback=copy_ide_skills
            )
        )

    lines.append(f"hint  Pipeline v0.2: {PIPELINE_LINE}")
    lines.append("hint  Run project-conventions agent in IDE to confirm conventions")

    return lines
