# Issue trackers — Linear, Jira, manual

WholeLoop is **tracker-agnostic**. Stories can come from **Linear MCP**, **Jira MCP**, or **manual paste** (no MCP).

Configure once in `.agents/skills/references/project-conventions.md` → section **Issue tracker**.

## Comparison

| Mode | Best for | Cohort discovery | Handoff comment |
|------|----------|------------------|-----------------|
| **linear** | Teams on Linear | Linear MCP in Cursor / Claude Code / VS Code | Linear MCP |
| **jira** | Teams on Jira Cloud/Server (with MCP) | Jira MCP + JQL/labels/epic | Jira MCP |
| **manual** | Any tool, exports, email, Notion | Human pastes table or list in chat | Paste comment yourself or MCP if added later |

Same skills everywhere: **tracker-intake** → **spec-validator** → … → **handoff**.

## `tracker.provider` in conventions

```markdown
| Setting | Value |
|---------|--------|
| **provider** | `linear` \| `jira` \| `manual` |
```

## Linking spec ↔ stories

| Provider | Typical link |
|----------|----------------|
| **linear** | Label `spec:SPEC-2025-042`, or epic parent |
| **jira** | Epic link, label `spec-SPEC-2025-042`, or JQL in conventions |
| **manual** | Spec lists expected stories in §6; human pastes current cohort at intake |

Spec frontmatter (`references/SPEC.template.md`) includes tracker-agnostic fields plus optional Linear/Jira keys.

## Linear (MCP)

1. Enable Linear MCP in the IDE ([IDE_SETUP.md](IDE_SETUP.md)).
2. `tracker.provider: linear`
3. “**tracker-intake** for `SPEC-2025-042`”.

## Jira (MCP)

1. Enable **Jira MCP** in the IDE (Atlassian or team-provided server — same pattern as Linear).
2. `tracker.provider: jira`
3. Document in conventions:
   - `jira_project_key` (e.g. `PROJ`)
   - Epic key or label for the spec
   - Optional **JQL template** for cohort listing
4. “**tracker-intake** for `SPEC-2025-042`” — agent runs JQL/filters via MCP.

If your Jira MCP exposes different tool names, add them to `project-conventions.md` under **MCP tool hints**.

## Manual (no MCP)

1. `tracker.provider: manual`
2. PM keeps stories in Jira, Azure DevOps, Asana, spreadsheet, etc.
3. Developer runs **tracker-intake** and **pastes** a cohort table when asked, for example:

```markdown
| story_key | title           | state      |
|-----------|-----------------|------------|
| PROJ-101  | Login form      | To Do      |
| PROJ-102  | Password reset  | In Progress|
```

4. Active story: “run on **PROJ-101**”.
5. **spec-validator** uses pasted cohort + spec; suggestions go to spec PR and human updates tracker.
6. **handoff** — paste `tracker_comment_markdown` into the tool by hand, or skip MCP post.

Manual mode also works when MCP is temporarily unavailable.

## Context shape (all providers)

`workspace/runs/<story-key>/context.json`:

```json
{
  "run": {
    "tracker_provider": "jira",
    "story_key": "PROJ-128",
    "story_url": "https://...",
    "cohort_story_keys": ["PROJ-128", "PROJ-129"],
    "cohort_source": "mcp | manual_paste"
  }
}
```

## Other tools (GitHub Issues, Azure DevOps, etc.)

Use **manual** until an MCP exists, or add a client-specific fork of **tracker-intake** / **handoff** following the same `run` JSON shape.

## See also

- [WORKFLOW_PRODUCT_LINEAR.md](WORKFLOW_PRODUCT_LINEAR.md) — end-to-end flow (tracker-agnostic)
- [IDE_SETUP.md](IDE_SETUP.md) — Cursor, Claude Code, VS Code
