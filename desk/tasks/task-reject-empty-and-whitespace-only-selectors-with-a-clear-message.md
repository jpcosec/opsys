---
id: task-reject-empty-and-whitespace-only-selectors-with-a-clear-message
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message
current_node: checklist-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message-testing-ready
history:
- operator-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message-activate
references:
- tests/test_cli.py
- d42a3e3
- desk/atoms/workflow-model/atom-reports-carry-minimal-reproduction-evidence.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message-execution-ready
- checklist-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message-testing-ready
- checklist-task-reject-empty-and-whitespace-only-selectors-with-a-clear-message-closeout-ready
task_type: bugfix
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Reject empty and whitespace-only selectors with a clear message

## Rationale

_Explain why this task exists or the business driver behind it._

desk/drawer/issues/issue-empty-selector-validation-error.md: an empty selector is not rejected, so it resolves to whatever matches first and the user gets a Pydantic error about a document they never named (show task "" reports the board's missing status field). An empty selector is the most likely typo, an unset shell variable.

## Goal

_Describe the concrete result this task must produce._

Every selector-taking command rejects an empty or whitespace-only selector before any lookup, naming the command and the subject.

## Scope

_State what is in scope and what is out of scope._

Selector validation in the CLI and the artifact resolution helpers. Also re-verify against the current CLI the items in desk/drawer/issues/issue-stress-test-fix-backlog.md phases 1 and 3 and fix the ones that still reproduce; report the rest as already fixed. Does not touch graph, store or identity code.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/cli/parser.py or the command entry points for validation at the boundary; deskops/operations.py _resolve_artifact_selector for defence in depth. Tests in tests/test_cli.py. The backlog issue lists the exact commands to re-run for phases 1 and 3.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py tests/test_operational.py -q

## Done When

_Name the observable condition that makes the task complete._

No command accepts an empty selector, the confirmed backlog items from phases 1 and 3 are fixed or reported fixed, and the suite is green.
