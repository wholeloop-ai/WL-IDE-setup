# WholeLoop architecture

## System shape

WholeLoop is **product-centered**: the product repository is the long-lived system of record (scope, product spec, interviews, inbox, `delivery_notes`, progress). App repositories hold code and **ephemeral** `workspace/runs/` for each delivery. The v0.2 pipeline runs in the app; **handoff** writes back to the product repo so truth stays in one place.

See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

## Pipeline (v0.2, app repo)

```text
spec-review → [ui-ux-designer B] → planner → builder|manual
  → reviewer → pr-agent → handoff
```

Optional agents: `ui-ux-designer` Phase A (product repo), `migration`, `ui-tester`.

Context per run: `workspace/runs/<run-key>/context.json` (+ per-story `plan.md`, `review-report.md`).

## Context object

| Block | Owner |
|-------|--------|
| `run.*`, `spec_review_notes` | spec-review |
| `release_strategy` | planner |
| `story_reviews.<key>` | reviewer |
| `pr` | pr-agent |

Humans (or the IDE agent) advance the pipeline — there is **no** background runner in this template.

## Gates

| Gate | After | Required |
|------|-------|----------|
| Spec / epic review | spec-review | yes |
| Design | ui-ux-designer Phase B | optional |
| Plan | planner | yes |
| PR | pr-agent | yes |
| Handoff | handoff | yes |

Declared in skill frontmatter (`human_gate: true`) and in **WHOLELOOP.md**.

## Extending agents

1. Add `agents/skills/my-agent/SKILL.md`.
2. Update **planner** if the agent belongs in the default route.
3. Run `wholeloop update` in app repos after publishing template changes.

## Product repo (this template’s `product-template/`)

- Scaffold: `wholeloop init-product` — PM skills in `.cursor/skills/`, folder layout for `Features/`, `Interviews/`, `Context/`, etc.
- Not bundled into `wholeloop init` / `wholeloop update` (those target app repos only).
- Future: `wholeloop update-product` to refresh PM skills without touching `Features/` or `Progress/`.

## Out of scope (this repo)

- Python orchestrator, inbox watchers, n8n flows — not part of the supported developer experience.
