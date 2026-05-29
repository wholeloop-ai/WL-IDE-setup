# WholeLoop + VS Code

Same skills and pipeline as **Cursor** and **Claude Code**. Start with **[IDE_SETUP.md](IDE_SETUP.md)**.

## What install creates

| File | Role |
|------|------|
| `WHOLELOOP.md` | Primary instructions — reference this in every Copilot chat for WholeLoop work |
| `.github/copilot-instructions.md` | Repo-wide Copilot context (points to `WHOLELOOP.md`) |
| `.agents/skills/` | Canonical skill prompts |

VS Code does **not** auto-discover `SKILL.md` like Cursor or Claude Code. You invoke agents **explicitly**.

## Example prompts (Copilot Chat)

```
Follow WHOLELOOP.md. Run tracker-intake for SPEC-2025-042 (Linear/Jira MCP or paste cohort table).
```

```
Follow WHOLELOOP.md and spec-validator for story PROJ-128 (or ACME-128).
```

```
Continue WholeLoop from workspace/runs/ACME-128/context.json — run analyser per WHOLELOOP.md.
```

## Issue tracker

**Linear** or **Jira MCP** in VS Code when available. **`manual`**: paste cohort + story AC in chat — same skills. See [TRACKERS.md](TRACKERS.md).

## Optional

- `.vscode/settings.json` — team-specific; not required by WholeLoop.
- Pin `WHOLELOOP.md` in chat context for long sessions.

## Parity tip

Teams often run **spec-validator** and **planner** gates in Cursor or Claude Code (skill discovery), and use VS Code for editing — same `context.json` in git-ignored `workspace/`.
