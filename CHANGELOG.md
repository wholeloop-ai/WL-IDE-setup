# Changelog

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
