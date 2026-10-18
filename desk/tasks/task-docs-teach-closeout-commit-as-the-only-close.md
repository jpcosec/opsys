---
id: task-docs-teach-closeout-commit-as-the-only-close
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f3-single-closure-path
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- docs/quickstart.md
- docs/faq.md
- .pi/skills/use-deskops/SKILL.md
- .opencode/skills/use-deskops/SKILL.md
- docs/diagrams/process/current-agent-workflow-and-automation.md
- docs/diagrams/process/current-agent-workflow-and-automation.mmd
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-docs-teach-closeout-commit-as-the-only-close.md
---

# Docs and skills teach `closeout commit` as the only way to close a task

## Rationale

_Explain why this task exists or the business driver behind it._

task-rw-f3-single-closure-path (owner decision A, 2026-10-18) makes `deskops advance` stop closing. The terminal transition and `--to complete` refuse and point at `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. These surfaces still teach closing a task with `advance`: docs/quickstart.md, docs/faq.md, .pi/skills/use-deskops/SKILL.md, .opencode/skills/use-deskops/SKILL.md, and docs/diagrams/process/current-agent-workflow-and-automation.{md,mmd} (found with `grep -rln "advance task"`). The agent e2e suite (tests/e2e_agent, owned by the SLDB_1 coordinator) has a cheap agent learn deskops from these docs.

## Goal

_Describe the concrete result this task must produce._

Every doc and skill that walks through closing a task uses `deskops closeout commit` and says that `advance` stops at the closeout node.

## Scope

_State what is in scope and what is out of scope._

In scope: the files listed above, plus any other hit of the grep in Validation. Out of scope: tests/e2e_agent, whose owner is the coordinator, and desk/drawer/ history.

## Implementation Path

_Outline the expected implementation route or affected surface._

Find every passage that closes a task with `advance`. Rewrite it to: advance to the closeout node, set references and files, then `deskops closeout commit`, with the two routes. Keep `advance` for the non-terminal steps.

## Validation

_List the checks required before this task can close._

- grep -rn "advance task" docs README.md .pi/skills .opencode/skills
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

No doc or skill describes `advance` as closing a task, and `pytest tests` is green (the skill drift guard included).

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
