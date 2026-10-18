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

1. Find every reader of runs/subagents/index.jsonl (grep -rn index.jsonl deskops tests). 2. In deskops/services/closure.py, after the closing commit is made, write the index line, stage it, and amend that same closing commit once (git commit --amend --no-edit); the amend only touches the commit this command just made. Amending changes the hash, so the line cannot hold the final hash: record task_id, run_dir and the Task-Id trailer, and set commit to null, or drop the field if no reader needs it; readers resolve the closing commit with git log --grep 'Task-Id: <id>'. If a reader needs the hash, choose a rule that keeps it working and explain the choice in result-summary.md. 3. Keep closeout verify and every index reader working. 4. Describe the rule in the ClosureService docstring.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_closeout.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

A test runs `closeout commit` (both routes) in a sandbox repo and asserts `git status --porcelain` is empty afterwards and the index line identifies the closing task, and `pytest tests` is green.
