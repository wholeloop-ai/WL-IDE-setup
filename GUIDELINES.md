# WholeLoop — team guidelines

Use with **README.md** when onboarding a team.

## 1. Terminology

| Term | Meaning |
|------|---------|
| **Spec** | `ARTIFACT-<PREFIX>-NNN` markdown in the **product** repo (prefix from `wholeloop-product.json`, e.g. `ARTIFACT-HAYA-042.md`). |
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
| **Workspace** | Ephemeral `workspace/runs/` in the **app** repo — execution state, not product truth. |
| **Product repo** | Durable system of record: scope, specs, interviews, inbox, progress, delivery history. |

> **History:** v0.1 used **cohort** (all stories reviewed together in spec-validator). v0.2 uses epic state + per-story plans.

## 2. Two repos — product is the center

WholeLoop is intentionally **two repositories**. The **product repo** holds everything that must stay aligned over time; the **app repo** runs delivery and code. You need both for the full loop — the product repo is not a side project.

| Layer | Repo | Role |
|-------|------|------|
| **Truth** | Product | Scope, product spec, interviews, roadmap context, inbox copies, `delivery_notes` after ship |
| **Execution** | App | Code, `wholeloop app init` skills, gitignored `workspace/runs/` per delivery |

**Scaffold:**

```bash
wholeloop setup                            # guided: product + app(s), linked
# or by role:
wholeloop product init <path>              # product — new repo only; see safety below
wholeloop app init <app-path> --product <product-path>   # app — delivery + link
```

The `--product` flag (or `wholeloop link <product>`) writes the product repo path into the app's `project-conventions.md` — that link is what lets the app **feed** the product repo. Install CLI: [install/README.md](install/README.md). Commands: [docs/CLI.md](docs/CLI.md).

### Product repo layout (system of record)

```text
<product>/
├── Features/<slug>/
│   ├── scope.yaml              # intent, status, delivery_notes (handoff writes here)
│   ├── ARTIFACT-<PREFIX>-NNN.md     # canonical spec
│   └── mockup.html             # optional (ui-ux-designer Phase A)
├── Interviews/                 # raw, processed, master.yaml
├── inbox/                      # copies of specs for cross-repo handoff
├── Progress/                   # handoffs, signals, delivery history
├── Context/                    # ICP, roadmap, analytics snapshots
├── .cursor/skills/             # PM agents (build-spec, brainstorm-feature, …)
└── Agents/                     # repo-local agent docs (roadmap, synthesis)
```

`wholeloop app update` refreshes app skills/docs only. For the product repo, `wholeloop product update` refreshes **only** the PM skills (`.cursor/skills/`, `Agents/`) and never touches `Features/`, `Interviews/`, `Progress/`, `inbox/`, `Context/`. To scaffold a **new** product repo: `wholeloop product init`. On a repo that already has content, do **not** use `product init --force` — that wipes the directory; use `product update` instead.

### App repo layout (delivery)

```text
<app>/
├── .agents/skills/          # canonical prompts (wholeloop app init)
├── workspace/runs/          # gitignored — ephemeral per run
├── WHOLELOOP.md
├── CLAUDE.md                # Claude Code
├── .github/copilot-instructions.md
├── .cursor/skills → .agents/skills
├── .claude/skills → .agents/skills
└── .cursor/rules/wholeloop.mdc
```

Point `project-conventions.md` at the product repo path and inbox so **spec-review** and **handoff** can close the loop.

### Workspace run layout (app only)

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

## 8. Keeping product and app in sync

- **Discovery → spec:** PM agents in the product repo (`build-spec`, interviews, roadmap) write durable artifacts under `Features/` and `Context/`.
- **Spec → delivery:** product spec (and/or epic in the tracker) flows into the app — typically via product `inbox/` and **spec-review**.
- **Delivery → product:** **handoff** appends `delivery_notes` to `Features/<slug>/scope.yaml` and may write under `Progress/` — the loop closes in the product repo.
- One **WholeLoop run** per `run-key` in the app repo (may contain multiple stories); runs are disposable, product docs are not.

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
wholeloop app update    # refreshes .agents/skills/ + IDE docs; keeps project-conventions.md
```

**Skills (product repo):**

```bash
wholeloop product update   # refreshes PM skills only; keeps Features/, Interviews/, …
```

Or diff `agents/skills/` in this template vs your app copy.

**Conventions:** `wholeloop conventions bootstrap` or import a team file — [docs/PROJECT_CONVENTIONS.md](docs/PROJECT_CONVENTIONS.md).

## 10. Support

Issues in **this** repository. Application bugs stay in each app repo.
