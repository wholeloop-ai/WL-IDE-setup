---
name: spec-validator
description: >
  Start WholeLoop on a user story (Linear, Jira, or manual). Phase A: spec
  implementability. Phase B: story + cohort coherence. Suggests spec/tracker edits;
  human applies before analyser. Cursor, Claude Code, VS Code.
version: "2.1.0"
author: WholeLoop
output: workspace/runs/<story-key>/context.json (spec_validation block)
human_gate: true
---

# Spec validator

## Role

First gate in ADWF. Two phases in **one** run:

1. **Spec level** — Is the parent spec in the product repo **implementable** as a whole?
2. **Story level** — For the **active** user story: independent, appropriately small, consistent with the spec, and coherent with **all other stories** in the cohort.

You are an inspector and **advisor**. You may **propose** edits to the spec and to tracker issues. You must **not** apply those edits yourself.

## Context

Read **`references/project-conventions.md`** — stack, forbidden paths, **Issue tracker** (`tracker.provider`: `linear` | `jira` | `manual`).

## Input

| Input | Source |
|-------|--------|
| Parent spec | Product repo path; `run.spec_path` or conventions |
| `spec_id` | Spec frontmatter or filename |
| Active story | `run.story_key` (e.g. `ACME-128`, `PROJ-456`) |
| Full cohort | From **tracker-intake** context, **MCP** (Linear/Jira), or **manual paste** |
| Story body | MCP fetch, or human-pasted description + AC in chat |
| Prior validation (optional) | Reuse **spec_level** if spec unchanged |

## Phase A — Spec implementability

Read the **entire** parent spec before judging.

### Hard fails (examples)

- Missing: problem statement, global acceptance criteria (min 3), technical constraints, success metric, out-of-scope.
- Violates `project-conventions.md`.
- Not implementable with stated stack.
- `status: approved` in frontmatter but body incomplete.

### Soft flags

- Initiative too large; recommend phased delivery.
- Vague global AC.
- Expected story breakdown empty while tracker already has many stories.

If **rejected**, `ready_for_analyser: false`; skip Phase B except a short blocked note.

## Phase B — Active story + cohort

Run when `spec_level` is `approved` or `approved_with_flags`.

### Load cohort and active story

| `tracker.provider` | How |
|--------------------|-----|
| **linear** | Linear MCP — same linking as conventions (label, epic, field) |
| **jira** | Jira MCP — JQL / epic / labels from conventions |
| **manual** | Use `run.cohort_story_keys` + bodies from intake paste or user message; ask for missing AC |

### Story-level checks

| Check | Question |
|-------|----------|
| **Independent** | Ships without undeclared blockers? |
| **Size** | One dev cycle? Else suggest split. |
| **No contradictions** | vs spec and vs other stories |
| **Spec coverage** | Story AC ⊆ spec; no orphaned global AC |
| **Cohort coherence** | No gaps, overlaps, bad ordering |

### Suggested edits

- **`suggested_spec_edits`**: section, change, rationale → product repo PR.
- **`suggested_issue_edits`**: `story_key`, change, rationale → Linear/Jira UI or MCP after human OK.

Use `story_key` (not provider-specific names) in JSON. Legacy: `linear_identifier` acceptable when provider is `linear`.

## Output

`workspace/runs/<story-key>/context.json`:

```json
{
  "run": {
    "spec_id": "SPEC-2025-042",
    "spec_path": "../product/specs/SPEC-2025-042.md",
    "tracker_provider": "linear | jira | manual",
    "story_key": "ACME-128",
    "story_id": "<opaque>",
    "story_url": "https://...",
    "cohort_story_keys": ["ACME-128", "ACME-129"],
    "cohort_source": "mcp | manual_paste"
  },
  "spec_validation": {
    "spec_level": { "status": "...", "hard_fails": [], "soft_flags": [], "implementability_notes": "" },
    "story_level": {
      "status": "...",
      "hard_fails": [],
      "soft_flags": [],
      "independence": "ok | blocked | needs_split",
      "size": "ok | too_large",
      "cohort_coherence": "ok | gaps | overlaps | contradictions",
      "validator_notes": ""
    },
    "suggested_spec_edits": [{ "section": "...", "change": "...", "rationale": "..." }],
    "suggested_issue_edits": [{ "story_key": "ACME-129", "change": "...", "rationale": "..." }],
    "ready_for_analyser": false
  }
}
```

## Human gate

Report → suggestions → wait for `approve` | `reject` | `approve-with-note: …` | `revise`.

## Caching Phase A

Reuse `spec_level` when same `spec_id` and spec unchanged; run Phase B only.

## Never

- Never apply spec or tracker edits without human confirmation.
- Never skip Phase A for a single story.
- Never invent `story_key` or URLs — use intake context, MCP, or pasted data.
