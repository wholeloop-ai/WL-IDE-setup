# Changelog

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
