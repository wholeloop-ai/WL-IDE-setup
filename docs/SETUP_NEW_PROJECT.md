# Setting up WholeLoop on a new project

## Checklist

1. [ ] Choose **artifact naming** (`ARTIFACT-<ORG>-<id>.md` or similar).
2. [ ] Copy **`agents/skills/`** from this repo into `<app>/.agents/skills/`.
3. [ ] Create **`references/project-conventions.md`** from `references/PROJECT_CONVENTIONS.template.md` — list stack, forbidden paths, test commands, env vars.
4. [ ] Add **`inbox/`** and **`workspace/`**; add `workspace/` to **`.gitignore`** (patterns in GUIDELINES).
5. [ ] Wire **orchestrator** (copy from reference implementation or build minimal runner that loads `SKILL.md` + calls your LLM API).
6. [ ] Add **`.env.local`** with model API key; never commit it.
7. [ ] Document in your app **README** how PM drops artifacts and how devs run the pipeline.
8. [ ] (Optional) **CI** — block merges that touch forbidden paths on `ui-only` labels, etc.

## Cursor-only mode (no Python)

Some teams run WholeLoop **manually**:

1. PM drops artifact in repo (or pastes into Cursor).
2. Human invokes skills in order (Composer / Agent with skill name).
3. Human updates `workspace/context.json` by hand or lets each agent append JSON.

This repo’s **skills** are still the source of truth for prompts; you lose automation, gates, and event logs unless you add scripts later.

## Install script (optional)

From anywhere (use absolute path to this repo):

```bash
bash /path/to/wholeloop/install/copy-skills-to-repo.sh /absolute/path/to/your-app
bash /path/to/wholeloop/install/copy-skills-to-repo.sh /absolute/path/to/your-app --force
```

Copies `agents/skills` → `<your-app>/.agents/skills` (`--force` overwrites). If the script is not executable after clone: `chmod +x wholeloop/install/copy-skills-to-repo.sh`.
