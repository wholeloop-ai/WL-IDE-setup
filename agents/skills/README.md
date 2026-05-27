# Skills — how to use this folder

- Each subdirectory is one **agent**; `SKILL.md` is the prompt body.
- Copy this entire `agents/skills` tree to **`<your-app>/.agents/skills/`** (see `install/copy-skills-to-repo.sh`).
- Add **`references/project-conventions.md`** in the **target** repo (copy from `wholeloop/references/PROJECT_CONVENTIONS.template.md` and fill in).

Frontmatter `name` must match the folder name your orchestrator passes to `load_skill("<name>")`.
