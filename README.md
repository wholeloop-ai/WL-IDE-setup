# WholeLoop

**WholeLoop** is an **agentic delivery workflow** (ADWF): structured specs → gated LLM agents → implementation → review → PR → optional handoff to your issue tracker and documentation repo.

This repository is the **portable template**: folder layout, generic `SKILL.md` prompts, conventions, and team guidelines. It contains **no product code** — you copy or symlink pieces into each application repository.

## What you get

| Area | In this repo |
|------|----------------|
| **Skills** | `agents/skills/*/SKILL.md` — copy to `<your-app>/.agents/skills/` (or set `SKILLS_DIR`) |
| **Conventions template** | `references/PROJECT_CONVENTIONS.template.md` — replace with your stack |
| **Orchestrator** | Not vendored here (see **Reference implementation** below). Use your fork or the Walliu `orchestrator.py` as a starting point. |
| **Guidelines** | `GUIDELINES.md`, `docs/` — how teams wire IDE, env, gates |

## Principles

1. **One artifact in** — Markdown (or YAML) spec dropped in `inbox/` defines the ticket.
2. **Gates** — Human or WholeLoop UI approves spec, plan, design, PR before continuing.
3. **Skills are prompts** — Each agent is a `SKILL.md` loaded by your runner (Python orchestrator, Cursor, n8n, etc.).
4. **Project conventions** — Single source of truth your agents read first (paths, stack, “never do X”).
5. **Ephemeral workspace** — Agent outputs under `workspace/`; handoff step consolidates and cleans when you wire it.

## Quick start (new project)

1. Read **[GUIDELINES.md](GUIDELINES.md)** and **[docs/SETUP_NEW_PROJECT.md](docs/SETUP_NEW_PROJECT.md)**.
2. Copy `agents/skills/` → `<app>/.agents/skills/`.
3. Copy `references/PROJECT_CONVENTIONS.template.md` → `<app>/.agents/skills/references/project-conventions.md` and fill in **your** stack.
4. Add an orchestrator (see **[docs/REFERENCE_IMPLEMENTATION.md](docs/REFERENCE_IMPLEMENTATION.md)**) or integrate skills with **Cursor** only (see **[docs/IDE_CURSOR.md](docs/IDE_CURSOR.md)**) / other editors (**[docs/IDE_VSCODE.md](docs/IDE_VSCODE.md)**).
5. Create `inbox/`, `workspace/`, `.env.local` with `ANTHROPIC_API_KEY` (or your LLM provider adapter).

## Reference implementation

Walliu open-sources a full Python orchestrator, Linear handoff, migration agent, etc. Use it as a **reference fork**, not a submodule requirement:

- App repo: `walliu` — `orchestrator.py`, `orchestrator_server.py`, `inbox/`, `workspace/`, `.agents/skills/` (may be ahead of this template).

When Walliu evolves agents, port changes back into **this** `wholeloop` repo so other projects stay aligned.

## Requirements (orchestrator path)

```txt
anthropic>=0.40
python-dotenv
requests
watchdog
```

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
