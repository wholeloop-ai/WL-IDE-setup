---
name: tracker-intake
description: >
  Bootstrap WholeLoop for a spec (Cursor, Claude Code, VS Code). List user stories
  via Linear MCP, Jira MCP, or manual paste. Pick active story; init context.json.
version: "1.0.0"
author: WholeLoop
output: cohort list + workspace/runs/<story-key>/context.json run block
human_gate: false
---

# Tracker intake

## Role

Bootstrap a WholeLoop run: resolve the **parent spec**, discover the **full cohort** of user stories, confirm the **active story**.

Does **not** validate — that is **spec-validator**.

Works with **Linear**, **Jira**, or **manual** input (see `project-conventions.md` → **Issue tracker**).

## Context

Read **`references/project-conventions.md`** — `tracker.provider`, linking rules, product repo path.

## Input

One of:

- `spec_id` (e.g. `SPEC-2025-042`)
- Path to spec markdown in the product repo
- Optional: active story key (e.g. `ACME-128`, `PROJ-456`) if already chosen

## Step 1 — Resolve spec

- Read spec from conventions path or frontmatter `product_repo_path` / `spec_path`.
- Extract `spec_id`, tracker hints from YAML (`tracker_label`, `tracker_epic_key`, `jira_epic_key`, etc.).

## Step 2 — Fetch cohort (by provider)

### `linear` — Linear MCP

- Linking per conventions: **label** `spec:<spec_id>`, **parent** epic, or **custom field**.
- Return: identifier, title, state, assignee, url.

### `jira` — Jira MCP

- Linking per conventions, e.g.:
  - **Epic Link** / parent = epic key from spec frontmatter
  - **Label** `spec-SPEC-2025-042`
  - **JQL**: `project = PROJ AND labels = "spec:SPEC-2025-042"` (document query in conventions)
- Return: key (`PROJ-123`), summary, status, assignee, url.

### `manual` — No MCP

Ask the human to provide **one** of:

1. **Markdown table** pasted in chat (columns: key, title, state, url optional), or  
2. **Bullet list** of story keys + titles, or  
3. **Export** (CSV/json) pasted or attached.

Minimum cohort fields per row: `story_key`, `title`. If only one story is provided, confirm it is the active story.

Do not block the pipeline — manual is first-class.

## Step 3 — Present cohort

Markdown table: key | title | state | url (if known).

## Step 4 — Confirm active story

Use user-provided key or ask which row to run WholeLoop on.

## Step 5 — Initialize context

Create `workspace/runs/<story-key>/context.json`:

```json
{
  "run": {
    "spec_id": "SPEC-2025-042",
    "spec_path": "../product/specs/SPEC-2025-042.md",
    "tracker_provider": "linear | jira | manual",
    "story_key": "ACME-128",
    "story_id": "<opaque id if MCP provided>",
    "story_url": "https://...",
    "cohort_story_keys": ["ACME-128", "ACME-129"],
    "cohort_source": "mcp | manual_paste"
  }
}
```

Use `story_key` as the run folder name (sanitize `/` and spaces for filesystem safety).

**Legacy:** you may also set `linear_identifier` = `story_key` when `tracker_provider` is `linear` for older context files.

## Step 6 — Hand off

Tell the human to run **spec-validator** next with this context loaded.

## Never

- Never skip conventions — provider and linking must match the client.
- Never assume `inbox/` — specs live in the **product** repo.
- Never start implementation — intake only.
- Never invent story keys or URLs when using MCP.
