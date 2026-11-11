---
id: task-inbox-y-drawer-trackeados-en-el-store-del-desk-includes-en-desk-declaration-yaml-y-message-send-promote-trackean-al-escribir-h10-de-cc34
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

# Inbox y drawer trackeados en el store del desk: includes en desk_declaration.yaml y message send / promote trackean al escribir (H10 de CC34)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-inbox-y-drawer-trackeados-en-el-store-del-desk-includes-en-desk-declaration-yaml-y-message-send-prom.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-inbox-y-drawer-trackeados-en-el-store-del-desk-includes-en-desk-declaration-yaml-y-message-send-prom.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por CC34 (worker cc34, 2026-11-11). run_view de sldb solo ve documentos trackeados. Hoy desk/drawer/tasks/*.md no lo trackea ningún desk (0 includes en deskops, sldb, spec2viz, scion, graph_ui ni en desk_declaration.yaml). desk/inbox/*.md no está en desk_declaration.yaml (sí en el store.yaml propio de los 5 repos). Y deskops message send y promote inbox-to-drawer-task escriben sin trackear, así que una nota o un drawer nuevos no salen en una vista hasta un desk update --apply. CC34 dejó drawer e inbox como agregado del CLI que lee del disco (H10), y solo board y task salen de run_view. Hecho cuando: (a) desk_declaration.yaml declara InboxNoteDoc desk/inbox/*.md y el modelo del drawer para desk/drawer/tasks/task-*.md (sin chocar con el glob doble TaskDoc del drawer bcf090a8 ni con sldb 6f9576a7), escritos por desk update --apply de forma idempotente; (b) message send y promote inbox-to-drawer-task trackean lo que escriben, en la misma transacción; (c) las vistas drawer e inbox de CC34 pasan a salir de run_view y se borra el agregado H10, con los goldens idénticos.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
