# Agent: synthesize-survey

Same playbook as `.cursor/skills/synthesize-survey/SKILL.md`.

Invoke when anonymized survey data lands in `Surveys/raw/` or after a PostHog survey period ends.

**Outputs:** `Surveys/processed/*.yaml`, `Surveys/synthesis/rollup.yaml`, survey fields on `Interviews/synthesis/master.yaml`.

**Do not** use for interviews or team meetings.
