# WholeLoop CLI — reference

Install the CLI: **[install/README.md](../install/README.md)** — macOS: `brew install uv` + `uv tool install wholeloop-cli`; also pipx, pip, Git.

Works on **macOS, Linux, and Windows** (use `--copy-ide-skills` if symlinks fail).

**Current pipeline (v0.2):** `spec-review → [ui-ux-designer B] → planner → builder|manual → reviewer → pr-agent → handoff`

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
wholeloop skills              # bundled agents + v0.2 pipeline (no app repo needed)
wholeloop conventions bootstrap
wholeloop conventions bootstrap --from FILE
wholeloop conventions import FILE
wholeloop update
wholeloop version
```

### `update` (migrate from v0.1)

Refreshes `.agents/skills/` from the installed CLI bundle and, by default, overwrites IDE workflow files so they match v0.2:

- `WHOLELOOP.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `.cursor/rules/wholeloop.mdc`

Keeps your customized `project-conventions.md` unless you pass `--no-keep-conventions`.

| Flag | Effect |
|------|--------|
| `--no-refresh-docs` | Skills only; leave WHOLELOOP.md and IDE instructions unchanged |
| `--no-keep-conventions` | Re-bootstrap conventions from template |
| `--copy-ide-skills` | Copy `.cursor`/`.claude` skills dirs instead of symlinks |

```bash
wholeloop update
wholeloop update --no-refresh-docs   # if you forked WHOLELOOP.md
wholeloop doctor
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
| `.agents/skills/` | Agent prompts (canonical) — includes **spec-review**, **planner**, **builder**, … |
| `.cursor/skills` → `.agents/skills` | Cursor |
| `.claude/skills` → `.agents/skills` | Claude Code |
| `WHOLELOOP.md` | Shared workflow v0.2 (incl. VS Code) |
| `CLAUDE.md` | Claude Code pointer |
| `.github/copilot-instructions.md` | VS Code Copilot |
| `.cursor/rules/wholeloop.mdc` | Cursor rules |
| `workspace/runs/` | Per-run context + plans (gitignored) |

Removed from the bundle in v0.2: `spec-validator`, `analyser`, `tracker-intake` (merged into **spec-review**).

## After install

1. **project-conventions** agent — confirm or complete conventions.
2. Product repo: ARTIFACT-WAL in `inbox/` or path in conventions.
3. **spec-review** with Linear/Jira MCP or manual epic paste — [TRACKERS.md](TRACKERS.md).

## CI / monorepo

```bash
uvx --from wholeloop-cli==0.2.0 wholeloop init ./apps/web --force
```

See [install/README.md](../install/README.md) for pinned installs.
