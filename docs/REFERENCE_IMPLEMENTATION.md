# Reference implementation (Walliu)

This **`wholeloop`** repository is the **portable template** (skills + docs). A **full production orchestrator** (Python, gates, Linear handoff, inbox watcher, n8n hooks) lives in the Walliu application repo as a **reference** you can copy and adapt.

## What to copy

| From Walliu `walliu` repo | Into your project |
|---------------------------|-------------------|
| `orchestrator.py` | Same name at app root (or `scripts/wholeloop/`). |
| `orchestrator_server.py` | If you need HTTP triggers. |
| `n8n/` flows (if any) | Only if you use n8n. |
| `.agents/skills/` | Merge with this template’s skills — Walliu may be ahead. |

## What to change

1. Replace Walliu-specific checks in **spec-validator** / **reviewer** with your product rules.
2. Replace `persist_handoff_markdown` paths (`WALLIU_PRODUCT_ROOT`, etc.) with your env names (e.g. `WHOLELOOP_HANDOFF_ROOT`) — or keep Walliu names for compatibility when merging upstream.
3. **ui-tester** — dev server URL, test framework (Selenium vs Playwright).
4. **pr-agent** — branch naming, default base branch, labels.

## Staying in sync

When Walliu improves WholeLoop:

1. Cherry-pick orchestrator fixes.
2. Port **generic** prompt changes back into `github.com/…/wholeloop` so other products benefit.

## License

Walliu’s orchestrator is part of their app repo — respect their license when copying files.
