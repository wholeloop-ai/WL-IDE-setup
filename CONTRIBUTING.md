# Contributing to WholeLoop

(template repo)

## CLI development

```bash
uv tool install . --force
# or: pip install -e .
wholeloop skills
wholeloop product init /tmp/test-product --name test --no-git -y
wholeloop app init /tmp/test-app --product /tmp/test-product -y
wholeloop doctor /tmp/test-app
wholeloop app update /tmp/test-app
wholeloop product update /tmp/test-product
wholeloop link /tmp/test-product /tmp/test-app
# end-to-end wizards without prompts use WHOLELOOP_NO_PROMPT=1 and WHOLELOOP_CONFIG_DIR
WHOLELOOP_PRODUCT_SOURCE=/path/to/source-repo python3 -m wholeloop.build_product_template $WHOLELOOP_PRODUCT_SOURCE product-template
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
