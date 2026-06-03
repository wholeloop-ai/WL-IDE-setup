# Workflow: product spec + user stories

Specs in a **product** repo; stories in **Linear**, **Jira**, or **manual paste**; implementation in an **app** repo with Cursor, Claude Code, or VS Code. No WholeLoop server, n8n, or Python runner to deploy.

> Tracker setup: **[TRACKERS.md](TRACKERS.md)** · IDE setup: **[IDE_SETUP.md](IDE_SETUP.md)**

## Overview

```text
Product repo                        Tracker                  App repo (delivery)
────────────                        ───────                  ──────────────────
scope.yaml
  └─ ui-ux-designer Phase A (opt)
       └─ mockup.html
build-spec
  └─ ARTIFACT-WAL-NNN  ──────────► Epic created (no stories yet)
  └─ inbox/ copy
                                                        spec-review
                                                          accepts: ARTIFACT-WAL / epic / both
                                                          detects: epic state + prior plan
                                                          writes:  context.json + spec_review_notes
                                                        ⊙ human gate
                                                        ui-ux-designer Phase B (opt)
                                                          writes: design-notes.md
                                                        ⊙ human gate
                                                        planner
                                                          reads:   spec_review_notes
                                                          mode 1:  creates stories + plan.md
                                                          mode 2:  creates plan.md (stories exist)
                                                          mode 3:  edits/replaces plan.md (prior plan)
                                                        ⊙ human gate
                                                        builder / manual
                                                          reads: plan.md
                                                        reviewer → pr-agent → ⊙ PR gate
                                                        handoff
                                                          writes: delivery_notes → scope.yaml
                                                          closes: stories + epic
```

1. PM authors scope and (optionally) mockup in the product repo; **build-spec** writes ARTIFACT-WAL and creates the epic (no child stories).
2. Developer runs **spec-review** with ARTIFACT-WAL and/or epic ref.
3. Optional **ui-ux-designer Phase B** → **planner** → per-story **builder** or manual → **reviewer** → **pr-agent** → **handoff**.

## Linking spec ↔ stories

Document in app `project-conventions.md` → **Issue tracker**.

| Provider | Typical link |
|----------|----------------|
| **linear** | Label `spec:ARTIFACT-WAL-NNN`, epic parent |
| **jira** | Epic link, label, or JQL |
| **manual** | Epic description + pasted stories at spec-review |

Spec frontmatter:

```yaml
spec_id: ARTIFACT-WAL-042
epic_ref: PROJ-EPIC-10
tracker_provider: linear
```

## Run folder layout

`workspace/runs/<run-key>/`:

```text
├── context.json        # spec-review (immutable base fields)
├── design-notes.md     # ui-ux-designer Phase B (optional)
├── <story-key>/
│   ├── plan.md         # planner · builder/manual live updates
│   └── review-report.md
└── .done               # handoff
```

For single-story runs, `plan.md` may live directly under `<run-key>/`.

## IDE setup (all three)

```bash
uv tool install wholeloop-cli    # once — see install/README.md
cd /path/to/your-app
wholeloop init
```

| IDE | Skills | Instructions |
|-----|--------|----------------|
| Cursor | `.cursor/skills` → `.agents/skills` | `WHOLELOOP.md` |
| Claude Code | `.claude/skills` → `.agents/skills` | `CLAUDE.md` |
| VS Code | `.agents/skills/` | `WHOLELOOP.md` + Copilot instructions |

## Typical session

1. **spec-review** — ARTIFACT-WAL and/or epic ref → detects state → context.json
2. ⊙ Human gate
3. *(optional)* **ui-ux-designer Phase B** → design-notes.md → ⊙ human gate
4. **planner** — reads spec_review_notes, picks mode, creates/updates plans
5. ⊙ Human gate → choose builder or manual in plan.md
6. **builder** / manual per story — executes plan.md → **reviewer**
7. **pr-agent** → ⊙ PR gate (story or epic per release_strategy)
8. **handoff** → delivery_notes → scope.yaml + `.done` + tracker closed

## Spec-review (replaces spec-validator · analyser · tracker-intake)

spec-review does what all three previous agents did, plus epic state detection.

| Responsibility | Previously | Now |
|---|---|---|
| Spec implementability + AC completeness | spec-validator | spec-review |
| Stack and constraint analysis | analyser | spec-review |
| Tracker ingestion and epic/story lookup | tracker-intake | spec-review |
| Epic state detection (stories, prior plan) | — not covered — | spec-review |

Epic states detected:

| State | Condition |
|-------|-----------|
| `spec-only` | No epic yet |
| `epic-no-stories` | Epic exists, no child stories |
| `epic-with-stories` | Epic + stories, no prior plan |
| `epic-with-plan` | Epic + stories + prior plan.md exists |

All findings passed to planner via `spec_review_notes` in context.json.

## Final pipeline (per story)

```text
spec-review           → context.json base + spec_review_notes
⊙ human gate
ui-ux-designer B      → design-notes.md (optional)
⊙ human gate
planner               → stories in tracker + plan.md + release_strategy
⊙ human gate
─── per story ───────────────────────────────────────────────
builder / manual      → executes plan.md, marks [x], progress notes
reviewer              → review-report.md + story_reviews[<key>]
─── end per story ───────────────────────────────────────────

story mode:           pr-agent after each story review
epic mode:            pr-agent once all story_reviews approved

pr-agent              → PR + context.json pr block
⊙ human PR gate
handoff               → release note + delivery_notes + .done
```

## Checklists

**Product repo:** `Features/<slug>/scope.yaml`, ARTIFACT-WAL, epic after build-spec.

**App repo:** [SETUP_NEW_PROJECT.md](SETUP_NEW_PROJECT.md), [TRACKERS.md](TRACKERS.md).
