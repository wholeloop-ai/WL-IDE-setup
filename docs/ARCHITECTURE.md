# WholeLoop architecture

## Pipeline (default)

```text
                    ┌─────────────────┐
   inbox/ARTIFACT-*  │  spec-validator │──► gate: spec
          ─────────►│  (+ human gate) │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    analyser     │  reads repo + artifact
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │     planner     │──► gate: plan
                    │ scope_validation│
                    └────────┬────────┘
                             ▼
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌────────────────┐            ┌──────────────┐
     │ ui-ux-designer │──► gate    │  migration   │  (optional, SQL-only)
     │    (optional)  │   design   └──────┬───────┘
     └────────┬───────┘                   │
              ▼                           ▼
     ┌────────────────┐            ┌──────────────┐
     │    builder     │            │   builder    │  (if not migration-only)
     └────────┬───────┘            └──────┬───────┘
              └────────────┬─────────────┘
                           ▼
                    ┌─────────────────┐
                    │   ui-tester     │  (optional)
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    reviewer     │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    pr-agent     │──► gate: pr
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    handoff      │  optional: doc + tracker + cleanup
                    └─────────────────┘
```

## Context object

Runs accumulate structured JSON (Walliu uses `workspace/context.json` keys: `spec_validation`, `codebase_analysis`, `execution_plan`, `build`, `review`, `pr`, `handoff`, …). Your orchestrator should:

1. Merge each agent’s JSON output into the context blob.
2. Pass the full context to the next agent (plus `project-conventions.md`).

## Events (optional)

Emit JSON lines or HTTP webhooks per step (`agent:started`, `gate:waiting`, `run:complete`) for observability or a PM dashboard.

## Extending agents

- Add a folder `agents/skills/my-agent/SKILL.md`.
- Teach `planner` when to route to `my-agent`.
- Implement `call_agent("my-agent", ctx)` in your orchestrator.

Keep **planner** as the single place that defines allowed agent order for a ticket type.
