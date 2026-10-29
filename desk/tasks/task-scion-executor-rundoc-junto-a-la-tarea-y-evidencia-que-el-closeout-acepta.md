---
id: task-scion-executor-rundoc-junto-a-la-tarea-y-evidencia-que-el-closeout-acepta
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- c594a86
- 695308e
- tests/test_scion_runtime.py
- atom-role-prompts-are-tracked-documents-agent-files-are-materializations
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Scion executor: RunDoc junto a la tarea y evidencia que el closeout acepta

## Rationale

_Explain why this task exists or the business driver behind it._

Los dos primeros despachos reales (sldb serve y store-generalize) mostraron que el RunDoc iba al repo del rol y no al de la tarea, que el agente crea su propio run dir, y que el closeout rechaza un run dir sin board.txt/git-status.txt.

## Goal

_Describe the concrete result this task must produce._

deskops runtime template acepta --task-root y --run-dir, y el agents.md generado pide los snapshots que closeout commit --run-dir exige.

## Scope

_State what is in scope and what is out of scope._

deskops/runtime/scion.py, cli/registry.py, cli/commands/runtime.py, tests/test_scion_runtime.py, golden de help.

## Implementation Path

_Outline the expected implementation route or affected surface._

commits c594a86 y 695308e

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_scion_runtime.py

## Done When

_Name the observable condition that makes the task complete._

11 tests verdes; un executor nuevo deja board.txt y git-status.txt sin intervención del supervisor.
