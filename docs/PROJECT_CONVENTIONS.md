# Project conventions — guide for developers

`references/project-conventions.md` is the **single source of truth** every WholeLoop agent reads before acting on your repo.

## Two steps (CLI + agent)

| Step | Tool | AI? | What it does |
|------|------|-----|----------------|
| 1 | **CLI** | No | `wholeloop init` or `wholeloop conventions bootstrap` — repo name, README excerpt, folders, guessed stack **or** import a team file from a senior dev |
| 2 | **Agent** | Yes (your IDE) | Skill **project-conventions** — questions, README/docs review, you **approve** final file |

The CLI **never** calls Claude/OpenAI. It only parses files in the repo.

## Team conventions file (senior → new dev)

A senior dev can share an already-approved `project-conventions.md`. The new dev installs it **instead of** CLI README extraction:

```bash
# During init
wholeloop init --conventions-from ~/Downloads/walliu-project-conventions.md

# After init
wholeloop conventions import ./project-conventions.md
wholeloop conventions bootstrap --from ./project-conventions.md

# Interactive (TTY): bootstrap asks if you have a team file
wholeloop conventions bootstrap
```

The CLI checks the file against the WholeLoop template (sections 1–8, no `{{PROJECT_NAME}}` placeholders). On success it becomes the repo’s first `references/project-conventions.md`. A short `<!-- wholeloop:team-import -->` note is added unless already present.

If the team file still has CLI bootstrap or TODO markers, run **project-conventions** in the IDE to confirm repo-specific details.

## CLI commands

```bash
wholeloop init                    # includes conventions bootstrap
wholeloop init --conventions-from FILE
wholeloop conventions bootstrap   # refresh CLI extraction (may prompt for team file)
wholeloop conventions bootstrap --from FILE
wholeloop conventions import FILE
wholeloop conventions bootstrap --force   # overwrite file (careful)
```

Bootstrap marker in file: `<!-- wholeloop:cli-bootstrap -->`  
Team import marker: `<!-- wholeloop:team-import -->`

## Agent (required before serious pipeline work)

In Cursor / Claude Code / VS Code:

> Run the **project-conventions** skill. Read README and docs, ask me confirming questions, update `references/project-conventions.md`, wait for my **approve**.

The agent must:

- Ask about **tracker** (linear / jira / manual), product repo path, forbidden paths, test commands.
- Not finalize without your explicit **approve**.

After approval, the bootstrap marker is removed.

## How conventions affect other agents

| Agent | Depends on |
|-------|------------|
| tracker-intake | Tracker provider, linking spec ↔ stories |
| spec-validator | Product rules, forbidden areas |
| analyser | Repo layout |
| planner | Allowed paths, routing |
| builder | Stack, tests, code style |
| migration | Migrations directory |
| ui-tester | Dev server URL |
| reviewer / pr-agent | DoD, branch rules |

**Incomplete conventions → agents guess → rework.**

## Maintaining over time

Re-run **project-conventions** agent when:

- New top-level package or service folder
- Stack change (e.g. added Playwright, changed package manager)
- Tracker or product repo path changes

Optionally refresh CLI hints:

```bash
wholeloop conventions bootstrap
```

Then confirm again with the agent (CLI may overwrite — use `--force` only when intentional).
