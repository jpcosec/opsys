---
id: task-integrar-fix-closeout-ignora-archivos-ignorados-en-main
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
- 594a892
- 5acb05b
- tests/test_closeout_atomless.py
- tests/test_board_portable_references.py
- tests/test_materialization_targets_outside_package.py
- atom-declared-materialization-targets-are-graph-nodes
- atom-closing-commits-are-tool-made-and-run-linked
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-declared-materialization-targets-are-graph-nodes
- atom-closing-commits-are-tool-made-and-run-linked
---

# Integrar fix/closeout-ignora-archivos-ignorados en main

## Rationale

_Explain why this task exists or the business driver behind it._

La rama llevaba 14 commits adelante de main con los arreglos pedidos por MEPU (closeout en desks sin átomos, Board portable, materializaciones fuera del paquete). Una rama abierta no le sirve a nadie: main debe avanzar con los features ya hechos.

## Goal

_Describe the concrete result this task must produce._

main contiene el squash de la rama, la suite completa pasa, la rama y su worktree ya no existen.

## Scope

_State what is in scope and what is out of scope._

Squash-merge a main, cherry-pick de la evidencia de verificación MEPU (9ca479d), borrado de fix/closeout-ignora-archivos-ignorados y fix/mepu-board-and-closeout y del worktree .tmp/mepu-final-verification. No cambia código.

## Implementation Path

_Outline the expected implementation route or affected surface._

git merge --squash; pytest; commit 594a892; cherry-pick -x 9ca479d (5acb05b); worktree remove; branch -D.

## Validation

_List the checks required before this task can close._

- python -m pytest -q
- git branch --list 'fix/*' devuelve vacío

## Done When

_Name the observable condition that makes the task complete._

git log main muestra 594a892 y 5acb05b, no quedan ramas fix/, la suite pasa.
