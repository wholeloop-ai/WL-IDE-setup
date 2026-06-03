# WholeLoop — team guidelines

Use with **README.md** when onboarding a team.

## 1. Terminology

| Term | Meaning |
|------|---------|
| **Spec** | ARTIFACT-WAL markdown in the **product** repo (e.g. `ARTIFACT-WAL-042.md`). |
| **Story** | User story in Linear, Jira, or a manual list — linked to that spec. |
| **spec-review** | Replaces spec-validator + analyser + tracker-intake. Validates spec/epic, detects epic state, passes spec_review_notes to planner. |
| **ui-ux-designer** | Phase A (pre-spec, product repo) · Phase B (pre-planner, delivery repo). |
| **epic state** | What spec-review detects: spec-only / epic-no-stories / epic-with-stories / epic-with-plan. |
| **plan.md** | Per-story execution plan written by planner. Builder's or developer's primary input. |
| **spec_review_notes** | Findings from spec-review deposited in context.json for planner to consume. |
| **delivery_notes** | Block appended to scope.yaml by handoff after shipping. |
| **ADWF** | Agentic Delivery Workflow — ordered pipeline with human gates. |
| **Skill** | `SKILL.md`: YAML frontmatter + instructions for one agent role. |
| **Gate** | Human approval before the next step (in IDE chat or tracker). |
| **Workspace** | Ephemeral `workspace/runs/` — not long-lived product docs. |

> **History:** v0.1 used **cohort** (all stories reviewed together in spec-validator). v0.2 uses epic state + per-story plans.

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

**Product repo (separate):** `Features/<slug>/scope.yaml`, ARTIFACT-WAL from your spec process.

**Install CLI (once):** [install/README.md](install/README.md) — macOS: `brew install uv` then `uv tool install wholeloop-cli`.  
**Install into app:** `wholeloop init` — [docs/CLI.md](docs/CLI.md).

### Workspace run layout

```text
workspace/runs/<run-key>/
├── context.json                   # spec-review · base fields immutable after creation
├── design-notes.md                # ui-ux-designer Phase B · optional
├── <story-key>/
│   ├── plan.md                    # planner writes · builder or dev updates live
│   └── review-report.md           # reviewer
└── .done                          # handoff · signals run complete
```

For single-story runs, `plan.md` may live directly in `<run-key>/`.

### context.json owners

| Block | Written by |
|-------|------------|
| `run.*` base, `spec_review_notes` | spec-review |
| `release_strategy` | planner |
| `story_reviews.<key>` | reviewer (per story) |
| `pr` | pr-agent |
| `.done` file | handoff |

## 3. Issue tracker

Set in `references/project-conventions.md`:

| `tracker.provider` | How stories arrive |
|--------------------|--------------------|
| `linear` | Linear MCP at spec-review |
| `jira` | Jira MCP at spec-review |
| `manual` | Pasted epic + stories in IDE chat |

Details: **[docs/TRACKERS.md](docs/TRACKERS.md)**.

## 4. Gates (minimum)

| Gate | After | Required |
|------|-------|----------|
| Spec + design draft | ui-ux-designer Phase A | optional |
| Spec / epic review | spec-review | yes |
| Design per scope area | ui-ux-designer Phase B | optional |
| Plan | planner | yes |
| PR | pr-agent (after reviewer) | yes |
| Handoff | handoff | yes |

Gates happen in the IDE (approve / reject / approve-with-note). No separate WholeLoop UI or n8n required.

## 5. Manual execution

When a developer chooses manual mode after the planner gate:

1. Set `execution_mode: manual` in plan.md (planner does this on selection).
2. Execute each step. After completing a step, mark it `[x]` in plan.md.
3. Add a progress note with date and brief description.
4. At any point, call planner in **Mode 4** (mid-run refinement) to get guidance on a specific
   pending step or to ask what is left.
5. When all steps are `[x]`: run **reviewer**, then **pr-agent**.

The reviewer uses plan.md to verify:

- Every `[x]` step has a corresponding change in the diff.
- No unchecked steps were skipped without explanation.
- Progress notes are consistent with the diff.

plan.md in manual mode is the developer's commitment — it is as auditable as builder output.

Builder and manual mode are equivalent in output quality; the choice is preference, not a quality tier.

## 6. Optional configuration

| Item | Purpose |
|------|---------|
| `WHOLELOOP_HANDOFF_ROOT` | Extra repo path for handoff markdown (optional) |
| Linear / Jira MCP | IDE settings — not committed to app repo |

LLM API keys live in the **IDE**, not in WholeLoop templates.

## 7. Security

- Never commit `workspace/` or API keys.
- `reviewer` — no secrets in diff.
- Planner + CI — forbidden paths per `project-conventions.md`.

## 8. Multi-repo

- One **WholeLoop run** per `run-key` in the app repo (may contain multiple stories).
- Cross-repo: **build-spec** copies ARTIFACT-WAL to inbox/; **handoff** appends `delivery_notes` to product `scope.yaml`.

## 9. Installing and updating

**CLI (machine):**

```bash
# macOS
brew install uv
uv tool install wholeloop-cli --upgrade --force

# or: brew install pipx && pipx upgrade wholeloop-cli
```

All methods: [install/README.md](install/README.md).

**Skills (app repo):**

```bash
wholeloop update    # refreshes .agents/skills/; keeps project-conventions.md
```

Or diff `agents/skills/` in this template vs your app copy.

**Conventions:** `wholeloop conventions bootstrap` or import a team file — [docs/PROJECT_CONVENTIONS.md](docs/PROJECT_CONVENTIONS.md).

## 10. Support

Issues in **this** repository. Application bugs stay in each app repo.
