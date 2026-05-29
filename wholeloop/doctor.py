"""Validate WholeLoop installation in an app repository."""

from __future__ import annotations

from pathlib import Path

from wholeloop.conventions import is_bootstrap_pending


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
    lines.append("")

    skills = app / ".agents" / "skills"
    check(skills.is_dir(), ".agents/skills/", "missing .agents/skills/ — run: wholeloop init")

    whooleloop = app / "WHOLELOOP.md"
    check(whooleloop.is_file(), "WHOLELOOP.md", "missing WHOLELOOP.md")

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
    else:
        check(False, "", "missing references/project-conventions.md")

    for parent in (".cursor", ".claude"):
        link = app / parent / "skills"
        if link.is_symlink():
            lines.append(f"  ✓ {parent}/skills → symlink")
        elif link.is_dir():
            lines.append(f"  ~ {parent}/skills is a copy (OK) or stale — prefer symlink")
        else:
            lines.append(f"  ✗ {parent}/skills missing — re-run: wholeloop init")

    lines.append("")
    if ok:
        lines.append("Ready for WholeLoop. Next: enable Linear/Jira MCP or use manual mode (docs/TRACKERS.md).")
    else:
        lines.append("Fix issues above, then: wholeloop doctor")

    return ok, lines
