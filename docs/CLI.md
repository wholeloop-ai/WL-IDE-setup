# WholeLoop CLI

Install WholeLoop into an **app repository** without cloning this template repo or running bash scripts.

Works on **macOS, Linux, and Windows** (use `--copy-ide-skills` if symlinks fail).

## Install the CLI (once per machine)

### macOS (Homebrew Python) — `externally-managed-environment`

Homebrew blocks `pip install` on system Python. Use **pipx** (best for CLI tools):

```bash
brew install pipx
pipx ensurepath
# close and reopen the terminal
pipx install wholeloop-cli==0.1.0
wholeloop version
```

### pipx (recommended)

```bash
pipx install wholeloop-cli==0.1.0
```

From Git (private or before PyPI):

```bash
pipx install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.1.0
```

**Publish to PyPI:** maintainers see [PUBLISHING_CLI.md](PUBLISHING_CLI.md).

### uv

```bash
uv tool install wholeloop-cli
# or
uv tool install git+https://github.com/wholeloop-ai/WL-IDE-setup.git
```

### pip without pipx (not recommended on Homebrew Python)

```bash
python3 -m pip install --user --break-system-packages wholeloop-cli==0.1.0
export PATH="$(python3 -m site --user-base)/bin:$PATH"
```

Or use a dedicated venv and call `wholeloop` via the venv’s `bin/` path.

### pip (virtualenv, contributors)

```bash
python3 -m venv ~/.venvs/wholeloop
source ~/.venvs/wholeloop/bin/activate
pip install wholeloop-cli==0.1.0
```

### Editable (WholeLoop contributors)

```bash
cd WL-IDE-setup
pip install -e .
```

## Use in your app repo

```bash
cd /path/to/your-app
wholeloop init
```

Options:

| Flag | Effect |
|------|--------|
| `--force` / `-f` | Overwrite existing install |
| `--copy-ide-skills` | Copy skills into `.cursor`/`.claude` instead of symlinks |
| `path` | Target directory (default: current directory) |

### Examples

```bash
# Install in current repo
wholeloop init

# Install into another checkout
wholeloop init ~/projects/acme-api

# Windows without symlink support
wholeloop init --copy-ide-skills

# Re-install / refresh templates
wholeloop init --force
```

## Other commands

```bash
wholeloop doctor                      # verify layout, conventions, symlinks
wholeloop conventions bootstrap       # re-extract conventions from README/stack (no AI)
wholeloop update                      # refresh skills; keeps project-conventions.md
wholeloop version
```

### Project conventions (no AI)

`wholeloop init` writes `.agents/skills/references/project-conventions.md` with:

- Repository name (folder or git remote)
- README excerpt, top-level directories
- Detected stack from `package.json`, `pyproject.toml`, `go.mod`, etc.

Then run the **project-conventions** agent in your IDE to confirm and complete. See [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md).

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

1. Run **project-conventions** agent — confirm CLI bootstrap ([PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md)).
2. Product repo: copy `SPEC.template.md` from WholeLoop docs or your vendor package.
3. Enable Linear/Jira MCP in your IDE, or use **manual** story paste — [TRACKERS.md](TRACKERS.md).

## Legacy bash script

`install/copy-skills-to-repo.sh` still works. If `wholeloop` is on `PATH`, the script delegates to `wholeloop init`.

## CI / monorepo

```bash
pipx run wholeloop-cli init ./apps/web --force
```

Pin version: `pipx install wholeloop-cli==0.1.1` (or `uv tool install wholeloop-cli==0.1.1`).
