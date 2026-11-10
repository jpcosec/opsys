---
id: task-tasks-con-status-terminal-heredado-y-history-vac-a-el-validador-las-rechaza-desks-pre-cc31
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

# Tasks con status terminal heredado y history vacía: el validador las rechaza (desks pre-CC31)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261110-182943-suggestion-tasks-con-status-terminal-heredado-y-history-vac-a-el-validador-las-rechaza-desks-pre-cc31.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261110-182943-suggestion-tasks-con-status-terminal-heredado-y-history-vac-a-el-validador-las-rechaza-desks-pre-cc31.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desks migrados antes de CC31 tienen tasks con status terminal heredado (superseded, cancelled, deferred) y history: [] en current_node ritual-execution. El validador actual las rechaza y quedan sin dueño en el ciclo de vida. Ejemplo: /srv/repos/Chatbot_Infra/desk/tasks/task-pyme-como-satelite.md (status: superseded, current_node: ritual-execution, history: [], summary 'Reemplazada (dueño 2026-10-16)…'). Salida de 'deskops desk update --apply --root .' en el kit: "inconsistent task lifecycle in desk/tasks/task-pyme-como-satelite.md, not written: status: 'superseded' is not an entry status; a task with an empty history at 'ritual-execution' has status 'draft' (status changes only through deskops advance and deskops closeout)". Cuántas hay: kit 6 (superseded), Governance varias (cancelled, y una active con history vacía), labchile 1, shared_llm-gateway 4 (superseded/deferred y 2 draft con history task_hands_to_closeout). En shared_llm-gateway además bloquea el registro de modelos: 'sldb stores check' falla con TaskDoc task-ci-propio-del-gateway (superseded, history vacía), así que doctor sigue con 'Unregistered models: ReviewDoc, Task*Doc'. Falta una vía de migración (por ejemplo, retire o closeout que acepte un estado terminal heredado y sintetice su history) o que desk update lo repare. Reporta: coordinador de AntonIA, 2026-11-10.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
