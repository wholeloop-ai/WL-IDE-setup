# Changelog

## 0.3.4

- **Path prompts strip shell quotes.** Pasting a path like `'/Users/you/app'` no longer creates a folder literally named `'` — surrounding `'` and `"` are removed before resolving.
- **Project-specific spec IDs.** Product init derives an artifact prefix from the product name (e.g. HAYAverse→`HAYA`, Walliu→`WAL`) and writes `wholeloop-product.json`. Templates and `wholeloop link` use `ARTIFACT-<PREFIX>-NNN` instead of hardcoded `ARTIFACT-WAL`.

## 0.3.3

- **`app update` self-heals scaffolding:** it now recreates `workspace/runs/` and ensures `.gitignore` lists `workspace/` (previously only `init` did this, so updated-from-old repos failed `doctor`).

## 0.3.2

- **Wizard prompts are now menus, not free text.** Product location ("here / home / another") and app repo ("this folder / another path") are pick-a-number choices, so you can't accidentally type a value like `existing` or `yes` as a path. Custom paths are confirmed (absolute path shown) before anything is created.
- **Existing install handled mid-wizard:** if the chosen app folder already has WholeLoop, `setup` offers update / reinstall / skip instead of erroring and aborting.

## 0.3.1

- **Wizard UX:** `product init` / `setup` default to creating `<name>-product/` **in the current directory** (like `git init`), with options for `~/<name>-product` or another location.
- Pointing at an **existing folder** nests `<name>-product/` inside it instead of erroring on a non-empty directory; a new or empty path is used directly as the repo. Clearer prompt wording.

## 0.3.0

- **CLI UX (noun-verb):** `wholeloop product init|update` and `wholeloop app init|update`. `init`, `init-product`, and `update` remain as aliases.
- **Guided wizards:** `wholeloop setup` walks founders through product repo + app repo(s) in one interaction; `product init` and `app init` prompt when run in a terminal (TTY). `--yes` / `WHOLELOOP_NO_PROMPT=1` skip all prompts for CI.
- **Product link (closes the loop):** `wholeloop app init --product <path|url>` and `wholeloop link <product> [app]` write the product repo into `project-conventions.md` (§2, §5, §8) so spec-review finds the inbox and handoff knows where to append `delivery_notes`.
- **`wholeloop product update`:** refreshes only the PM skills (`.cursor/skills/`, `Agents/`) — never touches `Features/`, `Interviews/`, `Progress/`, `inbox/`, `Context/`.
- **`wholeloop doctor`:** new check for the product-repo link (warns when missing or unresolvable).
- **Config:** per-machine `~/.wholeloop/config.json` records the product repo and app repos for smart defaults (override dir with `WHOLELOOP_CONFIG_DIR`). Local only; no secrets.
- **Upgrade notices:** status commands check PyPI at most once a day and, if a newer release exists, print the CLI upgrade command plus the right per-repo update (`app update` vs `product update`). Best-effort, skipped for non-interactive output, opt out with `WHOLELOOP_NO_UPDATE_CHECK=1`.
- Running `wholeloop` with no command prints a role-oriented welcome.

## 0.2.2

- **CLI:** `wholeloop init-product <path>` scaffolds a sanitized product discovery repo (PM skills, folder layout).
- Bundle includes `product-template/` (generic placeholders, no customer-specific repo names).

## 0.2.1

- **project-conventions** skill v1.1: migrate existing conventions from v0.1 → v0.2 on developer request.

## 0.2.0

- **project-conventions** skill v1.1: migrate existing `project-conventions.md` from v0.1 → v0.2 when dev requests (preserve confirmed content).
- **CLI:** `wholeloop update` refreshes WHOLELOOP.md and IDE instruction files by default; `--no-refresh-docs` to skip.
- **CLI:** `wholeloop skills` lists bundled agents; `wholeloop doctor` validates v0.2 skills and warns on legacy installs.
- **CLI:** `python -m wholeloop` supported via `wholeloop/__main__.py`.
- **Breaking:** Merged **spec-validator**, **analyser**, and **tracker-intake** into **spec-review** (v2 pipeline).
- New skills: **spec-review**, **ui-ux-designer** (Phase A/B), **builder** (plan.md execution).
- **planner** v2.0: three epic modes + mid-run refinement (Mode 4) + `release_strategy` in context.json.
- **reviewer** v2.0: plan fidelity, `story_reviews` block; runs per story before **pr-agent**.
- **pr-agent** v2.0: story vs epic release strategy.
- **handoff** v3.0: `delivery_notes` → scope.yaml, roadmap signals, `.done` marker.
- Docs and templates updated for v0.2 run layout (`workspace/runs/<run-key>/`).

## 0.1.4

- Fix `conventions bootstrap` on repos missing `.agents/skills/references/` (create folder; was wrongly reported as missing `.agents/skills/` in 0.1.3).

## 0.1.3

- Fix `wholeloop conventions bootstrap`: import `references_dir` (was `NameError` in 0.1.2).
- Import team `project-conventions.md`: `init --conventions-from`, `conventions bootstrap --from`, `conventions import`, or interactive prompt on bootstrap (validates template sections).
- Bootstrap creates `references/` when missing (repos installed before that folder existed); clearer error if `.agents/skills/` is absent.

## 0.1.2

- Fix `wholeloop update` when restoring `project-conventions.md` (create `references/` parent dir).
- Run conventions bootstrap after update if no prior conventions file.
- Skill **project-conventions** (create/maintain conventions with human approval).
- CLI `wholeloop conventions bootstrap` (no AI).

## 0.1.1

- CLI bootstrap for `project-conventions.md` from README and stack detection.
- Skill **project-conventions**.

## 0.1.0

- Initial PyPI release: `wholeloop init`, `update`, `doctor`, dev skills bundle.
