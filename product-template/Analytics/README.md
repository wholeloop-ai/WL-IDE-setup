# Analytics

Dated snapshots from **PostHog** (exports, notebook PDFs, or markdown summaries).

Naming: `YYYY-MM-DD-<topic>.md` or `YYYY-MM-DD-posthog-export.json`

**Rules:**
- Link each insight to `Interviews/synthesis/master.yaml` themes when possible.
- Metrics complement interviews and `Surveys/` synthesis; they do not replace `quote_refs` or survey `response_refs`.
- Survey **response text** and NPS themes → `Surveys/` via `synthesize-survey`, not only Analytics.
- Update `Context/analytics-snapshot.md` with rollup pointers after each snapshot.

Do not store API keys or raw PII exports in git.
