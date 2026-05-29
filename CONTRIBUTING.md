# Contributing to WholeLoop

(template repo)

## CLI development

```bash
pip install -e .
wholeloop init /tmp/test-app
wholeloop doctor /tmp/test-app
python -m build   # wheel includes agents/ via hatch force-include
```

## Guidelines

- Keep skills **project-agnostic** — use placeholders like “your repo root”, “your stack”, not product names.
- Keep this repo **IDE-only** — do not reintroduce orchestrator/n8n docs unless in a separate experimental branch.
- PRs should update `docs/` and `GUIDELINES.md` when folder names or env vars change.
- Do not commit secrets, `.env` files, or customer-specific artifacts.
