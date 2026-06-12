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
| **spec_id_pattern** | `ARTIFACT-<PREFIX>-NNN` (from product repo `wholeloop-product.json`) |
| **Default spec path** | `../product-repo/inbox/{spec_id}.md` |

PM creates stories **after** spec `status: approved`. See WholeLoop **`docs/TRACKERS.md`**.

### If `linear`

| Setting | Value |
|---------|--------|
| **Strategy** | `label` \| `epic_parent` \| `custom_field` |
| **Label prefix** | e.g. `spec:` → `spec:ARTIFACT-<PREFIX>-042` |
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
