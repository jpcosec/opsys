---
id: task-quitar-o-migrar-el-glob-taskdoc-desk-tasks-task-md-de-store-yaml-cuando-sldb-d-la-v-a
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Quitar o migrar el glob TaskDoc desk/tasks/task-*.md de store.yaml cuando sldb dé la vía

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-quitar-o-migrar-el-glob-taskdoc-desk-tasks-task-md-de-store-yaml-cuando-sldb-dé-la-vía.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-quitar-o-migrar-el-glob-taskdoc-desk-tasks-task-md-de-store-yaml-cuando-sldb-dé-la-vía.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

El .sldb/store.yaml de deskops declara TaskDoc con glob desk/tasks/task-*.md (desde 376fdcce) además de los paths de TaskCodeDoc y TaskDebugDoc. Con sldb@main, stores build trackea los 5 tasks actuales dos veces (bajo el hijo y bajo TaskDoc) y los selectores por nombre quedan ambiguos; build --check da rc 0. Los 5 tasks ya están tipados con su modelo hijo, así que el glob no aporta nada.

No se puede corregir hoy: stores declare --write conserva el glob autorado, no hay CLI para quitarlo y editar .sldb a mano está prohibido. Depende de la nota del inbox de sldb 6f9576a7 (tracking doble padre/hijo y vía de CLI para quitar una entrada include).

Hecho cuando: con la vía de sldb, el glob TaskDoc se quita o se migra (por CLI, deskops desk update o sldb), stores build trackea cada task una sola vez, los selectores por nombre resuelven sin ambigüedad y los 4 pasos del workflow pasan en un clon limpio.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
