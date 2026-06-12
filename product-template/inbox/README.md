# Inbox (product repo)

When `build-spec` completes:

1. Writes `Features/<slug>/ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md`
2. Copies to `inbox/ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md`
3. Copy to **`{{APP_REPO}}/inbox/`** (or path in org-repositories.md)

Delivery runs in the app repo via WholeLoop **spec-review** (see `wholeloop init` in {{APP_REPO}}).

Do not commit secrets. Artefacts only.
