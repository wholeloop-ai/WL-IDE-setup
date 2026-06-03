# WholeLoop + VS Code

Same skills and pipeline as **Cursor** and **Claude Code**. Start with **[IDE_SETUP.md](IDE_SETUP.md)**.

## What `wholeloop init` creates

| File | Role |
|------|------|
| `WHOLELOOP.md` | Primary instructions — reference this in every Copilot chat for WholeLoop work |
| `.github/copilot-instructions.md` | Repo-wide Copilot context (points to `WHOLELOOP.md`) |
| `.agents/skills/` | Canonical skill prompts |

VS Code does **not** auto-discover `SKILL.md` like Cursor or Claude Code. You invoke agents **explicitly**.

## Example prompts (Copilot Chat)

```
Follow WHOLELOOP.md. Run spec-review for ARTIFACT-WAL-042 (Linear/Jira MCP or paste epic + stories).
```

```
Follow WHOLELOOP.md and planner for run PROJ-SPEC-042 after spec-review is approved.
```

```
Continue WholeLoop from workspace/runs/PROJ-SPEC-042/PROJ-101/plan.md — run builder per WHOLELOOP.md.
```

## Issue tracker

**Linear** or **Jira MCP** in VS Code when available. **`manual`**: paste epic + stories at spec-review — same skills. See [TRACKERS.md](TRACKERS.md).

## Optional

- `.vscode/settings.json` — team-specific; not required by WholeLoop.
- Pin `WHOLELOOP.md` in chat context for long sessions.

## Parity tip

Teams often run **spec-review** and **planner** gates in Cursor or Claude Code (skill discovery), and use VS Code for editing — same `context.json` in git-ignored `workspace/`.
