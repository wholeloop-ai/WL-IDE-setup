# Workflow: product spec + user stories

Specs in a **product** repo; stories in **Linear**, **Jira**, or **manual paste**; implementation in an **app** repo with Cursor, Claude Code, or VS Code. No WholeLoop server, n8n, or Python runner to deploy.

> Tracker setup: **[TRACKERS.md](TRACKERS.md)** · IDE setup: **[IDE_SETUP.md](IDE_SETUP.md)**

## Overview

```text
Product repo                    Issue tracker                  App repo
─────────────                   ─────────────                  ────────
specs/SPEC-042.md  ──approve──► Stories (Linear/Jira/manual) ──► .agents/skills/
(status: approved)              linked to spec                 workspace/runs/
```

1. PM authors spec from `references/SPEC.template.md`.
2. After approval, create stories in Linear, Jira, or keep list for **manual** intake.
3. Developer runs **tracker-intake** (MCP or paste cohort).
4. **spec-validator** → human gate → **analyser** → **planner** → … → **handoff**.

## Linking spec ↔ stories

Document in app `project-conventions.md` → **Issue tracker**.

| Provider | Typical link |
|----------|----------------|
| **linear** | Label `spec:SPEC-2025-042`, epic parent |
| **jira** | Epic link, label, or JQL |
| **manual** | Spec §6 breakdown + pasted table at intake |

Spec frontmatter:

```yaml
spec_id: SPEC-2025-042
tracker_provider: linear
tracker_label: spec:SPEC-2025-042
```

## Per-story context

`workspace/runs/<story-key>/context.json` (e.g. `ACME-128`, `PROJ-101`).

## IDE setup (all three)

```bash
wholeloop init    # after: pipx install wholeloop-cli — see CLI.md
```

| IDE | Skills | Instructions |
|-----|--------|----------------|
| Cursor | `.cursor/skills` → `.agents/skills` | `WHOLELOOP.md` |
| Claude Code | `.claude/skills` → `.agents/skills` | `CLAUDE.md` |
| VS Code | `.agents/skills/` | `WHOLELOOP.md` + Copilot instructions |

## Typical session

1. **tracker-intake** for `SPEC-2025-042` (or paste cohort if `manual`).
2. **spec-validator** on active `story_key`.
3. Human applies suggestions → `approve`.
4. **analyser** → **planner** → … → **handoff**.

## Spec-validator

| Phase | Validates | Can suggest |
|-------|-----------|-------------|
| **A** | Spec implementable | Spec PR |
| **B** | Story + cohort | Spec + tracker issues |

## Checklists

**Product repo:** `specs/`, `spec_id` naming, stories after approval.

**App repo:** [SETUP_NEW_PROJECT.md](SETUP_NEW_PROJECT.md), [TRACKERS.md](TRACKERS.md).
