# WholeLoop CLI — reference

Install the CLI: **[install/README.md](../install/README.md)** (uv, pipx, pip, Git).

Works on **macOS, Linux, and Windows** (use `--copy-ide-skills` if symlinks fail).

## Use in your app repo

```bash
cd /path/to/your-app
wholeloop init
```

| Flag | Effect |
|------|--------|
| `--force` / `-f` | Overwrite existing install |
| `--copy-ide-skills` | Copy into `.cursor`/`.claude` instead of symlinks |
| `--conventions-from FILE` | Team `project-conventions.md` instead of CLI README bootstrap |
| `path` | Target directory (default: current directory) |

### Examples

```bash
wholeloop init
wholeloop init ~/projects/acme-api
wholeloop init --copy-ide-skills          # Windows without symlinks
wholeloop init --conventions-from ./team-project-conventions.md
wholeloop init --force
```

## Commands

```bash
wholeloop doctor
wholeloop conventions bootstrap
wholeloop conventions bootstrap --from FILE
wholeloop conventions import FILE
wholeloop update
wholeloop version
```

### Project conventions (no AI)

`wholeloop init` writes `.agents/skills/references/project-conventions.md` (README excerpt, layout, detected stack).

Then run the **project-conventions** agent in your IDE. Details: [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md).

**Team file from a senior dev:**

```bash
wholeloop init --conventions-from ~/Downloads/project-conventions.md
# or after init:
wholeloop conventions import ./project-conventions.md
```

Interactive import on bootstrap (TTY): `wholeloop conventions bootstrap` asks if you have a team file.

## What `init` creates

| Path | Purpose |
|------|---------|
| `.agents/skills/` | Agent prompts (canonical) |
| `.cursor/skills` → `.agents/skills` | Cursor |
| `.claude/skills` → `.agents/skills` | Claude Code |
| `WHOLELOOP.md` | Shared workflow (incl. VS Code) |
| `CLAUDE.md` | Claude Code pointer |
| `.github/copilot-instructions.md` | VS Code Copilot |
| `.cursor/rules/wholeloop.mdc` | Cursor rules |
| `workspace/runs/` | Per-story context (gitignored) |

## After install

1. **project-conventions** agent — confirm or complete conventions.
2. Product repo: `references/SPEC.template.md` → `specs/`.
3. Linear/Jira MCP or manual stories — [TRACKERS.md](TRACKERS.md).

## CI / monorepo

```bash
uvx --from wholeloop-cli==0.1.4 wholeloop init ./apps/web --force
```

See [install/README.md](../install/README.md) for pinned installs.
