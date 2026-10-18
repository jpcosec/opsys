---
id: task-closeout-commit-leaves-the-run-index-clean
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/services/closure.py
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `closeout commit` leaves the run index clean

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 while closing tasks through the single closure path (a0e00e3); graph-ui-59 hit it too (it amended the line into ae4eb2e). `deskops closeout commit` appends the closing commit's hash to runs/subagents/index.jsonl after making the commit, so every close leaves the tree dirty. The supervisor has been committing that line separately ("runs: registra el hash de cierre ..."), which doubles the commits per task.

## Goal

_Describe the concrete result this task must produce._

After `deskops closeout commit` (both --run-dir and --no-run) the working tree is clean, and runs/subagents/index.jsonl still records the closing commit's hash.

## Scope

_State what is in scope and what is out of scope._

In scope: how deskops/services/closure.py records the index entry, the closeout ritual text in desk/rituals/closeout.md if it describes the index, and tests. Out of scope: rewriting older index entries.

## Implementation Path

_Outline the expected implementation route or affected surface._

Recommended rule: write the index line, stage it, and amend the closing commit once with `git commit --amend --no-edit` (the closing commit is the one this command just made, so the amend only touches its own commit). The hash recorded must then be the final, amended hash; since the hash changes when the file changes, record the line keyed by Task-Id with the commit hash of the closing commit's parent-free content is impossible, so instead: (a) make the commit, (b) compute nothing in-file that depends on the final hash: write the line with `"commit": null` plus `"task_id"`, stage it, amend; then the index is resolvable through `git log --grep "Task-Id: <id>"`. Pick whichever of these two keeps `deskops closeout verify` and runs readers working; grep for readers of index.jsonl (`grep -rn index.jsonl deskops tests`) and keep them passing. Document the rule in the code docstring.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_closeout.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

A test runs `closeout commit` (both routes) in a sandbox repo and asserts `git status --porcelain` is empty afterwards and the index line identifies the closing task, and `pytest tests` is green.
