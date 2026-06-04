# CLAUDE.md — Product discovery (WholeLoop)

This repo is the **system of record for product discovery** for {{PRODUCT_NAME}}.
It stores evidence-backed decisions: interviews, meetings, analytics snapshots, OST, roadmap, and feature specs.
It does **not** contain production application code.

## Flow

Context → Interviews + Surveys → Analytics → Product Meetings → OST → Roadmap → Features → (handoff) {{APP_REPO}}/inbox

## Key paths

- **Features/** — `scope.yaml`, `ARTIFACT-WAL-NNN.md`, optional mockups
- **Progress/adwf-handoffs/** — closure summaries after delivery (`handoff` agent in app repo)
- **inbox/** — mirror of approved artifacts before copy to app repo

## Sibling repos

See `Context/org-repositories.md`. App delivery uses WholeLoop v0.2: **spec-review** → planner → …

## Conventions

- Dates: `YYYY-MM-DD` in filenames
- Artifact prefix: `ARTIFACT-WAL-NNN` (increment per existing files in `Features/`)
- Quotes in synthesis need `quote_refs`; assumptions go in `risks_and_assumptions`
