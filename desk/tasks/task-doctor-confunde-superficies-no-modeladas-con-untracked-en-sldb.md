---
id: task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb
current_node: checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-execution-ready
history: []
references:
- desk/drawer/tasks/task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-execution-ready
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-testing-ready
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Doctor confunde superficies no modeladas con untracked en sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20260811-011208-suggestion-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb.md`.

## Scope

_State what is in scope and what is out of scope._

En el repo sldb, tras corregir data_mutation y sincronizar los docs modelados, deskops status --root . sigue reportando como 'Untracked desk documents' superficies que no deberían forzarse a estar trackeadas por SLDB: desk/drawer/features/*.md, desk/issues/*.md y desk/METHODOLOGY.md. En la práctica, el doctor está mezclando 'docs no modelados' con 'estado roto'. Sería mejor excluir esas superficies no modeladas del chequeo de untracked, o distinguirlas explícitamente de los documentos que sí deben estar registrados en .sldb. Evidencia: en tools/sldb ya no quedan data_mutation; sólo esos paths siguen apareciendo en Doctor Findings.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
