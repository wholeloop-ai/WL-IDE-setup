---
name: handoff
description: >
  Closes the loop after the PR gate. Behaviour depends on release_strategy in context.json:
  story mode — runs per story.
  epic mode — runs once after the epic PR merges.
  Builds release notes, comments on stories and epic, writes delivery_notes to scope.yaml,
  signals roadmap-snapshot, writes Progress/adwf-handoffs/, cleans workspace.
version: "3.0.0"
author: WholeLoop
output: release note + tracker comments + delivery_notes + roadmap signal + .done
human_gate: false
---

# Handoff

## Role

Closes the loop at every level: story, epic, product repo, roadmap.
Reads the review block and pr block from context.json — never invents content.

## Release strategy behaviour

Read `context.json → release_strategy.scope`:

**story mode:** runs after each story's PR gate. Produces one release note per story.

**epic mode:** runs once after the epic PR merges. Aggregates all story_reviews and
produces one release note for the full epic, plus individual story comments.

## Input (read in this order)

1. `context.json` — full run state: release_strategy, story_reviews, pr block, spec_ref, epic_ref, scope_file
2. `workspace/runs/<story-key>/review-report.md` (per story)
3. ARTIFACT-WAL spec — for release note framing
4. `scope.yaml` via scope_file — for delivery_notes

## Actions

### 1. Release note

Build from `context.json → pr.release_notes_draft` + review blocks.

```markdown
# Release: <title> — <YYYY-MM-DD>

**Spec:** <ARTIFACT-WAL ref>
**Epic:** <epic ref>
**Stories:** <list or single>
**PR:** <url>

## What shipped
<user-facing description from ARTIFACT-WAL jtbd.primary>

### Changes
- ...  (from pr.release_notes_draft.what_changed)

### Acceptance criteria delivered
| AC | Status |
|----|--------|
| ... | covered / deferred |

## Deferred
- <item> — <reason>  (from story_reviews[].deferred)

## Known limitations
- ...  (from pr.release_notes_draft.known_limitations)
```

Write to path from `project-conventions.md` handoff section.

### 2. Tracker comments

**Per story** (both modes):

```
Delivered in PR <url>

AC: N/N covered. Deviations: <list or none>. Deferred: <list or none>.
Release note: <link>
```

**Epic comment** (epic mode only):

```
Epic delivered — <date>

Stories: <list with links>
Full release note: <link>
Deferred items carried to next cycle: <list or none>
```

| Provider | Post comment |
|----------|--------------|
| **linear** | Linear MCP → story / epic |
| **jira** | Jira MCP → issue keys |
| **manual** | Output paste-ready markdown for human |

### 3. delivery_notes → scope.yaml

Append to `Features/<slug>/scope.yaml` (path from `context.json → scope_file`):

```yaml
delivery_notes:
  delivered_date: YYYY-MM-DD
  release_strategy: story | epic
  run_key: <run-key>
  artifact_ref: ARTIFACT-WAL-NNN
  epic_ref: <epic-key>
  story_keys: []
  pr_url: <from context.json pr.url>
  implemented_in_scope: []
  deviations: []
  deferred: []
  new_capabilities_created: []
  release_note_file: <path>
  handoff_notes: ""
```

Does NOT modify any other section of scope.yaml.

### 4. Roadmap signal

If `maintain-roadmap` is configured: write a one-line signal file at
`Progress/signals/YYYY-MM-DD-<run-key>.yaml`:

```yaml
date: YYYY-MM-DD
feature_slug: <slug>
artifact_ref: ARTIFACT-WAL-NNN
status: shipped
deferred_items: N
release_note: <path>
```

`maintain-roadmap` reads this on next run to update `roadmap-snapshot.md`.

### 5. Progress/adwf-handoffs/

Write `Progress/adwf-handoffs/YYYY-MM-DD-<run-key>.md` — full handoff record.

### 6. Workspace cleanup

Write `workspace/runs/<run-key>/.done` with delivered date.
Preserve all workspace files for reference. Do not delete.

## Never

- Never invent PR URLs, story keys, or AC status.
- Never paste secrets into markdown.
- Never run in epic mode until the epic PR has merged.
