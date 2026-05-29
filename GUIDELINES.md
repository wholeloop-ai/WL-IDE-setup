# WholeLoop — team guidelines

Use with **README.md** when onboarding a team.

## 1. Terminology

| Term | Meaning |
|------|---------|
| **Spec** | Approved markdown in the **product** repo (e.g. `specs/SPEC-2025-042.md`). |
| **Story** | User story in Linear, Jira, or a manual list — linked to that spec. |
| **Cohort** | All stories for one spec — reviewed together in **spec-validator**. |
| **ADWF** | Agentic Delivery Workflow — ordered pipeline with human gates. |
| **Skill** | `SKILL.md`: YAML frontmatter + instructions for one agent role. |
| **Gate** | Human approval before the next step (in IDE chat or tracker). |
| **Workspace** | Ephemeral `workspace/runs/` — not long-lived product docs. |

## 2. Repository layout (app repo)

```text
<app>/
├── .agents/skills/          # canonical prompts (wholeloop init)
├── workspace/runs/          # gitignored
├── WHOLELOOP.md
├── CLAUDE.md                # Claude Code
├── .github/copilot-instructions.md
├── .cursor/skills → .agents/skills
├── .claude/skills → .agents/skills
└── .cursor/rules/wholeloop.mdc
```

**Product repo (separate):** `specs/SPEC-*.md` from `references/SPEC.template.md`.

Install: `wholeloop init` — [docs/CLI.md](docs/CLI.md).

## 3. Issue tracker

Set in `references/project-conventions.md`:

| `tracker.provider` | How stories arrive |
|--------------------|--------------------|
| `linear` | Linear MCP |
| `jira` | Jira MCP |
| `manual` | Pasted table / list in IDE chat |

Details: **[docs/TRACKERS.md](docs/TRACKERS.md)**.

## 4. Gates (minimum)

| Gate | After |
|------|--------|
| Spec + story | **spec-validator** |
| Plan | **planner** |
| Design | **ui-ux-designer** (optional) |
| PR | **pr-agent** |

Gates happen in the IDE (approve / reject / approve-with-note). No separate WholeLoop UI or n8n required.

## 5. Optional configuration

| Item | Purpose |
|------|---------|
| `WHOLELOOP_HANDOFF_ROOT` | Extra repo path for handoff markdown (optional) |
| Linear / Jira MCP | IDE settings — not committed to app repo |

LLM API keys live in the **IDE**, not in WholeLoop templates.

## 6. Security

- Never commit `workspace/` or API keys.
- `reviewer` — no secrets in diff.
- Planner + CI — forbidden paths per `project-conventions.md`.

## 7. Multi-repo

- One **WholeLoop run** per story per app repo.
- Cross-repo work: split stories or link `story_key` / spec_id in handoff notes.

## 8. Updating skills

```bash
wholeloop update    # in app repo; keeps project-conventions.md
```

Or diff `agents/skills/` in this template vs your app copy.

## 9. Support

Issues in **this** repository. Application bugs stay in each app repo.
