# Setting up WholeLoop on a new project

**Product spec + stories (Linear / Jira / manual) + IDE skills** — no orchestrator or n8n. See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

## Checklist (app repo)

1. [ ] Install WholeLoop: `wholeloop init` in your app repo ([CLI.md](CLI.md)) — or legacy bash script
2. [ ] Fill **`references/project-conventions.md`** — stack, **issue tracker** (`linear` \| `jira` \| `manual`), product repo path.
3. [ ] Add **`workspace/runs/`** (install script creates it) and **`workspace/`** to **`.gitignore`**.
4. [ ] **IDEs** — install script configures Cursor, Claude Code, and VS Code together ([IDE_SETUP.md](IDE_SETUP.md))
5. [ ] Configure tracker: Linear/Jira MCP and/or **manual** paste — [TRACKERS.md](TRACKERS.md).
6. [ ] Document in app **README**: product spec → stories → WholeLoop per `story_key`.
7. [ ] (Optional) **CI** — path filters, forbidden dirs.

## Checklist (product repo)

1. [ ] Copy `references/SPEC.template.md` → `specs/SPEC-YYYY-NNN.md`
2. [ ] On approval: create stories in Linear, Jira, or list for manual intake
3. [ ] Link spec in epic description (URL to markdown file)

## IDE workflow (summary)

1. **tracker-intake** — cohort via MCP or manual paste.
2. **spec-validator** — Phase A + Phase B → `approve`.
3. **analyser** → **planner** → … → **handoff**.

Context: `workspace/runs/<story-key>/context.json`.

## Install (CLI — recommended)

```bash
pipx install wholeloop-cli   # https://pypi.org/project/wholeloop-cli/
cd /path/to/your-app
wholeloop init
wholeloop doctor
```

See **[CLI.md](CLI.md)** for `update`, `--force`, Windows `--copy-ide-skills`.

Legacy: `bash wholeloop/install/copy-skills-to-repo.sh /path/to/app` (uses CLI if installed).

## Architecture

[ARCHITECTURE.md](ARCHITECTURE.md) — pipeline, context, gates (IDE-only).
