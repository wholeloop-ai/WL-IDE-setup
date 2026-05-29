# WholeLoop — agentic delivery workflow

> Installed in your **app** repo by `wholeloop init` (CLI: `wholeloop-cli` on PyPI).  
> Works with **Cursor**, **Claude Code**, and **VS Code** (GitHub Copilot). Same skills, same pipeline.

## Before you start

1. **project-conventions** — CLI bootstrap on `init`; run the **project-conventions** agent in IDE to confirm (see `docs/PROJECT_CONVENTIONS.md`).
2. Enable **Linear** or **Jira MCP** in your IDE when not using `manual` mode (see `docs/TRACKERS.md`).
3. Specs live in the **product** repo (`specs/SPEC-*.md`), not in this app repo.

## Skills location (single source of truth)

| Path | Used by |
|------|---------|
| `.agents/skills/<agent>/SKILL.md` | **Canonical** — all IDEs |
| `.cursor/skills/` | Cursor (symlink → `.agents/skills`) |
| `.claude/skills/` | Claude Code (symlink → `.agents/skills`) |

**VS Code:** invoke by name — open `.agents/skills/<agent>/SKILL.md` or ask Copilot to follow `WHOLELOOP.md` and that skill file.

## Pipeline (one Linear story per run)

```text
tracker-intake (optional)   # Linear MCP, Jira MCP, or manual paste
    → spec-validator  [human gate: approve / reject / approve-with-note]
    → analyser
    → planner         [human gate]
    → (optional: ui-ux-designer, migration, ui-tester)
    → builder
    → reviewer
    → pr-agent        [human gate: PR]
    → handoff         (tracker comment via MCP or manual paste)
```

Context file (per story): `workspace/runs/<story-key>/context.json`

## How to invoke each agent

| IDE | How |
|-----|-----|
| **Cursor** | “run **tracker-intake** for SPEC-…”; rules in `.cursor/rules/wholeloop.mdc` |
| **Claude Code** | `/tracker-intake`, `/spec-validator`, … or natural language |
| **VS Code** | Copilot Chat: “Follow `WHOLELOOP.md` and run the **spec-validator** skill from `.agents/skills/spec-validator/SKILL.md` for ACME-128” |

## Typical session

1. **tracker-intake** — `spec_id` or spec path → cohort table (MCP or manual paste).
2. **spec-validator** — active story (e.g. `ACME-128`, `PROJ-101`) → Phase A + Phase B; apply suggestions; then `approve`.
3. **analyser** → **planner** → … → **handoff**.

## Spec-validator (summary)

- **Phase A:** Parent spec in product repo — implementable, complete, conventions.
- **Phase B:** Active story + **all** cohort stories — independent, right size, no contradictions, fits spec, coherent together.
- May **suggest** edits to spec and Linear issues; **never** apply without human confirmation.
- Set `ready_for_analyser: true` in context only after human gate.

## Issue tracker (Linear, Jira, manual)

| Mode | Intake | Handoff |
|------|--------|---------|
| **linear** | Linear MCP | Comment via MCP |
| **jira** | Jira MCP + JQL/labels | Comment via MCP |
| **manual** | Paste cohort table in chat | Paste comment text yourself |

Details: WholeLoop `docs/TRACKERS.md`.

## Product repo

Copy `SPEC.template.md` into product `specs/`. On approval, create stories in your tracker (or maintain list for manual mode).

## More documentation

WholeLoop template repo: `docs/WORKFLOW_PRODUCT_LINEAR.md`, `docs/IDE_CURSOR.md`, `docs/IDE_CLAUDE_CODE.md`, `docs/IDE_VSCODE.md`.
