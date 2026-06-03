# Install `wholeloop-cli`

Package on PyPI: **[wholeloop-cli](https://pypi.org/project/wholeloop-cli/)**  
Command: **`wholeloop`**

**Current release:** `0.2.1` (match [pyproject.toml](../pyproject.toml) when cutting a release)

Install the CLI **once per machine**, then run `wholeloop init` in each app repo. Usage: **[docs/CLI.md](../docs/CLI.md)**.

There is **no** `brew install wholeloop-cli` in Homebrew core yet — use **uv** or **pipx** via Homebrew (below).
Reason: `wholeloop-cli` is distributed via **PyPI** (Python package index), and `brew` installs formulas/casks from Homebrew taps.

---

## macOS — Homebrew (recommended path)

Install the runtime with Homebrew, then install `wholeloop-cli` from PyPI.

### Option A — uv + PyPI (preferred)

```bash
brew install uv
uv tool install wholeloop-cli==0.2.1
wholeloop version
```

**Upgrade:**

```bash
uv tool install wholeloop-cli --upgrade --force
```

### Option B — pipx + PyPI

```bash
brew install pipx
pipx ensurepath
# restart terminal (or: exec $SHELL -l)

pipx install wholeloop-cli==0.2.1
wholeloop version
```

**Upgrade:** `pipx upgrade wholeloop-cli`

> Do **not** run `pip install wholeloop-cli` into Homebrew’s system Python (`externally-managed-environment`). Use uv or pipx.

---

## uv (all platforms)

Works without Homebrew; good on Linux and in CI.

```bash
# Install uv (once)
curl -LsSf https://astral.sh/uv/install.sh | sh
# macOS with Homebrew:
# brew install uv

uv tool install wholeloop-cli==0.2.1
wholeloop version
```

**Upgrade:**

```bash
uv tool install wholeloop-cli --upgrade --force
```

**From this repo (contributors or before PyPI):**

```bash
uv tool install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.2.1
# editable:
uv tool install /path/to/WL-IDE-setup --force
```

### uv: “No solution found” for a pinned version

If your company uses a **private PyPI mirror**, `uv` may see `wholeloop-cli` there without the latest version. Either upgrade without a pin, or:

```bash
uv tool install wholeloop-cli --upgrade --force --index-strategy unsafe-best-match
```

Or install only from public PyPI for one command:

```bash
uv tool install wholeloop-cli==0.2.1 --force \
  --default-index https://pypi.org/simple --index https://pypi.org/simple
```

---

## pipx (without Homebrew)

```bash
python3 -m pip install --user pipx   # if needed
pipx ensurepath
# restart shell

pipx install wholeloop-cli==0.2.1
wholeloop version
```

**Upgrade:** `pipx upgrade wholeloop-cli`

**From Git:**

```bash
pipx install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.2.1
```

---

## pip (virtualenv)

For contributors or locked environments:

```bash
python3 -m venv ~/.venvs/wholeloop
source ~/.venvs/wholeloop/bin/activate
pip install wholeloop-cli==0.2.1
wholeloop version
```

---

---

## Verify

```bash
which wholeloop
wholeloop version
```

Expected: `wholeloop 0.2.1` (or newer if you used `--upgrade`).

---

## Next steps (app repo)

```bash
cd /path/to/your-app
wholeloop init
wholeloop conventions bootstrap    # optional: refresh or import team file
wholeloop doctor
```

- Conventions: [docs/PROJECT_CONVENTIONS.md](../docs/PROJECT_CONVENTIONS.md)
- Workflow: [docs/WORKFLOW_PRODUCT_LINEAR.md](../docs/WORKFLOW_PRODUCT_LINEAR.md)
- All CLI commands: [docs/CLI.md](../docs/CLI.md)

### Upgrade from v0.1

```bash
uv tool install wholeloop-cli==0.2.1 --upgrade --force
cd /path/to/your-app
wholeloop update          # skills + WHOLELOOP.md + IDE instructions
wholeloop doctor
wholeloop skills          # list bundled agents (optional)
```

Use `wholeloop update --no-refresh-docs` if you customized `WHOLELOOP.md`.

---

## CI / monorepo

```bash
uv tool install wholeloop-cli==0.2.1
wholeloop init ./apps/web --force
```

Or one-off without global install:

```bash
uvx --from wholeloop-cli==0.2.1 wholeloop init ./apps/web --force
```

---

## Maintainers

Publishing: [docs/PUBLISHING_CLI.md](../docs/PUBLISHING_CLI.md)

On each release, bump `version` in `pyproject.toml` and the version pins in this file and [README.md](../README.md).
