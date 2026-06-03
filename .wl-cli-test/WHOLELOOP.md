# WholeLoop — agentic delivery workflow

> Installed in your **app** repo by `wholeloop init` (CLI: `wholeloop-cli` on PyPI).  
> Works with **Cursor**, **Claude Code**, and **VS Code** (GitHub Copilot). Same skills, same pipeline.

## Before you start

1. **project-conventions** — CLI bootstrap on `init`; run the **project-conventions** agent in IDE to confirm (see `docs/PROJECT_CONVENTIONS.md`).
2. Enable **Linear** or **Jira MCP** in your IDE when not using `manual` mode (see `docs/TRACKERS.md`).
3. Specs (ARTIFACT-WAL) arrive from the **product** repo via `inbox/` or path in conventions.

## Skills location (single source of truth)

| Path | Used by |
|------|---------|
| `.agents/skills/<agent>/SKILL.md` | **Canonical** — all IDEs |
| `.cursor/skills/` | Cursor (symlink → `.agents/skills`) |
| `.claude/skills/` | Claude Code (symlink → `.agents/skills`) |

**VS Code:** invoke by name — open `.agents/skills/<agent>/SKILL.md` or ask Copilot to follow `WHOLELOOP.md` and that skill file.

## Pipeline (v0.2)

```text
spec-review       [human gate]
  → (optional: ui-ux-designer Phase B)  [human gate]
  → planner         [human gate]
  → builder | manual (plan.md live state)
  → reviewer
  → pr-agent        [human gate: PR]
  → handoff
```

Optional: `migration`, `ui-tester`.

Run folder: `workspace/runs/<run-key>/` — see `GUIDELINES.md` for layout.

## How to invoke each agent

| IDE | How |
|-----|-----|
| **Cursor** | “run **spec-review** for ARTIFACT-WAL-042”; rules in `.cursor/rules/wholeloop.mdc` |
| **Claude Code** | `/spec-review`, `/planner`, … or natural language |
| **VS Code** | Copilot Chat: “Follow `WHOLELOOP.md` and run **spec-review** from `.agents/skills/spec-review/SKILL.md`” |

## Typical session

1. **spec-review** — ARTIFACT-WAL and/or epic → `context.json` → human `approve`.
2. *(optional)* **ui-ux-designer Phase B** → `design-notes.md`.
3. **planner** → `plan.md` per story → gate → set `execution_mode` (builder | manual).
4. **builder** or manual execution → **reviewer** → **pr-agent** → gate → **handoff**.

## Issue tracker (Linear, Jira, manual)

| Mode | spec-review | Handoff |
|------|-------------|---------|
| **linear** | Linear MCP | Comment via MCP |
| **jira** | Jira MCP | Comment via MCP |
| **manual** | Paste epic + stories | Paste comment yourself |

Details: WholeLoop `docs/TRACKERS.md`.

## Product repo

Scope → (optional mockup) → build-spec → ARTIFACT-WAL + epic. Copy spec to app `inbox/` before delivery.

## More documentation

WholeLoop template repo: `docs/WORKFLOW_PRODUCT_LINEAR.md`, `docs/IDE_CURSOR.md`, `docs/IDE_CLAUDE_CODE.md`, `docs/IDE_VSCODE.md`.
