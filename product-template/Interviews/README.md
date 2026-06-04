# Interviews

Customer evidence pipeline.

| Path | Edit policy |
|------|-------------|
| `raw/` | **Immutable** — never edit transcripts |
| `processed/` | One YAML per interview; agent creates from `synthesize-interview` |
| `synthesis/master.yaml` | Rollup; agent-managed sections + PM hand-edited |

**Skill:** `.cursor/skills/synthesize-interview/`
