# WholeLoop

**WholeLoop** is an **agentic delivery workflow** (ADWF): product specs → user stories (Linear, Jira, or manual) → gated agents in the IDE → implementation → review → PR → handoff.

Portable **skills + CLI + docs**. No background orchestrator, no n8n — developers run the pipeline in **Cursor**, **Claude Code**, or **VS Code**.

## What you get

| Area | In this repo |
|------|----------------|
| **Skills** | `agents/skills/*/SKILL.md` |
| **CLI** | `pipx install wholeloop-cli` → `wholeloop init` — [docs/CLI.md](docs/CLI.md) · [Publish](docs/PUBLISHING_CLI.md) |
| **Trackers** | [docs/TRACKERS.md](docs/TRACKERS.md) — Linear, Jira, manual |
| **Spec template** | `references/SPEC.template.md` (product repo) |
| **Conventions** | `references/PROJECT_CONVENTIONS.template.md` |
| **Workflow** | [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md) |

## Principles

1. **Spec in product repo** — Stories in your issue tracker (or manual list).
2. **One run per story** — `workspace/runs/<story-key>/context.json`.
3. **Human gates** — After spec-validator and planner (and PR when applicable).
4. **IDE-native** — Skills + MCP or pasted stories; no WholeLoop server to deploy.

## Quick start

1. [docs/WORKFLOW_PRODUCT_LINEAR.md](docs/WORKFLOW_PRODUCT_LINEAR.md)
2. `uv tool install wholeloop-cli==0.1.2` — [PyPI](https://pypi.org/project/wholeloop-cli/)
3. In your app: `wholeloop init` → `wholeloop doctor`
4. Edit `.agents/skills/references/project-conventions.md`
5. Product repo: `references/SPEC.template.md` → `specs/`

[docs/SETUP_NEW_PROJECT.md](docs/SETUP_NEW_PROJECT.md) · [docs/IDE_SETUP.md](docs/IDE_SETUP.md) · [GUIDELINES.md](GUIDELINES.md)

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
