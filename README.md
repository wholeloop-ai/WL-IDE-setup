# WholeLoop

**WholeLoop** is an **agentic delivery workflow** (ADWF) built around a **product repository** (scope, specs, interviews, delivery history) and one or more **app repositories** (code + gated delivery). Stories live in Linear, Jira, or a manual list; agents run in the IDE — spec → plan → ship → handoff back to product.

Portable **skills + CLI + docs**. No background orchestrator, no n8n — **Cursor**, **Claude Code**, or **VS Code**.

## What you get

| Area | In this repo |
|------|----------------|
| **Skills** | `agents/skills/*/SKILL.md` |
| **CLI** | `wholeloop-cli` on PyPI → `setup` · `product init` · `app init` — [install/](install/) · [docs/CLI.md](docs/CLI.md) |
| **Product template** | `product-template/` · `wholeloop product init` |
| **Trackers** | [docs/TRACKERS.md](docs/TRACKERS.md) — Linear, Jira, manual |
| **Spec template** | `references/SPEC.template.md` (product repo) |
| **Conventions** | `references/PROJECT_CONVENTIONS.template.md` |
| **Workflow** | [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md) |

## Principles

1. **Product repo is the center** — Durable truth: `Features/`, interviews, inbox, `delivery_notes` after handoff. Not optional for a full WholeLoop loop.
2. **App repo executes delivery** — Code plus `workspace/runs/` (ephemeral); skills via `wholeloop app init` / `app update`.
3. **Stories in the tracker** — Linear, Jira, or manual; linked to product spec in the product repo.
4. **Human gates** — After spec-review and planner (and PR when applicable).
5. **IDE-native** — Skills + MCP or pasted stories; no WholeLoop server to deploy.

## Quick start

1. Read [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md).
2. Install the CLI ([install/README.md](install/README.md)):

   ```bash
   brew install uv          # macOS
   uv tool install wholeloop-cli
   ```

3. **Guided setup** (founders / first time) — product repo + app repo(s) in one flow:

   ```bash
   wholeloop setup
   ```

   Or set them up by role:

4. **Product repo** (PM — system of record):

   ```bash
   wholeloop product init ~/projects/my-product --name my-product
   ```

   Open in Cursor; use PM skills (`build-spec`, `brainstorm-feature`, …). Existing product repo with data: **do not** `product init --force` — use `wholeloop product update`.

5. **App repo** (Dev — delivery, linked to product):

   ```bash
   cd /path/to/your-app
   wholeloop app init --product ~/projects/my-product
   wholeloop doctor
   ```

6. Run **project-conventions** in the app IDE → approve `references/project-conventions.md`.

[docs/SETUP_NEW_PROJECT.md](docs/SETUP_NEW_PROJECT.md) · [docs/IDE_SETUP.md](docs/IDE_SETUP.md) · [GUIDELINES.md](GUIDELINES.md)

> **Versions:** the delivery **pipeline is v0.2**; the **CLI is published independently** (see [PyPI](https://pypi.org/project/wholeloop-cli/) for the latest). Upgrade with `uv tool install wholeloop-cli --upgrade --force`. The CLI also tells you when a newer release is available.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
