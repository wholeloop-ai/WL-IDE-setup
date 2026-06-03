# WL-IDE-setup — project conventions (template)

<!-- wholeloop:cli-bootstrap -->
> **CLI bootstrap** (no AI). Review every section, then run the **project-conventions** agent
> in your IDE to complete, correct, and confirm with you before relying on other WholeLoop agents.


> Replace `WL-IDE-setup` and all sections with your real stack. Agents load this file **before** touching code.

## 1. What this product is

_No README found — describe the product with the **project-conventions** agent._

- **Out of scope:** <!-- TODO: confirm with project-conventions agent -->


## 2. Repository layout

- <!-- TODO: confirm with project-conventions agent -->

- **Product repo (specs):** <!-- TODO: confirm with project-conventions agent --> e.g. `../product-repo/specs/`


## 3. Stack

| Layer | Technology | Version / notes |
|-------|------------|-----------------|
| Runtime | <!-- TODO: confirm with project-conventions agent --> | |
| Package manager | <!-- TODO: confirm with project-conventions agent --> | |
| Tests | <!-- TODO: confirm with project-conventions agent --> | |
| Linter / formatter | <!-- TODO: confirm with project-conventions agent --> | |


## 4. Rules agents must follow

- Import / module conventions.
- Where tests live.
- Forbidden paths (e.g. do not edit `infra/` without ticket).
- Secrets: never commit; env var names for client vs server.

## 5. Issue tracker (required)

| Setting | Value |
|---------|--------|
| **provider** | <!-- TODO: confirm with project-conventions agent -->| `jira` \| `manual` |
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
| **Epic / stories at spec-review** | Dev pastes epic description + story table in chat |
| **Handoff** | Human copies `tracker_comment_markdown` into their tool |

## 6. WholeLoop run paths

| Path | Purpose |
|------|---------|
| `workspace/runs/<run-key>/context.json` | Run context (spec-review writes base fields) |
| `workspace/runs/<run-key>/design-notes.md` | Optional ui-ux-designer Phase B |
| `workspace/runs/<run-key>/<story-key>/plan.md` | Per-story plan (planner → builder/manual) |
| `workspace/runs/<run-key>/.done` | handoff marks run complete |
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
