---
id: task-drawer-al-dia-ritual-de-triage-readme-board-y-tarea-sin-frontmatter
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
- a8601fee
- desk/drawer/README.md
- tests/test_taskdoc_read_without_overlay.py
depends_on: []
pills: []
files:
- desk/rituals/ritual-drawer-triage.md
- desk/drawer/README.md
- desk/drawer/tasks/Board.md
- desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- commit
- document
---

# Drawer al dia: ritual de triage, README, board y tarea sin frontmatter

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Que el drawer describa la entrada real: el ritual no promete promocion directa, el README y el board listan las tareas diferidas que existen y toda tarea del drawer se lee como TaskDoc.

## Scope

_State what is in scope and what is out of scope._

Solo desk/rituals/ritual-drawer-triage.md, desk/drawer/README.md, desk/drawer/tasks/Board.md, el frontmatter de desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md y borrar desk/drawer/tasks/task-revisar-dag-workspace-con-agentes-baratos.md (copia sin frontmatter de una tarea ya cerrada en a8601fee). No cambia el contenido de ninguna tarea diferida ni el manual.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest tests/test_taskdoc_read_without_overlay.py

## Done When

_Name the observable condition that makes the task complete._

El ritual dice que la tarea se escribe con add task --from-drawer, el board lista las tareas diferidas existentes y test_taskdoc_read_without_overlay pasa.
