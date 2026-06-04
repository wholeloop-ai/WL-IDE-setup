# Surveys — B2C qualitative signals at scale

Encuestas in-product (PostHog Surveys) y herramientas externas aportan señales que **complementan** entrevistas: volumen alto, contexto de uso, pero menos profundidad y sin sustituir `quote_refs` de entrevistas.

| Path | Edit policy |
|------|-------------|
| `registry.yaml` | Catálogo de encuestas activas (IDs, triggers, enlaces PostHog) — PM + agent |
| `raw/` | Export anonimizado (CSV/JSON). **No PII en git** — ver README en `raw/` |
| `processed/` | Un YAML por ventana de análisis (`synthesize-survey`) |
| `synthesis/rollup.yaml` | Rollup cross-survey; alimenta `Interviews/synthesis/master.yaml` |

**Skill:** `.cursor/skills/synthesize-survey/`

**Peso ICP (discovery):** señal agregada de encuesta = **0.4** por tema/feature_signal documentado (vs entrevista ICP1 = 1.0). Ver `Context/signals-sources.md`.

**Relación con Analytics/** — métricas de embudo y volumen (`survey shown` / `survey sent`) viven en snapshots PostHog; **significado** de respuestas abiertas y NPS vive aquí.
