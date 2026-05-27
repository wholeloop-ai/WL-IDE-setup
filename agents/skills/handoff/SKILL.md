---
name: handoff
description: >
  After PR gate approval: emit one closure markdown for your doc repo, optional
  issue-tracker comment (e.g. Linear), then allow workspace cleanup. Orchestrator
  may perform API calls; this skill defines content and JSON shape.
version: "1.0.0"
author: WholeLoop
output: JSON handoff block (orchestrator persists files + posts to tracker)
human_gate: false
---

# Handoff

## Role
Close the loop for PM/discovery: **one** summary document + **short** tracker comment + signal to clean ephemeral workspace files.

## Input
Full run context including `pr.pr_url`, gates, review/build summaries, artifact AC table.

## Output JSON
```json
{
  "handoff": {
    "ok": true,
    "filename": "YYYY-MM-DD-<ticket-id>-handoff.md",
    "full_markdown": "... full doc ...",
    "linear_comment_markdown": "... shorter body for Linear / copy-paste to other trackers ...",
    "run_cleanup": true
  }
}
```

- **`linear_comment_markdown`**: keep under ~8k chars; include PR link and AC status. (Jira/GitHub: paste same text or adapt.)
- **`run_cleanup`**: `true` when safe to delete ephemeral agent outputs (your orchestrator runs the cleanup script).

## Environment (typical)
- `LINEAR_API_KEY` + issue id = `ticket_id` (Linear GraphQL), or adapt orchestrator for Jira/GitHub.
- `WHOLELOOP_HANDOFF_ROOT` — absolute path to the documentation/product repo where handoff `.md` files live (subpath e.g. `Progress/adwf-handoffs/` is your convention). Walliu uses `WALLIU_PRODUCT_ROOT` + fixed subpath — rename in your fork if you prefer.

## Never
- Never invent PR URLs.
- Never paste secrets into markdown.
