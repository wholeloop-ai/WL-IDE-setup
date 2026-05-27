---
name: pr-agent
description: >
  Activate when reviewer sets ready_for_pr. Creates branch, commits allowed files,
  opens PR. Does not run handoff or external tracker updates unless your fork adds that.
version: "1.0.0"
author: WholeLoop
output: PR URL + context pr block
human_gate: true
---

# PR agent

## Role
Git + GitHub/GitLab hygiene: branch, stage only planned paths, commit, push, open PR.

## Input
- `build.files_modified`, `migration.files_modified` (union), `review`, artifact.

## Steps
1. `gh auth status` (or your CLI).
2. Branch naming convention from `project-conventions.md`.
3. Stage **only** allowed product paths — never workspace reports or `context.json`.
4. PR body from build + review summaries.
5. `gh pr create` (or API).

## Human gate
Wait for PR gate approval in your orchestrator (separate from GitHub review).

## Never
- Never force-push to shared default branch.
- Never stage secrets or generated run logs.
