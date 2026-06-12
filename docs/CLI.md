# WholeLoop CLI — reference

Install the CLI: **[install/README.md](../install/README.md)** — macOS: `brew install uv` + `uv tool install wholeloop-cli`; also pipx, pip, Git.

Works on **macOS, Linux, and Windows** (use `--copy-ide-skills` if symlinks fail).

**Current pipeline (v0.2):** `spec-review → [ui-ux-designer B] → planner → builder|manual → reviewer → pr-agent → handoff`

The CLI uses a **noun-verb** shape: `wholeloop product …` and `wholeloop app …`. `init`, `init-product`, and `update` still work as aliases. Run `wholeloop` with no command for a role-oriented welcome.

## Setup by role

| Role | Command | Outcome |
|------|---------|---------|
| **PM** | `wholeloop product init` | Scaffold the product repo (system of record) |
| **Dev** | `wholeloop app init --product <path\|url>` | Install delivery skills **and** link to the product repo |
| **Dev (later)** | `wholeloop link <product> [app]` | Connect an already-installed app to a product repo |
| **Founder** | `wholeloop setup` | Product repo + one or more app repos in one flow |

In a terminal these are **interactive** (they ask, with sensible defaults). Pass `--yes` / `-y`, or set `WHOLELOOP_NO_PROMPT=1`, to skip prompts in CI.

### `wholeloop setup` (founder one-shot)

```bash
wholeloop setup                                   # interactive
wholeloop setup \
  --new-product ~/work/acme-product --name acme \
  --app ~/work/acme-api --app ~/work/acme-scraper # non-interactive
```

Walks: product repo (create / existing / skip) → app repo(s) → links each app to the product → `doctor` summary.

### Product repo (`wholeloop product`)

Durable home for scope, specs, interviews, and delivery history (no application code). Required for the full loop.

```bash
wholeloop product init ~/projects/acme-product --name acme
wholeloop product init ~/projects/acme-product --force   # replace non-empty dir (destructive)
wholeloop product update ~/projects/acme-product         # refresh PM skills only
```

| Command | Effect |
|---------|--------|
| `product init [path]` | Scaffold a **new** product repo (`.cursor/skills/`, `Features/`, `Context/`, …). Prompts for name/path/git in a TTY. |
| `product update [path]` | Refresh **only** `.cursor/skills/` and `Agents/`. **Never** touches `Features/`, `Interviews/`, `Progress/`, `inbox/`, `Context/`. |

> `product init --force` deletes the target directory. **Do not** use it on a repo that already has product content — use `product update` to refresh skills.

### App repo (`wholeloop app`)

```bash
cd /path/to/acme-api
wholeloop app init --product ../acme-product
```

| Flag | Effect |
|------|--------|
| `--product REF` | Product repo path or git URL to link (writes into conventions) |
| `--force` / `-f` | Overwrite existing install |
| `--copy-ide-skills` | Copy into `.cursor`/`.claude` instead of symlinks |
| `--conventions-from FILE` | Team `project-conventions.md` instead of CLI bootstrap |
| `--yes` / `-y` | No prompts; use defaults |
| `path` | Target directory (default: current directory) |

Without `--product`, an interactive run offers your last-used product repo (from `~/.wholeloop/config.json`), a custom path/URL, or skip.

### Link an app to its product (`wholeloop link`)

```bash
wholeloop link ../acme-product               # from inside the app repo
wholeloop link ../acme-product ~/work/acme-api
wholeloop link https://github.com/acme/acme-product
```

Rewrites `project-conventions.md` §2 (product path), §5 (default spec path → `<product>/inbox/`), and §8 (link). This is what lets the app **feed** the product repo: spec-review reads the inbox; handoff appends `delivery_notes`.

## Commands

```bash
wholeloop setup                 # guided: product + app(s)
wholeloop product init <path>   # product repo (new)
wholeloop product update [path] # refresh PM skills (keeps content)
wholeloop app init [path]       # app repo (delivery) + --product link
wholeloop app update [path]     # refresh delivery skills + IDE docs
wholeloop link <product> [app]  # connect app → product
wholeloop doctor [path]         # verify app repo (incl. product link)
wholeloop skills                # bundled agents + v0.2 pipeline
wholeloop conventions bootstrap [--from FILE]
wholeloop conventions import FILE
wholeloop version

# aliases
wholeloop init          # = app init
wholeloop init-product  # = product init
wholeloop update        # = app update
```

### `app update` (also: `update` — migrate from v0.1)

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
wholeloop app update
wholeloop app update --no-refresh-docs   # if you forked WHOLELOOP.md
wholeloop doctor
```

### Upgrade notices

Status commands (`version`, `doctor`, `setup`, `app update`, `product update`, and the bare `wholeloop` welcome) check PyPI **at most once a day** and, if a newer release exists, print a one-line hint with two steps:

```text
↑ WholeLoop 0.3.4 is available (you have 0.3.3).
  Upgrade the CLI:   uv tool install wholeloop-cli --upgrade --force
  Then in your repo: wholeloop app update        # or product update, by repo type
```

The "then in your repo" command is chosen from where you are: a product repo → `wholeloop product update`, an app repo → `wholeloop app update`. The check is best-effort (never blocks or fails a command), is skipped on non-interactive output, and can be turned off with `WHOLELOOP_NO_UPDATE_CHECK=1`.

### Machine config (`~/.wholeloop/config.json`)

`setup`, `app init --product`, and `link` record your product repo and app repos so the CLI can suggest sensible defaults next time. It's **local to your machine**, never committed, and holds no secrets. The per-repo source of truth for agents stays in each app's `project-conventions.md`.

Override the location with `WHOLELOOP_CONFIG_DIR` (useful in CI).

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
2. Product repo: product spec in `inbox/` or path in conventions.
3. **spec-review** with Linear/Jira MCP or manual epic paste — [TRACKERS.md](TRACKERS.md).

## CI / monorepo

```bash
uvx --from wholeloop-cli==0.3.3 wholeloop app init ./apps/web --force
```

See [install/README.md](../install/README.md) for pinned installs.
