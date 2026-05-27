# {{PROJECT_NAME}} — project conventions (template)

> Replace `{{PROJECT_NAME}}` and all sections with your real stack. Agents load this file **before** touching code.

## 1. What this product is

- One paragraph: user, problem, what is **out of scope** (e.g. payments).

## 2. Repository layout

- Tree of important directories (`src/`, `api/`, `packages/foo`, …).

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

## 5. Definition of Done

- Tests required per change type.
- Docs to update when schema or public API changes.

## 6. Links

- Design system / Figma.
- Issue tracker project URL.
- Runbooks.
