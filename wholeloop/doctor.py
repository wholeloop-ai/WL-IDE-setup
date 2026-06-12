"""Validate WholeLoop installation in an app repository."""

from __future__ import annotations

from pathlib import Path

from wholeloop import __version__
from wholeloop.conventions import is_bootstrap_pending, product_link_status
from wholeloop.pipeline import (
    PIPELINE_LINE,
    PIPELINE_VERSION,
    REQUIRED_SKILL_DIRS,
    audit_skills,
    is_v02_pipeline_doc,
)


def run_doctor(app: Path) -> tuple[bool, list[str]]:
    app = app.resolve()
    ok = True
    lines: list[str] = []

    def check(condition: bool, pass_msg: str, fail_msg: str) -> None:
        nonlocal ok
        if condition:
            lines.append(f"  ✓ {pass_msg}")
        else:
            lines.append(f"  ✗ {fail_msg}")
            ok = False

    lines.append(f"Checking {app}")
    lines.append(f"  CLI version: wholeloop {__version__} (pipeline v{PIPELINE_VERSION})")
    lines.append("")

    skills = app / ".agents" / "skills"
    check(skills.is_dir(), ".agents/skills/", "missing .agents/skills/ — run: wholeloop init")

    if skills.is_dir():
        missing, legacy, installed = audit_skills(skills)
        for name in REQUIRED_SKILL_DIRS:
            if name in installed:
                lines.append(f"  ✓ skill {name}/")
            else:
                lines.append(f"  ✗ skill {name}/ missing — run: wholeloop update")
                ok = False
        for name in legacy:
            lines.append(
                f"  ✗ legacy skill {name}/ (removed in v0.2) — run: wholeloop update"
            )
            ok = False

    whooleloop = app / "WHOLELOOP.md"
    check(whooleloop.is_file(), "WHOLELOOP.md", "missing WHOLELOOP.md")
    if whooleloop.is_file() and not is_v02_pipeline_doc(whooleloop):
        lines.append(
            "  ⚠ WHOLELOOP.md looks like v0.1 — run: wholeloop update (refreshes docs)"
        )

    runs = app / "workspace" / "runs"
    check(runs.is_dir(), "workspace/runs/", "missing workspace/runs/")

    gitignore = app / ".gitignore"
    if gitignore.exists():
        check(
            "workspace" in gitignore.read_text(encoding="utf-8"),
            ".gitignore lists workspace/",
            ".gitignore should include workspace/",
        )
    else:
        check(False, "", ".gitignore missing (should ignore workspace/)")

    conventions = skills / "references" / "project-conventions.md"
    if conventions.exists():
        text = conventions.read_text(encoding="utf-8")
        if is_bootstrap_pending(conventions):
            lines.append(
                "  ⚠ project-conventions.md — CLI bootstrap only; "
                "run **project-conventions** agent in IDE and approve"
            )
        else:
            lines.append("  ✓ project-conventions.md confirmed")
        check(
            "tracker.provider" in text.lower() or "**provider**" in text,
            "conventions mention issue tracker",
            "add Issue tracker section (linear | jira | manual)",
        )
        if "spec-validator" in text or "tracker-intake" in text:
            lines.append(
                "  ⚠ conventions mention v0.1 agents — update wording to spec-review"
            )
    else:
        check(False, "", "missing references/project-conventions.md")

    linked, value = product_link_status(app)
    if linked:
        ref = value or ""
        resolvable = ref.startswith(("http://", "https://", "git@", "ssh://")) or (
            app / ref
        ).resolve().exists()
        if resolvable:
            lines.append(f"  ✓ product repo linked ({ref})")
        else:
            lines.append(
                f"  ⚠ product repo linked but path not found: {ref} — re-run: wholeloop link"
            )
    else:
        lines.append(
            "  ⚠ product repo not linked — run: wholeloop link <product-path-or-url> "
            "(needed for spec inbox + handoff)"
        )

    for parent in (".cursor", ".claude"):
        link = app / parent / "skills"
        if link.is_symlink():
            lines.append(f"  ✓ {parent}/skills → symlink")
        elif link.is_dir():
            lines.append(f"  ~ {parent}/skills is a copy (OK) or stale — prefer symlink")
        else:
            lines.append(f"  ✗ {parent}/skills missing — re-run: wholeloop init")
            ok = False

    lines.append("")
    if ok:
        lines.append(f"Ready for WholeLoop v{PIPELINE_VERSION}.")
        lines.append(f"  Pipeline: {PIPELINE_LINE}")
        lines.append("  Next: spec-review with product spec and/or epic (docs/TRACKERS.md).")
    else:
        lines.append("Fix issues above, then: wholeloop doctor")

    return ok, lines
