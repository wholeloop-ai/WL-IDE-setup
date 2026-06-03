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
8. [ ] App **README**: ARTIFACT-WAL → spec-review → planner → per-story execution
9. [ ] (Optional) **CI** — path filters, forbidden dirs

## Checklist (product repo)

1. [ ] `Features/<slug>/scope.yaml` from your scoping process
2. [ ] (Optional) **ui-ux-designer Phase A** → `mockup.html`
3. [ ] **build-spec** → ARTIFACT-WAL + epic in tracker (no child stories yet)
4. [ ] Copy ARTIFACT-WAL to app `inbox/`

## Delivery skills (app repo)

| Skill | Repo | Invoked by | When |
|-------|------|-----------|------|
| project-conventions | app | dev (once) | Repo setup |
| spec-review | app | dev | Start of every run |
| ui-ux-designer | both | PM+designer (A) / dev+designer (B) | Optional |
| planner | app | dev | After spec-review gate; mid-run refinement (Mode 4) |
| builder | app | dev | After planner gate (if builder mode chosen) |
| reviewer | app | dev | After all plan steps complete |
| pr-agent | app | dev | After reviewer pass |
| handoff | app | dev | After PR gate |

## IDE workflow (summary)

1. **spec-review** — ARTIFACT-WAL and/or epic → `context.json` + gate.
2. *(optional)* **ui-ux-designer Phase B** → `design-notes.md`.
3. **planner** → `plan.md` per story + gate → builder or manual.
4. **reviewer** → **pr-agent** → gate → **handoff**.

Context: `workspace/runs/<run-key>/context.json`.

## Install

**macOS (Homebrew):**

```bash
brew install uv
uv tool install wholeloop-cli
```

**App repo:**

```bash
cd /path/to/your-app
wholeloop init
wholeloop doctor
```

pipx, pip, Git, upgrades: **[install/README.md](../install/README.md)**.

## Architecture

[ARCHITECTURE.md](ARCHITECTURE.md) — pipeline, context, gates (IDE-only).
