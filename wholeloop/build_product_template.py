"""Build product-template/ from a live product repo (maintainer-only)."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

# Paths relative to product repo root to delete entirely
REMOVE_GLOBS = [
    ".git",
    ".DS_Store",
    "inbox/ARTIFACT-*.md",
    "inbox/*.md",  # catch-all then restore README
    "Progress/adwf-handoffs/2026-*.md",
    "Progress/adwf-handoffs/linear-*.md",
    "Progress/signals/*",
    "Progress/2026-*.md",
    "Releases/2026-*.md",
    "Roadmap/feature-*.md",
    "Roadmap/2026-*.md",
    "Roadmap/linear-*.md",
    "Roadmap/linear-export-*.json",
    "Features/*/ARTIFACT-*.md",
    "Features/*/scope.yaml",
    "Features/*/mockup*.html",
    "Features/*/mockup*.md",
    "Features/*/design-*.md",
    "Features/*/follow-up-*.md",
    "Features/*/posthog-*.md",
    "Features/*/user-stories.md",
    "Features/*/*.html",
    "Interviews/raw/*.md",
    "Interviews/raw/*.txt",
    "Interviews/processed/*.yaml",
    "Interviews/processed/20*.yaml",
    "Surveys/processed/*.yaml",
    "Surveys/processed/20*.yaml",
    "Surveys/synthesis/rollup.yaml",
    "scripts/*.py",
    "Context/source-docs/**/*",
    "Roadmap/pending-features*.md",
    "Analytics/2026-*.md",
    "Analytics/2026-*.json",
    "Analytics/*.json",
    "Product Meetings/themes.md",
]

KEEP_FEATURE_DIRS = {"_template", "README.md"}


def _remove_path(p: Path) -> None:
    if p.is_symlink() or p.is_file():
        p.unlink(missing_ok=True)
    elif p.is_dir():
        shutil.rmtree(p, ignore_errors=True)


def _clear_feature_folders(root: Path) -> None:
    features = root / "Features"
    if not features.is_dir():
        return
    for child in features.iterdir():
        if child.name.startswith(".") or child.name in KEEP_FEATURE_DIRS:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        elif child.is_file() and child.name != "README.md":
            child.unlink(missing_ok=True)


def _clear_context_snapshots(ctx: Path) -> None:
    """Keep README; replace operational snapshots with hand-edited stubs."""
    stubs = {
        "icp-profiles.md": "# ICP profiles\n\n> Hand-edited. Define primary and secondary segments for evidence weighting.\n",
        "capabilities-inventory.md": "# Capabilities inventory\n\n> Hand-edited. What the product can do today (links to repos/services).\n",
        "roadmap-snapshot.md": "# Roadmap snapshot\n\n> Updated by **maintain-roadmap** and PM. Strategy context for agents.\n",
        "product-baseline.md": "# Product baseline\n\n> Hand-edited. Current product state summary.\n",
        "analytics-snapshot.md": "# Analytics snapshot\n\n> Optional. Metrics snapshot for prioritization.\n",
        "data-model-snapshot.md": "# Data model snapshot\n\n> Optional. Key entities for spec/planner agents.\n",
        "org-repositories.md": """# Org repositories

> Hand-edited. Sibling repos and roles for agents.

| Repo | Role |
|------|------|
| **{{APP_REPO}}** | Application delivery (WholeLoop `wholeloop init`) |
| **{{SCRAPER_REPO}}** | Optional data/ingestion service |
| **{{PRODUCT_REPO}}** | This repo — discovery, specs, scope |
""",
        "shipped-inventory.md": "# Shipped inventory\n\n> Agent-assisted from Progress/Releases; PM confirms.\n",
        "signals-sources.md": "# Signals sources\n\n> Where survey/analytics signals come from.\n",
        "sources-index.md": "# Sources index\n\n> Index of Context/source-docs/ when used.\n",
    }
    for name, body in stubs.items():
        (ctx / name).write_text(body, encoding="utf-8")
    src_docs = ctx / "source-docs"
    if src_docs.is_dir():
        shutil.rmtree(src_docs)
    (ctx / "source-docs").mkdir(parents=True, exist_ok=True)
    (ctx / "source-docs" / "README.md").write_text(
        "# Source docs\n\nOptional PDFs, audits, exports referenced from Context/.\n",
        encoding="utf-8",
    )
    for p in ctx.iterdir():
        if p.name.startswith("2026-") or p.name.startswith("ux-audit"):
            _remove_path(p)


def _write_template_files(root: Path) -> None:
    tpl = root / "Features" / "_template"
    tpl.mkdir(parents=True, exist_ok=True)
    (tpl / "scope.yaml").write_text(
        """schema_version: "1.0"
id: example-feature
title: Example feature
created: YYYY-MM-DD
created_by: "PM"
status: candidate

evidence:
  signal_count: 0
  icp_weighted_count: 0
  confidence: low
  confidence_reason: ""
  primary_icp_validated: false
  supporting_interviews: []
  supporting_surveys: []

jtbd:
  primary: >
    When <situation>, I want <motivation>, so I can <outcome>.
  secondary: []

icp:
  primary_segment: ICP1_primary
  secondary_segments: []
  excluded_segments: []
  icp_match_required: ICP1_primary

in_scope:
  - <first deliverable>

out_of_scope:
  - <explicit deferral>

validation_gates:
  - id: gate-1
    question: "<question for PM>"
    status: open
    answer: null

delivery_notes: null
""",
        encoding="utf-8",
    )
    (tpl / "README.md").write_text(
        "Copy this folder to `Features/<slug>/` when starting a feature.\n",
        encoding="utf-8",
    )

    master = root / "Interviews" / "synthesis" / "master.yaml"
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text(
        """schema_version: "1.2"

counts:
  interviews_total: 0
  interviews_icp1: 0
  interviews_icp2: 0
  interviews_anti_icp: 0
  themes_total: 0
  surveys_processed: 0
  survey_respondents_total: 0
  feature_candidates_total: 0

survey_themes: []
interviews: []
themes: []
feature_candidates: []
""",
        encoding="utf-8",
    )

    registry = root / "Surveys" / "registry.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        "schema_version: \"1.0\"\nsurveys: []\n",
        encoding="utf-8",
    )

    for sub in (
        "Progress/signals",
        "Progress/adwf-handoffs",
        "inbox",
        "Interviews/raw",
        "Surveys/raw",
        "Product Meetings/meetings",
        "Product Meetings/meeting-synthesis",
    ):
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not any(d.iterdir()):
            gitkeep.touch()

    _write_generic_docs(root)


def _neutralize_brand_names(text: str) -> str:
    """Remove customer-specific repo/brand names from template text."""
    text = re.sub(r"/Users/[^\s\)]+", "{{WORKSPACE_ROOT}}", text)
    text = text.replace("WALLIU_PRODUCT_ROOT", "PRODUCT_REPO_ROOT")
    for old, new in (
        ("walliu-product", "{{PRODUCT_REPO}}"),
        ("walliu-scraper", "{{SCRAPER_REPO}}"),
        ("Walliu-ai", "{{WORKSPACE_ROOT}}"),
        ("Walliu Scrapers", "{{SCRAPER_REPO}}"),
        ("Walliu Admin", "{{APP_REPO}}-admin"),
        ("Walliu", "{{PRODUCT_NAME}}"),
        ("walliu", "{{APP_REPO}}"),
    ):
        text = text.replace(old, new)
    return text


def _neutralize_agent_playbooks(root: Path) -> None:
    agents = root / "Agents"
    if not agents.is_dir():
        return
    for path in agents.glob("*.md"):
        if path.name == "README.md":
            continue
        text = _neutralize_brand_names(path.read_text(encoding="utf-8"))
        text = text.replace("price-history-ui", "<feature-slug>")
        text = re.sub(
            r"python orchestrator\.py[^\n]*",
            "WholeLoop spec-review in {{APP_REPO}}",
            text,
        )
        path.write_text(text, encoding="utf-8")


def _write_generic_docs(root: Path) -> None:
    (root / "README.md").write_text(
        """# {{PRODUCT_REPO}} — product discovery

**Product discovery** repo: evidence → decisions → roadmap → specs. Production code lives in sibling repos.

## Sibling repos

| Repo | Role |
|------|------|
| **{{APP_REPO}}** | App + WholeLoop delivery (`wholeloop init`) |
| **{{SCRAPER_REPO}}** | Optional ingestion / data service |
| **{{PRODUCT_REPO}}** | This repo |

## Handoff to engineering

When a spec is ready (`build-spec`):

1. `Features/<slug>/ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md`
2. Copy to `{{APP_REPO}}/inbox/` (or path in `Context/org-repositories.md`)
3. Run **spec-review** in the app repo

## PM agents (Cursor)

| Skill | When |
|-------|------|
| `synthesize-interview` | Transcript in `Interviews/raw/` |
| `synthesize-meeting` | Transcript in `Product Meetings/meetings/` |
| `brainstorm-feature` | → `Features/<slug>/scope.yaml` |
| `maintain-roadmap` | → `Context/roadmap-snapshot.md` |
| `build-spec` | → `ARTIFACT-{{ARTIFACT_PREFIX}}-*.md` + `inbox/` |

Install this layout: `wholeloop init-product <path>`
""",
        encoding="utf-8",
    )

    (root / "CLAUDE.md").write_text(
        """# CLAUDE.md — Product discovery (WholeLoop)

This repo is the **system of record for product discovery** for {{PRODUCT_NAME}}.
It stores evidence-backed decisions: interviews, meetings, analytics snapshots, OST, roadmap, and feature specs.
It does **not** contain production application code.

## Flow

Context → Interviews + Surveys → Analytics → Product Meetings → OST → Roadmap → Features → (handoff) {{APP_REPO}}/inbox

## Key paths

- **Features/** — `scope.yaml`, `ARTIFACT-{{ARTIFACT_PREFIX}}-NNN.md`, optional mockups
- **Progress/adwf-handoffs/** — closure summaries after delivery (`handoff` agent in app repo)
- **inbox/** — mirror of approved artifacts before copy to app repo

## Sibling repos

See `Context/org-repositories.md`. App delivery uses WholeLoop v0.2: **spec-review** → planner → …

## Conventions

- Dates: `YYYY-MM-DD` in filenames
- Artifact prefix: `ARTIFACT-{{ARTIFACT_PREFIX}}-NNN` (increment per existing files in `Features/`)
- Quotes in synthesis need `quote_refs`; assumptions go in `risks_and_assumptions`
""",
        encoding="utf-8",
    )

    (root / "Features" / "README.md").write_text(
        """# Features

One folder per feature slug (kebab-case):

```
Features/<slug>/
  scope.yaml
  ARTIFACT-{{ARTIFACT_PREFIX}}-NNN.md
  mockup.html   # optional
```

**Status:** `candidate` → `validating` → `scoped` → `spec-written` → `building` → `shipped`

Skills: `brainstorm-feature`, `build-spec`

Handoff: copy `ARTIFACT-{{ARTIFACT_PREFIX}}-*.md` to `{{APP_REPO}}/inbox/`.
""",
        encoding="utf-8",
    )

    (root / "Progress" / "README.md").write_text(
        """# Progress

Shipped work summaries and ADWF handoff records.

Example filename: `YYYY-MM-DD-{{APP_REPO}}-<feature-slug>.md`

**Repos:** {{APP_REPO}} | {{SCRAPER_REPO}} (if used)

See `Progress/adwf-handoffs/` for per-delivery closure docs (written by **handoff** in app repo).
""",
        encoding="utf-8",
    )

    (root / "Progress" / "adwf-handoffs" / "README.md").write_text(
        """# ADWF handoffs — delivery closure summaries

One markdown file per shipped story or epic. Written by the **handoff** agent in the app repo;
WholeLoop appends `delivery_notes` to `scope.yaml` and may write here via `Progress/adwf-handoffs/`.

Naming: `YYYY-MM-DD-<run-key>-handoff.md`

Use `TEMPLATE-handoff.md` as the starting shape.

Does not replace `Features/<slug>/ARTIFACT-{{ARTIFACT_PREFIX}}-*.md` — this is the operational closure summary.
""",
        encoding="utf-8",
    )

    (root / "Progress" / "adwf-handoffs" / "TEMPLATE-handoff.md").write_text(
        """# ADWF handoff — <story-key>: <short title>

**Date:** YYYY-MM-DD
**Status:** shipped
**Repos:** {{APP_REPO}} (PR), {{PRODUCT_REPO}} (this file)

## Tracker

- **Story:** <PROJ-123> — <title>
- **PR:** <url>

## Acceptance criteria

| AC | Status | Notes |
|----|--------|-------|
| Given … | covered / deferred | … |

## Deviations / deferred

- …

## Workspace

App run folder: `{{APP_REPO}}/workspace/runs/<run-key>/` (preserved or cleaned per team policy).
""",
        encoding="utf-8",
    )

    (root / "Opportunity Solution Tree" / "ost-snapshot.md").write_text(
        "# OST snapshot\n\n> Hand-edited or agent-assisted from `Interviews/synthesis/master.yaml`.\n",
        encoding="utf-8",
    )

    _neutralize_agent_playbooks(root)

    (root / "Releases" / "README.md").write_text(
        """# Releases

Release notes for stakeholders (not a substitute for `Progress/adwf-handoffs/`).

Naming: `YYYY-MM-DD-<epic-or-feature-slug>.md`

Example: `2026-06-01-epic-checkout-v2.md`
""",
        encoding="utf-8",
    )

    inbox_readme = root / "inbox" / "README.md"
    if inbox_readme.is_file():
        inbox_readme.write_text(
            """# Inbox (product repo)

When `build-spec` completes:

1. Writes `Features/<slug>/ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md`
2. Copies to `inbox/ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md`
3. Copy to **`{{APP_REPO}}/inbox/`** (or path in org-repositories.md)

Delivery runs in the app repo via WholeLoop **spec-review** (see `wholeloop init` in {{APP_REPO}}).

Do not commit secrets. Artefacts only.
""",
            encoding="utf-8",
        )


def build_product_template(source: Path, dest: Path) -> None:
    """Copy source product repo to dest and strip operational data."""
    source = source.resolve()
    dest = dest.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Source not found: {source}")

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(
        source,
        dest,
        ignore=shutil.ignore_patterns(
            ".git",
            "__pycache__",
            "*.pyc",
            ".DS_Store",
            "node_modules",
        ),
    )

    for pattern in REMOVE_GLOBS:
        for p in dest.glob(pattern):
            if p.name == "README.md":
                continue
            _remove_path(p)

    _clear_feature_folders(dest)
    _clear_context_snapshots(dest / "Context")
    _write_template_files(dest)

    # Restore inbox README if deleted
    (dest / "inbox" / "README.md").parent.mkdir(parents=True, exist_ok=True)

    _neutralize_tree(dest)

    marker = dest / ".wholeloop-product-template"
    marker.write_text(
        "Generated product template for wholeloop init-product. Rebuild via wholeloop.build_product_template.\n",
        encoding="utf-8",
    )


def _neutralize_tree(root: Path) -> None:
    """Pass over text files and replace any remaining brand-specific strings."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".mdc", ".txt"}:
            continue
        if path.name == ".wholeloop-product-template":
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = _neutralize_brand_names(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    import sys

    src = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("WHOLELOOP_PRODUCT_SOURCE", "")
    )
    if not src:
        print("Usage: python -m wholeloop.build_product_template <source-product-repo> [dest]", file=sys.stderr)
        raise SystemExit(2)
    src = Path(src)
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "product-template")
    build_product_template(src, out)
    print(f"Built {out}")
