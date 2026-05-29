# Setting up WholeLoop on a new project

**Product spec + stories (Linear / Jira / manual) + IDE skills** — no orchestrator or n8n. See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

## Checklist (app repo)

1. [ ] Install CLI — [install/README.md](../install/README.md) (`uv tool install wholeloop-cli`)
2. [ ] `wholeloop init` in your app repo — [CLI.md](CLI.md)
3. [ ] `wholeloop conventions bootstrap` or `--conventions-from` team file — [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md)
4. [ ] Run **project-conventions** agent in IDE → approve `references/project-conventions.md`
5. [ ] **`workspace/`** in **`.gitignore`** (`wholeloop init` adds it)
6. [ ] **IDEs** — Cursor, Claude Code, VS Code via `wholeloop init` ([IDE_SETUP.md](IDE_SETUP.md))
7. [ ] Tracker: Linear/Jira MCP and/or **manual** — [TRACKERS.md](TRACKERS.md)
8. [ ] App **README**: product spec → stories → WholeLoop per `story_key`
9. [ ] (Optional) **CI** — path filters, forbidden dirs

## Checklist (product repo)

1. [ ] Copy `references/SPEC.template.md` → `specs/SPEC-YYYY-NNN.md`
2. [ ] On approval: create stories in Linear, Jira, or list for manual intake
3. [ ] Link spec in epic description (URL to markdown file)

## IDE workflow (summary)

1. **tracker-intake** — cohort via MCP or manual paste.
2. **spec-validator** — Phase A + Phase B → `approve`.
3. **analyser** → **planner** → … → **handoff**.

Context: `workspace/runs/<story-key>/context.json`.

## Install

```bash
uv tool install wholeloop-cli==0.1.4
cd /path/to/your-app
wholeloop init
wholeloop doctor
```

pipx, pip, Git: **[install/README.md](../install/README.md)**.

## Architecture

[ARCHITECTURE.md](ARCHITECTURE.md) — pipeline, context, gates (IDE-only).
