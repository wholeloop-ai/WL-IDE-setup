# Contributing to WholeLoop

(template repo)

## CLI development

```bash
uv tool install . --force
# or: pip install -e .
wholeloop skills
wholeloop init /tmp/test-app
wholeloop doctor /tmp/test-app
wholeloop update /tmp/test-app
uvx hatch build   # wheel includes agents/ via hatch force-include
```

## Release (maintainers)

1. Bump `version` in `pyproject.toml` and `wholeloop/__init__.py`.
2. Update `CHANGELOG.md`.
3. Pin version in `install/README.md` and `README.md` quick start.
4. `uvx hatch build && uvx hatch publish`
5. Git tag `vX.Y.Z` and push.

## Guidelines

- Keep skills **project-agnostic** — use placeholders like “your repo root”, “your stack”, not product names.
- Keep this repo **IDE-only** — do not reintroduce orchestrator/n8n docs unless in a separate experimental branch.
- PRs should update `docs/`, `install/README.md`, and `GUIDELINES.md` when folder names, install paths, or env vars change.
- Do not commit secrets, `.env` files, or customer-specific artifacts.
- Do not add bash install scripts — clients use `wholeloop-cli` only ([install/README.md](install/README.md)).
