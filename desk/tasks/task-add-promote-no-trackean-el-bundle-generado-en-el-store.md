---
id: task-add-promote-no-trackean-el-bundle-generado-en-el-store
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-add-promote-no-trackean-el-bundle-generado-en-el-store
current_node: checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-execution-ready
history: []
references:
- desk/drawer/tasks/task-add-promote-no-trackean-el-bundle-generado-en-el-store.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-execution-ready
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-testing-ready
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# add/promote no trackean el bundle generado en el store

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20260901-000500-unclear-add-promote-no-trackean-el-bundle-generado.md`.

## Scope

_State what is in scope and what is out of scope._

`deskops add task` y `deskops promote drawer-task-to-active-task` generan el bundle completo (task, routine, checklists, conditions, edges, operators) pero no lo trackean en el store sldb. Evidencia: en gemini_test (worktree vitali, 2026-08-31/09-01) una pasada de promotes dejo 22 docs untracked y un `add task` dejo 19; `deskops doctor` los reporta como "Untracked desk documents" y hay que correr `sldb docs track <path> --model <Model>` a mano por cada archivo. Repro: `deskops add task --root . --title X` en un desk con store `.sldb`, luego `deskops doctor --root .`. Esperado: el bundle queda trackeado al crearse, igual que hace `repo register` con su entry.

Nota entregada a mano en este inbox porque el camino CLI (`deskops inbox --repo deskops`) no fue posible desde gemini_test; ver la nota hermana sobre el registry.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-add-promote-no-trackean-el-bundle-generado-en-el-store.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
