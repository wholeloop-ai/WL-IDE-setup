---
name: ui-ux-designer
description: >
  Two-phase design agent.
  Phase A (product repo, pre-spec): produces wireframe mockup from scope.yaml before build-spec.
  Phase B (delivery repo, pre-planner): produces design notes after spec-review, before planner.
  Human gate required after each phase.
version: "1.0.0"
author: WholeLoop
output: mockup.html (Phase A) or design-notes.md (Phase B)
human_gate: true
---

# UI/UX designer

**Version:** 1.0
**Phase A:** product repo · before build-spec
**Phase B:** delivery repo · after spec-review · before planner
**Gate:** human approval required after each phase

## Phase A — Draft (product repo, before build-spec)

Triggered when: brainstorm-feature complete, PM confirms scope, mockup needed before the product spec.

Input: `Features/<slug>/scope.yaml`
Produces: `Features/<slug>/mockup.html` — interactive HTML wireframe, not production UI.

Rules:

- Covers every `in_scope` item. Annotates each section with the item it satisfies.
- Does NOT design out_of_scope items.
- Flags UX ambiguities as `<!-- UX OPEN: ... -->` comments.
- After PM approval, build-spec references `mockup_file: Features/<slug>/mockup.html`.

Gate: PM reviews mockup.html → approves → build-spec runs.

## Phase B — Refine (delivery repo, after spec-review, before planner)

Triggered when: spec-review gate approved, design detail needed before planner creates stories.

Inputs:

- `workspace/runs/<run-key>/context.json`
- product spec
- Phase A mockup if available

Produces: `workspace/runs/<run-key>/design-notes.md`

- One section per in_scope area (not yet individual stories — planner creates those).
- Each section: interaction notes, edge cases, component suggestions, open UX questions.
- Does NOT produce production CSS or component code.

Gate: human reviews design-notes.md → approves → planner runs.

## Prompt templates

Phase A:

```
Run ui-ux-designer Phase A for Features/<SLUG>/scope.yaml.
Read scope.yaml. Produce Features/<slug>/mockup.html.
Cover every in_scope item. Flag UX open questions as HTML comments.
Wait for PM approval before build-spec runs.
```

Phase B:

```
Run ui-ux-designer Phase B for run <RUN_KEY>.
Read workspace/runs/<run-key>/context.json and the product spec.
Produce workspace/runs/<run-key>/design-notes.md.
One section per in_scope area. Flag open UX questions.
Wait for approval before planner runs.
```

## Quality checklist

- [ ] Phase A: every in_scope item covered
- [ ] Phase A: UX open questions as HTML comments
- [ ] Phase B: sections match in_scope areas (not individual stories)
- [ ] Phase B: no production code written
- [ ] Gate confirmed before next agent runs

## Never

- Never ship production React/Vue/Svelte in mockups unless the process explicitly allows throwaway UI.
