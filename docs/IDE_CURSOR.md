# WholeLoop + Cursor IDE

## Option 1 — Cursor Agent Skills (recommended)

1. Copy `agents/skills/*` into your app at **`.cursor/skills/<name>/SKILL.md`** *or* keep under `.agents/skills/` and add a **rule** that tells the AI to read those paths.

2. In **Cursor Settings → Rules**, add something like:

   > When working on a ticket from `inbox/ARTIFACT-*.md`, follow the WholeLoop sequence: spec-validator → analyser → planner → … Use `.agents/skills/<agent>/SKILL.md` as the system prompt for that step.

3. Optional: add a **`.cursor/rules/wholeloop.mdc`** (project rule) with the same workflow and links to `project-conventions.md`.

## Option 2 — Symlink (single source of truth)

If the canonical skills live in a git submodule or monorepo path:

```bash
ln -s ../wholeloop/agents/skills .agents/skills
```

Point `SKILLS_DIR` in your orchestrator to `.agents/skills`.

## Option 3 — MCP + manual

Use **Linear**, **GitHub**, or other MCP servers from Cursor for issue/PR actions; keep WholeLoop skills for **implementation discipline** only.

## Skill frontmatter

Cursor discovers skills via YAML frontmatter (`name`, `description`). Keep descriptions **short** and **trigger-oriented** so the right skill is suggested.

## Conflicts

If both `.cursor/skills` and `.agents/skills` exist, **delete or symlink one** — document which is canonical in your repo README.
