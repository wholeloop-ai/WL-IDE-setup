# WholeLoop architecture

## Pipeline

See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

```text
Product spec (approved) ──► Story cohort (Linear / Jira MCP or manual)
        │
        ▼
tracker-intake (optional) ──► spec-validator ──► gate (human)
   Phase A: spec implementability
   Phase B: story + cohort coherence (+ suggested edits)
        │
        ▼
analyser → planner → gate (human) → … → pr-agent → gate → handoff
```

Optional agents: `ui-ux-designer`, `migration`, `ui-tester`.

Context per story: `workspace/runs/<story-key>/context.json`.

## Context object

Each agent appends JSON blocks (`spec_validation`, `codebase_analysis`, `execution_plan`, `build`, `review`, `pr`, `handoff`, …). The next agent reads the full file plus `project-conventions.md`.

Humans (or the IDE agent) advance the pipeline — there is **no** background runner in this template.

## Gates

| Gate | After |
|------|--------|
| Spec / story | **spec-validator** |
| Plan | **planner** |
| Design | **ui-ux-designer** (if used) |
| PR | **pr-agent** |

Declared in skill frontmatter (`human_gate: true`) and in **WHOLELOOP.md**.

## Extending agents

1. Add `agents/skills/my-agent/SKILL.md`.
2. Update **planner** routes for when to invoke it.
3. Run `wholeloop update` in app repos after publishing template changes.

Keep **planner** as the single place that defines agent order per ticket type.

## Out of scope (this repo)

- Python orchestrator, inbox watchers, n8n flows — not part of the supported developer experience.
- Automation is via **IDE + skills + MCP** (or manual story paste).
