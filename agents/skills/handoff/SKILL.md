---
name: handoff
description: >
  After PR gate: closure markdown + tracker comment (Linear/Jira MCP) or paste-ready
  text for manual mode. Cursor, Claude Code, VS Code.
version: "2.1.0"
author: WholeLoop
output: handoff block in workspace/runs/<story-key>/context.json
human_gate: false
---

# Handoff

## Role

Close the loop: **one** summary document + **short tracker comment** + optional workspace cleanup.

## Input

`workspace/runs/<story-key>/context.json` — `run.tracker_provider`, `run.story_key`, `pr`, review/build summaries, story AC.

## Output JSON

```json
{
  "handoff": {
    "ok": true,
    "filename": "YYYY-MM-DD-<story-key>-handoff.md",
    "full_markdown": "...",
    "tracker_comment_markdown": "... PR link, spec_id, AC status ...",
    "run_cleanup": true
  }
}
```

Legacy field name `linear_comment_markdown` is acceptable when `tracker_provider` is `linear`.

## Actions (by provider)

| Provider | Post comment | Doc file |
|----------|--------------|----------|
| **linear** | Linear MCP → `run.story_id` / story URL | Conventions path |
| **jira** | Jira MCP → issue `run.story_key` | Same |
| **manual** | Output `tracker_comment_markdown` for human to paste in any tool | Same |

1. Write `full_markdown` to handoff/product path from conventions.
2. Post or paste `tracker_comment_markdown`.
3. Delete `workspace/runs/<story-key>/` only after human confirms when `run_cleanup: true`.

## Never

- Never invent PR URLs or story keys.
- Never paste secrets into markdown.
