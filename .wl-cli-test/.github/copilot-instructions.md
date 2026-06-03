# GitHub Copilot — repository instructions

Follow **[WHOLELOOP.md](../WHOLELOOP.md)** at the repository root for the WholeLoop agentic delivery workflow.

When assisting on features tied to a product spec and user stories (Linear, Jira, or manual):

1. Read `.agents/skills/references/project-conventions.md` (`tracker.provider`).
2. Load skills: `spec-review`, `planner`, `builder`, `reviewer`, `pr-agent`, `handoff` (optional: `ui-ux-designer`).
3. Use Linear/Jira MCP when available; otherwise accept pasted epic/stories at spec-review. Context: `workspace/runs/<run-key>/context.json`.

See repo **`docs/TRACKERS.md`** (if WholeLoop docs are vendored nearby).
4. Respect human gates after spec-review and planner; use `plan.md` as execution state.

This repo uses the same skills as **Cursor** (`.cursor/skills`) and **Claude Code** (`.claude/skills`) via symlink to `.agents/skills/`.
