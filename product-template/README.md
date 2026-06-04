# {{PRODUCT_REPO}} — product discovery

**Product discovery** repo: evidence → decisions → roadmap → specs. Production code lives in sibling repos.

## Sibling repos

| Repo | Role |
|------|------|
| **{{APP_REPO}}** | App + WholeLoop delivery (`wholeloop init`) |
| **{{SCRAPER_REPO}}** | Optional ingestion / data service |
| **{{PRODUCT_REPO}}** | This repo |

## Handoff to engineering

When a spec is ready (`build-spec`):

1. `Features/<slug>/ARTIFACT-WAL-<NNN>.md`
2. Copy to `{{APP_REPO}}/inbox/` (or path in `Context/org-repositories.md`)
3. Run **spec-review** in the app repo

## PM agents (Cursor)

| Skill | When |
|-------|------|
| `synthesize-interview` | Transcript in `Interviews/raw/` |
| `synthesize-meeting` | Transcript in `Product Meetings/meetings/` |
| `brainstorm-feature` | → `Features/<slug>/scope.yaml` |
| `maintain-roadmap` | → `Context/roadmap-snapshot.md` |
| `build-spec` | → `ARTIFACT-WAL-*.md` + `inbox/` |

Install this layout: `wholeloop init-product <path>`
