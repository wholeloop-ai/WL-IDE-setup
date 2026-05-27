# WholeLoop — team guidelines

Use this document with **README.md** when onboarding a team to WholeLoop on a new repository or monorepo.

## 1. Terminology

| Term | Meaning |
|------|---------|
| **Artifact** | The inbound spec file (e.g. `ARTIFACT-PROJ-42-feature.md`) dropped in `inbox/`. |
| **ADWF** | Agentic Delivery Workflow — the ordered pipeline with gates. |
| **Skill** | A `SKILL.md` file: YAML frontmatter + markdown instructions for one agent role. |
| **Gate** | A pause for human (or PM UI) approval before the next expensive or irreversible step. |
| **Workspace** | Ephemeral directory for `context.json`, reports, screenshots — **not** long-lived product docs. |

## 2. Repository layout (in each app repo)

Recommended (compatible with Walliu reference orchestrator):

```text
<app>/
├── .agents/
│   └── skills/
│       ├── spec-validator/SKILL.md
│       ├── analyser/SKILL.md
│       ├── planner/SKILL.md
│       ├── migration/SKILL.md      # optional — SQL-only repos
│       ├── ui-ux-designer/SKILL.md # optional — frontend tickets
│       ├── builder/SKILL.md
│       ├── ui-tester/SKILL.md      # optional
│       ├── reviewer/SKILL.md
│       ├── pr-agent/SKILL.md
│       ├── handoff/SKILL.md        # optional — closure + tracker + cleanup
│       └── references/
│           └── project-conventions.md   # YOUR stack — maintain this
├── inbox/                    # inbound artifacts (gitignore active queue if you prefer)
├── workspace/                # ephemeral — strong .gitignore
├── orchestrator.py           # your runner (or copy from reference impl.)
└── .env.local                # API keys — never commit
```

**Cursor / IDE:** Many teams also mirror skills under `.cursor/skills/` for **manual** agent invocation. Pick **one** source of truth to avoid drift:

- **Option A** — Only `.agents/skills/` (orchestrator + symlink from `.cursor` if needed).
- **Option B** — Only `.cursor/skills/` and set `SKILLS_DIR` in orchestrator to that path.

Document the choice in your app `CONTRIBUTING.md`.

## 3. Environment variables (typical)

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | LLM calls from Python orchestrator (or swap for your provider). |
| `SKILLS_DIR` | Path to folder containing `*/SKILL.md` (default `.agents/skills`). |
| `INBOX_DIR`, `WORKSPACE_DIR` | Artifact queue and run scratch space. |
| `LINEAR_API_KEY` | Optional — handoff posts issue comment (see skill `handoff`). |
| `WHOLELOOP_HANDOFF_ROOT` | Optional — root repo path where handoff markdown is written (your “product doc” repo). |
| `LINEAR_SKIP` | `1` to skip Linear API. |

Rename or extend per project (e.g. Jira instead of Linear — fork `handoff` skill).

## 4. Artifact naming

Define a **prefix** and **ID scheme** per org (e.g. `ARTIFACT-ACME-123.md`). The orchestrator should watch `ARTIFACT-*.md` or your glob. Document:

- Where specs are authored (Notion, internal repo, PM tool export).
- Who may drop files into `inbox/`.

## 5. Gates (minimum viable)

| Gate | Typical trigger |
|------|-----------------|
| **spec** | After spec-validator output. |
| **plan** | After planner + scope validation. |
| **design** | If `ui-ux-designer` ran. |
| **pr** | After `pr-agent` opens PR. |

You can start with **terminal-only** gates (`input()` or a simple HTTP gate) before investing in WholeLoop UI or n8n.

## 6. Security

- Never commit API keys or customer data from `workspace/`.
- `reviewer` skill should include “no secrets in diff” for your stack.
- Restrict which paths `builder` / `migration` may touch (enforce in planner + CI path filters).

## 7. Multi-repo / monorepo

- **One orchestrator per app repo** is simplest.
- If one ticket spans two repos, split into **two artifacts** or run orchestrator twice with linked ticket IDs in the handoff doc.

## 8. Updating from this template

1. Diff `agents/skills/` in this repo vs your app `.agents/skills/`.
2. Merge generic improvements; keep your `project-conventions.md` and any custom agents.

## 9. Support

Issues and discussions live in **this** `wholeloop` repository. Product-specific bugs belong in each application’s repo.
