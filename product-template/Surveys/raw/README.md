# Survey raw exports

Place **anonymized** exports here before running `synthesize-survey`.

## Allowed in git

- Aggregated CSV/JSON from PostHog UI (Results → export) with columns stripped of email, name, `distinct_id`, IP
- Redacted open-text only if no identifying details

## Do not commit

- Full PostHog person exports
- Files with `distinct_id`, email, phone, or free text that could identify a person

## Naming

`YYYY-MM-DD-<tool>-<survey-slug>.{json,csv}`

Examples:

- `2026-06-01-posthog-nps-product.json`
- `2026-06-01-typeform-onboarding-exit.csv`

If exports are sensitive, keep them locally and pass only the file path to the agent in chat (do not add to repo).
