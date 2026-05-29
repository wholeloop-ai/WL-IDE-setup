# WholeLoop + Claude Code

Same skills as **Cursor** and **VS Code**. Start with **[IDE_SETUP.md](IDE_SETUP.md)**.

## Install

```bash
bash wholeloop/install/copy-skills-to-repo.sh /path/to/your-app
```

Creates:

- `.agents/skills/` — canonical
- `.claude/skills` → symlink to `.agents/skills`
- `CLAUDE.md` + `WHOLELOOP.md`
- `workspace/runs/`

## Usage

- `/tracker-intake`, `/spec-validator`, …
- Configure **Linear** or **Jira** in `.mcp.json`, or use `manual` — [TRACKERS.md](TRACKERS.md)

## First-time note

Restart Claude Code after the install **creates** `.claude/skills/` so the directory watcher picks up skills.

## Shared repo with Cursor/VS Code

Never edit `.claude/skills/` directly — edit `.agents/skills/` only.

Full workflow: **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)**.
