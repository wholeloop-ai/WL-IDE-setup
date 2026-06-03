# WholeLoop + Cursor IDE

Same skills as **Claude Code** and **VS Code**. Start with **[IDE_SETUP.md](IDE_SETUP.md)**.

## Install

```bash
uv tool install wholeloop-cli    # install/README.md
cd /path/to/your-app
wholeloop init
```

Creates:

- `.agents/skills/` — canonical
- `.cursor/skills` → symlink to `.agents/skills`
- `.cursor/rules/wholeloop.mdc` — points to `WHOLELOOP.md`
- `WHOLELOOP.md`, `workspace/runs/`

## Usage

- “Follow **WHOLELOOP.md**, run **spec-review** for ARTIFACT-WAL-042” (Linear/Jira MCP or manual paste)
- Enable **Linear** or **Jira MCP** per [TRACKERS.md](TRACKERS.md)

## Rules + skills

Do not edit `.cursor/skills/` directly — change `.agents/skills/` only (shared with other IDEs).

Full workflow: **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)**.
