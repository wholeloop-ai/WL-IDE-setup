# Publishing `wholeloop-cli` for clients

Package name on PyPI: **`wholeloop-cli`**  
Command after install: **`wholeloop`**

## What clients will run

```bash
uv tool install wholeloop-cli
cd their-app
wholeloop init
wholeloop doctor
```

Pin a version in onboarding docs (see [install/README.md](../install/README.md)):

```bash
uv tool install wholeloop-cli==0.3.3
```

---

## Before you publish

### 1. Update `pyproject.toml`

- **`version`** — bump on every release (`0.1.0` → `0.1.1`).
- **`[project.urls]`** — real GitHub org/repo URLs (not placeholders).
- **`authors`** — legal entity or team name if needed.

### 2. PyPI account and token

1. Create account at [https://pypi.org](https://pypi.org).
2. Register the project name **`wholeloop-cli`** (upload first release or reserve via upload).
3. Create an **API token** (scope: entire account or project `wholeloop-cli`).
4. Store the token in a password manager — use it only in CI or local publish, never commit it.

### 3. Install build tools (maintainers)

```bash
python3 -m pip install --user hatch twine
# or
pipx install hatch
```

### 4. Verify the wheel bundles skills

The wheel must include `agents/skills` and `references/` (via hatch `force-include`).

**Run every build from the repo root** (the directory that contains `pyproject.toml`).
If you run `hatch build` from `~` or another folder, Hatch fails with `ValueError: Empty module name`.

```bash
cd /path/to/wholeloop-IDE-setup   # or WL-IDE-setup
uvx hatch build
unzip -l dist/wholeloop_cli-0.2.0-py3-none-any.whl | grep SKILL.md
```

You should see paths under `wholeloop/_bundle/agents/skills/` (including `spec-review/SKILL.md`).

Smoke test locally:

```bash
uv tool install dist/wholeloop_cli-0.2.0-py3-none-any.whl --force
wholeloop version
wholeloop skills
mkdir /tmp/wl-test && wholeloop init /tmp/wl-test
wholeloop doctor /tmp/wl-test
```

---

## Publish to public PyPI

```bash
cd /path/to/wholeloop-IDE-setup
uvx hatch build
uvx hatch publish
```

## Troubleshooting `hatch build`

| Symptom | Cause | Fix |
|---------|--------|-----|
| `ValueError: Empty module name` | Not in the package repo (e.g. ran from `~`) | `cd` to the repo that contains `pyproject.toml`, then `uvx hatch build` |
| Wheel missing `spec-review` | Old dist artifacts or build from wrong branch | `rm -rf dist/` and rebuild from a clean checkout |

`hatch publish` prompts for username `__token__` and password = your PyPI API token.

Alternative with **twine**:

```bash
hatch build
python3 -m twine upload dist/*
```

### TestPyPI (optional dry run)

```bash
hatch build
twine upload --repository testpypi dist/*
pipx install --index-url https://test.pypi.org/simple/ wholeloop-cli
```

---

## Release checklist

1. [ ] Bump `version` in `pyproject.toml`.
2. [ ] Changelog / Git tag `v0.1.0`.
3. [ ] `hatch build` + wheel contains all `SKILL.md` files.
4. [ ] `hatch publish` to PyPI.
5. [ ] Update version pins in `install/README.md`, `README.md`, and related docs.
6. [ ] Smoke test: `uv tool install wholeloop-cli==X.Y.Z` → `wholeloop init` → `wholeloop doctor`.

---

## Options for clients (without public PyPI)

### A — Install from Git (private or public repo)

No PyPI; clients need git + network access:

```bash
pipx install git+https://github.com/wholeloop-ai/WL-IDE-setup.git@v0.1.0
```

Pin the **tag** so installs are reproducible.

### B — Private package index

Host wheels on:

- GitHub Packages (Python)
- AWS CodeArtifact
- Gemfury / Artifactory / Cloudsmith

Clients configure pip/pipx index URL + token; install same package name `wholeloop-cli`.

### C — Vendor the wheel in your onboarding

Attach `wholeloop_cli-0.1.0-py3-none-any.whl` to an internal wiki:

```bash
pipx install ./wholeloop_cli-0.1.0-py3-none-any.whl
```

Good for air-gapped or strict compliance.

---

## CI publish (GitHub Actions example)

Store `PYPI_API_TOKEN` as a repository secret.

```yaml
name: Publish CLI
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # optional: PyPI trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install hatch
      - run: hatch build
      - run: hatch publish -u __token__ -a ${{ secrets.PYPI_API_TOKEN }}
```

Prefer [PyPI trusted publishers](https://docs.pypi.org/trusted-publishers/) (OIDC) instead of long-lived tokens when possible.

---

## After clients install

Point them to:

- [CLI.md](CLI.md) — usage
- [SETUP_NEW_PROJECT.md](SETUP_NEW_PROJECT.md) — app + product repo
- [TRACKERS.md](TRACKERS.md) — Linear / Jira / manual

They do **not** need to clone [WL-IDE-setup](https://github.com/wholeloop-ai/WL-IDE-setup) if they use PyPI or `pipx install wholeloop-cli`.

---

## Updating skills for clients

When you release **0.1.1** with new `SKILL.md` content:

1. Publish new wheel to PyPI.
2. Clients run: `pipx upgrade wholeloop-cli` (or `pipx install wholeloop-cli==0.1.1`).
3. In each app repo: `wholeloop update` (refreshes `.agents/skills/`).

Document that in your client changelog.
