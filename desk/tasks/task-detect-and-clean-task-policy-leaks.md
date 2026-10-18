---
id: task-detect-and-clean-task-policy-leaks
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/task_policy.py
- deskops/graph/self_reflection.py
- tests/test_task_policy_leaks.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Detect and clean global policy leaks in task files

## Rationale

_Explain why this task exists or the business driver behind it._

Task files should carry only task-local facts. Global workflow rules already live in rituals,
pills, AGENTS.md, and `docs/workflow-policy-reference.md`, but at least one active task restated global workflow rules. There is no drift check for this leakage.

## Goal

_Describe the concrete result this task must produce._

Add a review-only `task-policy-leak` finding to `deskops drift check`, then remove the current
leak from the active task set without changing any global policy text.

## Scope

_State what is in scope and what is out of scope._

In scope: a scanner module, its tests, wiring into `drift_check_knowledge_surfaces`, and cleanup of
the owner-link task (closed in 33c0482). Out of scope: closeout gate changes, new
task fields, changes to rituals or pills, and rewriting task rationale that merely names
`closeout` as the task subject.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `deskops/task_policy.py` with `TaskPolicyLeak` (`path`, `line`, `phrase`) and
   `scan_task_policy_leaks(root)`.
2. Scan only the body after frontmatter of `desk/tasks/task-*.md` and
   `desk/drawer/tasks/task-*.md`; skip `Board.md`. Do not scan frontmatter.
3. Use sentence-level regexes, not single keywords:
   `\b(supervisor|executor)\b.*\b(commit|promote|close)`, `\bclosing always requires\b`,
   `\bevery closed task\b`, `\bphase\b.*\bgate\b`, `\bdo not skip\b`.
4. Append `task-policy-leak: <path>:<line> repeats global policy phrase '<phrase>'; reference
   desk/rituals/closeout.md or a pill instead` in `drift_check_knowledge_surfaces`.
5. Remove the two global-policy sentences in
   the owner-link task (closed in 33c0482) ("The supervisor promotes ..." and
   "Closing always requires ..."). Keep the task-specific reproduction and done-when.
6. Add `tests/test_task_policy_leaks.py`: a leaked sentence is found once; a task-local validation
   line such as `a task-specific pytest command` is not found; frontmatter is ignored; the scanner does
   not modify task bytes.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_task_policy_leaks.py -q
- python -m pytest tests/test_graph_self_reflection.py -q
- python -m deskops drift check --root .
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

`deskops drift check` prints no `task-policy-leak` finding for the repository, a synthetic leaked
sentence produces exactly one finding, and all listed tests pass.
