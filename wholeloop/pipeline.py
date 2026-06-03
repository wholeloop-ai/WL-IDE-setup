"""WholeLoop v0.2 delivery pipeline — skill names and install checks."""

from __future__ import annotations

from pathlib import Path

PIPELINE_VERSION = "0.2"

PIPELINE_LINE = (
    "spec-review → [ui-ux-designer B] → planner → builder|manual "
    "→ reviewer → pr-agent → handoff"
)

REQUIRED_SKILL_DIRS = (
    "spec-review",
    "planner",
    "builder",
    "reviewer",
    "pr-agent",
    "handoff",
    "project-conventions",
)

OPTIONAL_SKILL_DIRS = (
    "ui-ux-designer",
    "migration",
    "ui-tester",
)

REMOVED_SKILL_DIRS = (
    "spec-validator",
    "analyser",
    "tracker-intake",
)

V02_DOC_MARKER = "spec-review"


def list_installed_skills(skills_root: Path) -> list[str]:
    if not skills_root.is_dir():
        return []
    return sorted(
        p.name
        for p in skills_root.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )


def audit_skills(skills_root: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (missing_required, legacy_present, installed_skill_dirs)."""
    installed = list_installed_skills(skills_root)
    installed_set = set(installed)
    missing = [s for s in REQUIRED_SKILL_DIRS if s not in installed_set]
    legacy = [s for s in REMOVED_SKILL_DIRS if s in installed_set]
    return missing, legacy, installed


def is_v02_pipeline_doc(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return V02_DOC_MARKER in text
