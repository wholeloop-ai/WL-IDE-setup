# IDE setup — Cursor, Claude Code, VS Code

WholeLoop uses **one canonical skills tree** (`.agents/skills/`) and wires each IDE to it.

## Install

```bash
uv tool install wholeloop-cli==0.1.4    # see install/README.md for pipx, pip, Git
cd /path/to/your-app
wholeloop init
wholeloop doctor
```

## What `wholeloop init` configures

| Artifact | Cursor | Claude Code | VS Code |
|----------|--------|---------------|---------|
| `.agents/skills/` | ✓ canonical | ✓ canonical | ✓ canonical |
| `.cursor/skills` → symlink | ✓ | — | — |
| `.claude/skills` → symlink | — | ✓ | — |
| `.cursor/rules/wholeloop.mdc` | ✓ | — | — |
| `WHOLELOOP.md` (repo root) | ✓ read | ✓ read | ✓ **primary** for Copilot |
| `.github/copilot-instructions.md` | — | — | ✓ Copilot repo instructions |
| `CLAUDE.md` | — | ✓ project memory | — |
| `workspace/runs/` + `.gitignore` | ✓ | ✓ | ✓ |

## After install

1. `wholeloop conventions bootstrap` or team import — [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md).
2. Run **project-conventions** agent → approve conventions file.
3. **Issue tracker:** Linear MCP, Jira MCP, or `manual` — [TRACKERS.md](TRACKERS.md).
4. Product repo: `references/SPEC.template.md` → `specs/`.

## Per-IDE notes

- **[IDE_CURSOR.md](IDE_CURSOR.md)** — Agent Skills, rules, symlinks.
- **[IDE_CLAUDE_CODE.md](IDE_CLAUDE_CODE.md)** — `/skill` commands, `.mcp.json`, restart after first `.claude/skills/`.
- **[IDE_VSCODE.md](IDE_VSCODE.md)** — Copilot + `WHOLELOOP.md`; explicit skill paths in chat.

## Same workflow everywhere

```text
tracker-intake → spec-validator → analyser → planner → … → handoff
```

Context: `workspace/runs/<story-key>/context.json`.

## Symlinks and Windows

`wholeloop init` uses relative symlinks. On Windows, enable Developer Mode or use:

```bash
wholeloop init --copy-ide-skills
```

Edit **`.agents/skills/`** only — never fork copies under `.cursor/` or `.claude/`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Cursor does not suggest skills | Check `.cursor/skills` symlink; reload window |
| Claude `/spec-validator` missing | Restart Claude Code; verify `.claude/skills` |
| VS Code ignores pipeline | Reference `WHOLELOOP.md` + skill path in first message |
| Drift between folders | Edit `.agents/skills` only; run `wholeloop update` |
