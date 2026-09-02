---
id: task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea
current_node: checklist-task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea-execution-ready
history: []
references:
- desk/drawer/tasks/task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea-execution-ready
- checklist-task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea-testing-ready
- checklist-task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# inbox cross-repo inusable fuera del ecosystem root y repo register crashea

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20260901-000600-unclear-inbox-cross-repo-inusable-fuera-del-ecosystem-root.md`.

## Scope

_State what is in scope and what is out of scope._

Dos bloqueos encadenados al intentar `deskops inbox "<nota>" --repo deskops` desde gemini_test (worktree en /home/jp/proyectos/_worktrees/vitali, fuera del ecosystem root):

1. El registry se resuelve contra `ecosystem_root/desk/registry` derivado del store local, asi que un repo que vive fuera del arbol del ecosistema no encuentra a `deskops` ("Repository id 'deskops' not found in registry"), y el registry del ecosistema (/home/jp/proyectos/hum-ecosystem/desk/registry/) tampoco tiene entry para el propio deskops.
2. Workaround intentado: `deskops repo register` local con path absoluto para deskops (funciona) y luego registrar el repo actual para pasar el check de identidad (`resolve_canonical_project_identity` exige el repo actual en el mismo registry). Ese segundo register crashea: `Unexpected: 'RegisteredRepository' object has no attribute 'models_index'`.

Esperado: poder enviar notas a repos hermanos desde cualquier checkout/worktree, o al menos un mensaje que indique el camino soportado. Esta nota y su hermana se entregaron escribiendo el archivo a mano en desk/inbox/ con el formato de las notas precedentes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
