# Skills — how to use this folder

- Each subdirectory is one **agent**; `SKILL.md` is the prompt body.
- Copy to **`<your-app>/.agents/skills/`** via `install/copy-skills-to-repo.sh`.
- Specs: **product** repo (`references/SPEC.template.md`). Stories: **Linear**, **Jira**, or **manual** — see **`docs/TRACKERS.md`**.

## Default pipeline

```text
tracker-intake → spec-validator → analyser → planner → … → handoff
```

**IDEs:** `.cursor/skills` and `.claude/skills` symlink here; VS Code uses `WHOLELOOP.md` + these paths.

See **`docs/WORKFLOW_PRODUCT_LINEAR.md`** and **`docs/IDE_SETUP.md`**.
