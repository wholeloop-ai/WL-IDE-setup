# Skills — how to use this folder

- Each subdirectory is one **agent**; `SKILL.md` is the prompt body.
- Installed into **`<your-app>/.agents/skills/`** with `wholeloop init` ([install/README.md](../../install/README.md)).
- Specs: **product** repo. Stories: **Linear**, **Jira**, or **manual** — see **`docs/TRACKERS.md`**.

## Default pipeline (v0.2)

```text
project-conventions (once per repo, human approve)

spec-review → [ui-ux-designer Phase B] → planner → builder|manual
  → reviewer → pr-agent → handoff
```

**IDEs:** `.cursor/skills` and `.claude/skills` symlink here; VS Code uses `WHOLELOOP.md` + these paths.

## Skills tree

```text
agents/skills/
├── builder/
├── handoff/
├── migration/
├── planner/
├── pr-agent/
├── project-conventions/
├── references/
├── reviewer/
├── spec-review/
├── ui-tester/
└── ui-ux-designer/
```

Removed in v0.2: `spec-validator/`, `analyser/`, `tracker-intake/` (merged into **spec-review**).

See **`docs/WORKFLOW_PRODUCT_LINEAR.md`** and **`docs/IDE_SETUP.md`**.
