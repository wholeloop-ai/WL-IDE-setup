# IDE setup — Cursor, Claude Code, VS Code

WholeLoop uses **one canonical skills tree** (`.agents/skills/`) and wires each IDE to it. Run once per app repo:

```bash
pipx install wholeloop-cli    # or from git — see CLI.md
cd /path/to/your-app
wholeloop init
```

## What the install script configures

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

1. Fill `.agents/skills/references/project-conventions.md`.
2. Configure **issue tracker**: Linear MCP, Jira MCP, or `manual` — [TRACKERS.md](TRACKERS.md).
3. Product repo: add specs from `references/SPEC.template.md`.

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

Install uses relative symlinks (`../.agents/skills`). On Windows, enable Developer Mode or run Git Bash as admin, or copy skills instead of symlinking (document in README — duplicate `.agents/skills` only, do not fork edits).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Cursor does not suggest skills | Check `.cursor/skills` symlink; reload window |
| Claude `/spec-validator` missing | Restart Claude Code after install; verify `.claude/skills` |
| VS Code ignores pipeline | Reference `WHOLELOOP.md` + full path to `SKILL.md` in first message |
| Drift between folders | Never edit `.cursor/skills` directly — edit `.agents/skills` only |
