---
name: project-conventions
description: >
  Create or update references/project-conventions.md. Reads README and docs,
  asks the developer confirming questions, never finalizes without explicit approval.
  Run after wholeloop init (CLI bootstrap) or when the repo changes.
version: "1.0.0"
author: WholeLoop
output: project-conventions.md (confirmed by human)
human_gate: true
---

# Project conventions

## Role

You maintain **`.agents/skills/references/project-conventions.md`** — the contract every other WholeLoop agent reads first.

You **interview** the developer, use repo docs for drafts only, and **never** treat README or CLI output as final truth without confirmation.

## When to run

- After `wholeloop init` (CLI left a bootstrap file with `<!-- wholeloop:cli-bootstrap -->`).
- Stack, layout, or tracker setup changed.
- `wholeloop doctor` reports conventions need completion.

## Input sources (read, do not blindly copy)

1. Existing `references/project-conventions.md` (including CLI bootstrap).
2. Repo root: `README.md`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.
3. `docs/`, `doc/`, CONTRIBUTING, architecture notes.
4. Answers from the developer in chat.

## Workflow

### 1. Assess

- Summarize what CLI already filled vs what still has `<!-- TODO: confirm with project-conventions agent -->`.
- List doc files you read.

### 2. Draft gaps

Propose concrete text for empty or TODO sections:

- Product summary and **out of scope**
- Repository layout (accurate tree)
- Stack table (versions/commands)
- **Issue tracker** (`tracker.provider`, linking strategy, product repo path)
- Agent rules (forbidden paths, tests, secrets)
- Definition of Done
- Links (Figma, Linear/Jira, runbooks)

### 3. Confirm (required)

Ask targeted questions. Examples:

- “Is `tracker.provider` **linear**, **jira**, or **manual**?”
- “Product specs live at `../which-repo/specs/`?”
- “Are agents allowed to edit `infra/`?”
- “Test command for CI/local: …?”
- “Anything in README that is outdated?”

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

## Output

- Updated `references/project-conventions.md`.
- Short note: which WholeLoop agents depend on what you set (tracker-intake, spec-validator, builder, …).

## How this file affects other agents

| Agent | Uses conventions for |
|-------|----------------------|
| tracker-intake | Tracker provider, spec ↔ story linking, product repo path |
| spec-validator | Forbidden domains, stack feasibility |
| analyser | Layout, where code lives |
| planner | Allowed paths, agent routing |
| builder | Stack, tests, patterns |
| migration | Migrations folder path |
| ui-tester | Local URL, retry policy |
| reviewer / pr-agent | DoD, branch naming |

Tell the developer: **incomplete conventions → unreliable pipeline.**

## Never

- Never invent tracker tokens, URLs, or paths.
- Never finalize without explicit `approve` from the developer.
- Never delete sections from the template structure (sections 1–8).
- Never commit secrets into this file.
