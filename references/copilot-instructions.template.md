# GitHub Copilot — repository instructions

Follow **[WHOLELOOP.md](../WHOLELOOP.md)** at the repository root for the WholeLoop agentic delivery workflow.

When assisting on features tied to a product spec and user stories (Linear, Jira, or manual):

1. Read `.agents/skills/references/project-conventions.md` (`tracker.provider`).
2. Load skills: `tracker-intake`, `spec-validator`, `analyser`, `planner`, `builder`, `reviewer`, `pr-agent`, `handoff`.
3. Use Linear/Jira MCP when available; otherwise accept pasted cohort. Context: `workspace/runs/<story-key>/context.json`.

See repo **`docs/TRACKERS.md`** (if WholeLoop docs are vendored nearby).
4. Respect human gates after spec-validator and planner; do not skip cohort checks.

This repo uses the same skills as **Cursor** (`.cursor/skills`) and **Claude Code** (`.claude/skills`) via symlink to `.agents/skills/`.
