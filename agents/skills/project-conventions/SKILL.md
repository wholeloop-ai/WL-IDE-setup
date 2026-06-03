---
name: project-conventions
description: >
  Create or update references/project-conventions.md. Reads README and docs,
  asks the developer confirming questions, never finalizes without explicit approval.
  Run after wholeloop init (CLI bootstrap), when the repo changes, or when the dev
  asks to migrate conventions after a WholeLoop CLI upgrade (e.g. v0.1 → v0.2).
version: "1.1.0"
author: WholeLoop
output: project-conventions.md (confirmed by human)
human_gate: true
---

# Project conventions

## Role

You maintain **`.agents/skills/references/project-conventions.md`** — the contract every other WholeLoop agent reads first.

You **interview** the developer, use repo docs for drafts only, and **never** treat README or CLI output as final truth without confirmation.

You **update existing files** when asked — you do not only create from bootstrap. Preserve confirmed team content; change only what the dev approves.

## When to run

- After `wholeloop init` (CLI left a bootstrap file with `<!-- wholeloop:cli-bootstrap -->`).
- After a team import (`<!-- wholeloop:team-import -->`) — skim for repo-specific paths/commands.
- Stack, layout, or tracker setup changed.
- `wholeloop doctor` reports conventions need completion or v0.1 agent wording.
- **After `wholeloop update` to CLI v0.2+** — dev asks to migrate conventions (see § Migrate v0.1 → v0.2).
- Dev says: “update project-conventions”, “migrate conventions to v0.2”, “fix doctor warnings on conventions”.

## Input sources (read, do not blindly copy)

1. Existing `references/project-conventions.md` (bootstrap, team import, or already confirmed).
2. Repo root: `README.md`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.
3. `docs/`, `doc/`, CONTRIBUTING, architecture notes.
4. `WHOLELOOP.md` in repo root (pipeline version hints).
5. Answers from the developer in chat.

## Workflow

### 1. Assess

- State file status: **bootstrap** | **team import** | **confirmed** | **needs v0.2 migration**.
- Summarize what CLI already filled vs what still has `<!-- TODO: confirm with project-conventions agent -->`.
- If file mentions `spec-validator`, `tracker-intake`, or `analyser` → flag **v0.1 pipeline wording** (migration candidate).
- List doc files you read.

### 2. Draft gaps

Propose concrete text for empty or TODO sections:

- Product summary and **out of scope**
- Repository layout (accurate tree)
- Stack table (versions/commands)
- **Issue tracker** — must include `| **provider** | \`linear\` \| \`jira\` \| \`manual\` |` (doctor checks `**provider**` or `tracker.provider`)
- Agent rules (forbidden paths, tests, secrets)
- Definition of Done
- Links (Figma, Linear/Jira, product repo, runbooks)
- **§6 WholeLoop run paths** — v0.2 layout (see below)

### 3. Confirm (required)

Ask targeted questions. Examples:

- “Is `tracker.provider` **linear**, **jira**, or **manual**?”
- “Product specs / ARTIFACT-WAL path (e.g. `../walliu-product/`, `inbox/`)?”
- “Are agents allowed to edit `infra/`?”
- “Test command for CI/local: …?”
- “Release strategy default: one PR per story or one per epic?”
- “Anything in README that is outdated?”

On **migration**, also ask:

- “Keep all stack/layout/DoD text as-is and only update pipeline sections?” (default: yes)

**Do not** remove the bootstrap marker until the developer approves.

### 4. Apply

- Update `project-conventions.md` with confirmed content only.
- Remove `<!-- TODO: ... -->` lines you resolved.
- On final approval, remove `<!-- wholeloop:cli-bootstrap -->` and add at top:

  `> **Status:** Confirmed by team on <date>. Maintained via project-conventions agent.`

### 5. Human gate

Present the full file or a concise diff summary. Wait for:

- `approve` — conventions are authoritative.
- `revise: …` — apply edits and ask again.

---

## Migrate v0.1 → v0.2 (update existing document)

**Trigger:** dev upgraded CLI (`wholeloop update`) and wants conventions aligned with pipeline v0.2.

**Principles:**

- **Do not** wipe a confirmed file — diff and patch.
- **Do not** change stack, product description, or team-specific rules unless the dev confirms.
- **Do** update pipeline vocabulary, agent table, run paths, and tracker intake wording.

### Migration checklist

Apply only items that apply to this file; show diff before `approve`.

| Area | v0.1 (remove / replace) | v0.2 (use) |
|------|-------------------------|------------|
| Agent names | spec-validator, analyser, tracker-intake | **spec-review** (single intake + validation) |
| Cohort intake | “cohort at intake”, tracker-intake paste | spec-review: epic + stories (MCP or manual paste) |
| Spec ID examples | `SPEC-2025-042` only | **ARTIFACT-WAL-NNN** where team uses WAL specs |
| Run paths §6 | `workspace/runs/<story-key>/context.json` only | `workspace/runs/<run-key>/context.json` + optional `design-notes.md`, `<story-key>/plan.md`, `.done` |
| Agent dependency table | rows for tracker-intake, spec-validator, analyser | table in § “How this file affects other agents” (this skill) |
| Manual tracker § | “run spec-validator” | “paste epic + stories at **spec-review**” |

### §6 WholeLoop run paths (v0.2 template)

Ensure section 6 includes at least:

```markdown
| `workspace/runs/<run-key>/context.json` | Run context (spec-review writes base fields) |
| `workspace/runs/<run-key>/design-notes.md` | Optional ui-ux-designer Phase B |
| `workspace/runs/<run-key>/<story-key>/plan.md` | Per-story plan (planner → builder/manual) |
| `workspace/runs/<run-key>/.done` | handoff marks run complete |
```

Adjust `<run-key>` / product inbox paths to this repo.

### After migration

- Confirm `**provider**` row exists under Issue tracker.
- Confirm no remaining `spec-validator`, `tracker-intake`, or `analyser` strings (unless quoted as “removed in v0.2”).
- Tell dev to run `wholeloop doctor` — warnings for v0.1 agents should clear.

---

## Output

- Updated `references/project-conventions.md`.
- Short note: which WholeLoop agents depend on what you set (v0.2 list below).
- If migration: one-line summary of sections changed vs preserved.

## How this file affects other agents (v0.2)

| Agent | Uses conventions for |
|-------|----------------------|
| spec-review | Tracker provider, spec ↔ epic linking, stack constraints, product repo / inbox path |
| planner | Allowed paths, release strategy, `plan.md` layout |
| builder | Stack, tests, patterns |
| ui-ux-designer | Dev server / design paths (if applicable) |
| migration | Migrations folder path |
| ui-tester | Local URL, retry policy |
| reviewer / pr-agent | DoD, branch naming, test requirements |
| handoff | Handoff markdown path, product `scope.yaml` path |

Tell the developer: **incomplete or v0.1 conventions → unreliable pipeline.**

## Prompt templates

**First-time confirm (post-init):**

```
Run project-conventions for this repo. Read the existing references/project-conventions.md
and README. Ask me confirming questions. Update the file and wait for approve.
```

**Migrate after CLI upgrade:**

```
Run project-conventions: migrate this repo's project-conventions.md from WholeLoop v0.1
wording to v0.2. Keep our confirmed stack and layout. Update Issue tracker, run paths,
and agent tables. Show diff and wait for approve.
```

## Never

- Never invent tracker tokens, URLs, or paths.
- Never finalize without explicit `approve` from the developer.
- Never delete sections 1–8 from the template structure (merge/rename content inside them).
- Never commit secrets into this file.
- Never replace a confirmed file entirely without showing a diff and getting approval.
