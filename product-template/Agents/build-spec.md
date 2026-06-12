# build-spec

**Job:** `scope.yaml` (scoped, gates answered) → `ARTIFACT-{{ARTIFACT_PREFIX}}-<NNN>.md` + `inbox/` copy.

**Handoff:** copy artifact to `{{APP_REPO}}/inbox/` → run **spec-review** in the app repo.

**Stop** if any `validation_gates.status: open`.

**Full skill:** [.cursor/skills/build-spec/SKILL.md](../.cursor/skills/build-spec/SKILL.md)

**Invoke:** "Build the spec for Features/<slug>/scope.yaml"
