# Issue trackers — Linear, Jira, manual

WholeLoop is **tracker-agnostic**. Stories can come from **Linear MCP**, **Jira MCP**, or **manual paste** (no MCP).

Configure once in `.agents/skills/references/project-conventions.md` → section **Issue tracker**.

## Comparison

| Mode | Best for | Epic / story state lookup | Handoff comment |
|------|----------|---------------------------|-----------------|
| **linear** | Teams on Linear | Linear MCP in Cursor / Claude Code / VS Code | Linear MCP |
| **jira** | Teams on Jira Cloud/Server (with MCP) | Jira MCP + JQL/labels/epic | Jira MCP |
| **manual** | Any tool, exports, email, Notion | Human pastes epic + stories at spec-review | Paste comment yourself or MCP if added later |

Same skills everywhere:

```text
spec-review → ui-ux-designer (opt) → planner → dev agents → reviewer → pr-agent → handoff
```

> **History:** v0.1 used **tracker-intake** for cohort discovery. v0.2 **spec-review** reads the epic and detects child stories if they exist.

## `tracker.provider` in conventions

```markdown
| Setting | Value |
|---------|--------|
| **provider** | `linear` \| `jira` \| `manual` |
```

## Linking spec ↔ stories

| Provider | Typical link |
|----------|----------------|
| **linear** | Label `spec:ARTIFACT-WAL-042`, or epic parent |
| **jira** | Epic link, label, or JQL in conventions |
| **manual** | Paste epic description and existing stories when running spec-review |

Spec frontmatter (`references/SPEC.template.md`) includes tracker-agnostic fields plus optional Linear/Jira keys.

## Linear (MCP)

1. Enable Linear MCP in the IDE ([IDE_SETUP.md](IDE_SETUP.md)).
2. `tracker.provider: linear`
3. “**spec-review** for ARTIFACT-WAL-042 and epic PROJ-EPIC-10”.

## Jira (MCP)

1. Enable **Jira MCP** in the IDE (Atlassian or team-provided server — same pattern as Linear).
2. `tracker.provider: jira`
3. Document in conventions:
   - `jira_project_key` (e.g. `PROJ`)
   - Epic key or label for the spec
   - Optional **JQL template** for listing child stories
4. “**spec-review** for ARTIFACT-WAL-042” — agent reads epic/stories via MCP.

If your Jira MCP exposes different tool names, add them to `project-conventions.md` under **MCP tool hints**.

## Manual (no MCP)

1. `tracker.provider: manual`
2. PM keeps stories in Jira, Azure DevOps, Asana, spreadsheet, etc.
3. Developer runs **spec-review** and **pastes** the epic description and any existing stories when asked, for example:

```markdown
Epic: PROJ-EPIC-10 — Price history on PDP

| story_key | title           | state      |
|-----------|-----------------|------------|
| PROJ-101  | Login form      | To Do      |
| PROJ-102  | Password reset  | In Progress|
```

4. Same output as MCP mode: `context.json` with `epic_state` and `spec_review_notes`.
5. **handoff** — paste tracker comments by hand, or skip MCP post.

Manual mode also works when MCP is temporarily unavailable.

## Context shape (all providers)

`workspace/runs/<run-key>/context.json` — see [GUIDELINES.md](../GUIDELINES.md) for the canonical v0.2 shape.

Base fields written by **spec-review**; **planner** adds `release_strategy`; **reviewer** adds `story_reviews`; **pr-agent** adds `pr`.

## Other tools (GitHub Issues, Azure DevOps, etc.)

Use **manual** until an MCP exists, or add a client-specific fork of **spec-review** / **handoff** following the same `run` JSON shape.

## See also

- [WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md) — end-to-end flow (tracker-agnostic)
- [IDE_SETUP.md](IDE_SETUP.md) — Cursor, Claude Code, VS Code
