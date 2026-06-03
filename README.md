# WholeLoop

**WholeLoop** is an **agentic delivery workflow** (ADWF): product specs → user stories (Linear, Jira, or manual) → gated agents in the IDE → implementation → review → PR → handoff.

Portable **skills + CLI + docs**. No background orchestrator, no n8n — developers run the pipeline in **Cursor**, **Claude Code**, or **VS Code**.

## What you get

| Area | In this repo |
|------|----------------|
| **Skills** | `agents/skills/*/SKILL.md` |
| **CLI** | `wholeloop-cli` on PyPI → `wholeloop init` — [install/](install/) · [docs/CLI.md](docs/CLI.md) |
| **Trackers** | [docs/TRACKERS.md](docs/TRACKERS.md) — Linear, Jira, manual |
| **Spec template** | `references/SPEC.template.md` (product repo) |
| **Conventions** | `references/PROJECT_CONVENTIONS.template.md` |
| **Workflow** | [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md) |

## Principles

1. **Spec in product repo** — ARTIFACT-WAL; stories in your issue tracker (or manual list).
2. **One run per delivery** — `workspace/runs/<run-key>/context.json` (+ `plan.md` per story).
3. **Human gates** — After spec-review and planner (and PR when applicable).
4. **IDE-native** — Skills + MCP or pasted stories; no WholeLoop server to deploy.

## Quick start

1. Read [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md).
2. Install the CLI:

   **macOS (Homebrew):**

   ```bash
   brew install uv
   uv tool install wholeloop-cli
   ```

   **Any OS (uv already installed):**

   ```bash
   uv tool install wholeloop-cli
   ```

   pipx, pip, Git, upgrades: **[install/README.md](install/README.md)**.

3. In your **app** repo:

   ```bash
   wholeloop init
   wholeloop doctor
   wholeloop conventions bootstrap   # or --conventions-from team file
   ```

4. Run the **project-conventions** agent in your IDE → approve `.agents/skills/references/project-conventions.md`.
5. **Product** repo: copy `references/SPEC.template.md` → `specs/`.

[docs/SETUP_NEW_PROJECT.md](docs/SETUP_NEW_PROJECT.md) · [docs/IDE_SETUP.md](docs/IDE_SETUP.md) · [GUIDELINES.md](GUIDELINES.md)

> **Version:** skills and docs target **v0.2**. Check [PyPI](https://pypi.org/project/wholeloop-cli/) for the latest CLI; use `uv tool install wholeloop-cli --upgrade --force` after publishing a new release.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
