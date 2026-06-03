# WholeLoop architecture

## Pipeline (v0.2)

See **[WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md)** and **[TRACKERS.md](TRACKERS.md)**.

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

## Out of scope (this repo)

- Python orchestrator, inbox watchers, n8n flows — not part of the supported developer experience.
- Product-repo agents (`build-spec`, `brainstorm-feature`, …) live in the product template, not this bundle.
