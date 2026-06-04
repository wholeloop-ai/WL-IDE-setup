# Setting up WholeLoop on a new project

WholeLoop assumes a **product repo** (durable product truth) and at least one **app repo** (code + delivery pipeline). No orchestrator or n8n. See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

> **Fastest path (founder):** `wholeloop setup` runs the product + app checklists below as one guided flow and links them automatically.

## Checklist (machine + product repo first)

1. [ ] Install CLI — [install/README.md](../install/README.md) (`uv tool install wholeloop-cli`)
2. [ ] **Product repo** — `wholeloop product init <path> --name <name>` for a **new** repo ([CLI.md](CLI.md))
3. [ ] Fill `Context/` (ICP, roadmap pointers) and start `Features/<slug>/scope.yaml`
4. [ ] (Optional) **ui-ux-designer Phase A** → `mockup.html`
5. [ ] **build-spec** → ARTIFACT-WAL + epic in tracker (no child stories yet)
6. [ ] Product `inbox/` or copy path documented for the app team

> **Existing product repo:** do **not** run `product init --force` — it deletes all `Features/`, `Interviews/`, `Progress/`, etc. Refresh PM skills safely with `wholeloop product update`.

## Checklist (app repo)

1. [ ] `wholeloop app init --product <product-path>` in your app repo — [CLI.md](CLI.md)
2. [ ] Confirm the **product link** (or run `wholeloop link <product>`) — `wholeloop doctor` checks it
3. [ ] `wholeloop conventions bootstrap` or `--conventions-from` — tracker + stack — [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md)
4. [ ] Run **project-conventions** agent in IDE → approve `references/project-conventions.md`
5. [ ] **`workspace/`** in **`.gitignore`** (`wholeloop app init` adds it)
6. [ ] **IDEs** — Cursor, Claude Code, VS Code ([IDE_SETUP.md](IDE_SETUP.md))
7. [ ] Tracker: Linear/Jira MCP and/or **manual** — [TRACKERS.md](TRACKERS.md)
8. [ ] App **README**: ARTIFACT-WAL / epic → spec-review → planner → per-story execution
9. [ ] (Optional) **CI** — path filters, forbidden dirs

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
wholeloop setup        # guided: product repo + app repo(s), linked
```

Or by role:

```bash
wholeloop product init ~/projects/my-product --name my-product
cd /path/to/your-app
wholeloop app init --product ~/projects/my-product
wholeloop doctor
```

pipx, pip, Git, upgrades: **[install/README.md](../install/README.md)**.

## Architecture

[ARCHITECTURE.md](ARCHITECTURE.md) — pipeline, context, gates (IDE-only).
