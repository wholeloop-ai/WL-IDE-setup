# {{PROJECT_NAME}} — project conventions (template)

> Replace `{{PROJECT_NAME}}` and all sections with your real stack. Agents load this file **before** touching code.

## 1. What this product is

- One paragraph: user, problem, what is **out of scope** (e.g. payments).

## 2. Repository layout

- Tree of important directories (`src/`, `api/`, `packages/foo`, …).
- **Product repo** (specs): absolute or relative path from this app repo (e.g. `../{{PRODUCT_REPO}}/specs/`).

## 3. Stack

| Layer | Technology | Version / notes |
|-------|------------|-----------------|
| Runtime | | |
| Package manager | | |
| Tests | | |
| Linter / formatter | | |

## 4. Rules agents must follow

- Import / module conventions.
- Where tests live.
- Forbidden paths (e.g. do not edit `infra/` without ticket).
- Secrets: never commit; env var names for client vs server.

## 5. Issue tracker (required)

| Setting | Value |
|---------|--------|
| **provider** | `linear` \| `jira` \| `manual` |
| **Default spec path** | `../product-repo/specs/{spec_id}.md` |

PM creates stories **after** spec `status: approved`. See WholeLoop **`docs/TRACKERS.md`**.

### If `linear`

| Setting | Value |
|---------|--------|
| **Strategy** | `label` \| `epic_parent` \| `custom_field` |
| **Label prefix** | e.g. `spec:` → `spec:SPEC-2025-042` |
| **Linear team / project** | |

### If `jira`

| Setting | Value |
|---------|--------|
| **jira_project_key** | e.g. `PROJ` |
| **Strategy** | `epic_link` \| `label` \| `jql` |
| **Label** | e.g. `spec-SPEC-2025-042` |
| **JQL template** (optional) | `project = PROJ AND labels = "spec:{{spec_id}}"` |
| **MCP tool hints** | tool names if non-standard |

### If `manual`

| Setting | Value |
|---------|--------|
| **Cohort at intake** | Dev pastes markdown table or list in chat |
| **Story bodies** | Paste description + AC when running spec-validator |
| **Handoff** | Human copies `tracker_comment_markdown` into their tool |

## 6. WholeLoop run paths

| Path | Purpose |
|------|---------|
| `workspace/runs/<story-key>/context.json` | Per-story pipeline context |
| `.agents/skills/` | Canonical prompts (Cursor / Claude Code / VS Code) |
| `WHOLELOOP.md` | IDE-neutral workflow (repo root) |
| `.cursor/skills/`, `.claude/skills/` | Symlinks to `.agents/skills/` (install script) |

## 7. Definition of Done

- Tests required per change type.
- Docs to update when schema or public API changes.

## 8. Links

- Design system / Figma.
- Issue tracker URL (Linear / Jira / other).
- Product repo URL.
- Runbooks.
