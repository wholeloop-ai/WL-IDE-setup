# Install `wholeloop-cli`

Package on PyPI: **[wholeloop-cli](https://pypi.org/project/wholeloop-cli/)**  
Command: **`wholeloop`**

**Current release:** `0.1.4` (match [pyproject.toml](../pyproject.toml) when cutting a release)

Install the CLI **once per machine**, then run `wholeloop init` in each app repo. Usage: **[docs/CLI.md](../docs/CLI.md)**.

---

## Recommended — uv

Fast, works well on macOS (including when Homebrew Python blocks `pip install`).

```bash
# Install uv (once)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: brew install uv

# Install WholeLoop CLI
uv tool install wholeloop-cli==0.1.4
wholeloop version
```

**Upgrade:**

```bash
uv tool install wholeloop-cli --upgrade --force
```

**From this repo (contributors or before PyPI):**

```bash
uv tool install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.1.4
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
uv tool install wholeloop-cli==0.1.4 --force \
  --default-index https://pypi.org/simple --index https://pypi.org/simple
```

---

## pipx

Good on Linux and when you prefer isolated Python CLIs.

```bash
python3 -m pip install --user pipx   # if needed
pipx ensurepath
# restart shell

pipx install wholeloop-cli==0.1.4
wholeloop version
```

**Upgrade:** `pipx upgrade wholeloop-cli`

**From Git:**

```bash
pipx install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.1.4
```

---

## pip (virtualenv)

For contributors or locked environments:

```bash
python3 -m venv ~/.venvs/wholeloop
source ~/.venvs/wholeloop/bin/activate
pip install wholeloop-cli==0.1.4
wholeloop version
```

---

## macOS + Homebrew Python

Homebrew Python is **externally managed** — do not `pip install` into it. Use **uv** (above) or **pipx**.

If you must use pip on system Python:

```bash
python3 -m pip install --user --break-system-packages wholeloop-cli==0.1.4
export PATH="$(python3 -m site --user-base)/bin:$PATH"
```

---

## Verify

```bash
which wholeloop
wholeloop version
```

Expected: `wholeloop 0.1.4` (or newer if you used `--upgrade`).

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

---

## CI / monorepo

```bash
uv tool install wholeloop-cli==0.1.4
wholeloop init ./apps/web --force
```

Or one-off without global install:

```bash
uvx --from wholeloop-cli==0.1.4 wholeloop init ./apps/web --force
```

---

## Maintainers

Publishing: [docs/PUBLISHING_CLI.md](../docs/PUBLISHING_CLI.md)

On each release, bump `version` in `pyproject.toml` and the version pins in this file and [README.md](../README.md).
