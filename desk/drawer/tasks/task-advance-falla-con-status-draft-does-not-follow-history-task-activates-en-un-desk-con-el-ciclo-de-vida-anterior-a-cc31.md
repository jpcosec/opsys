---
id: task-advance-falla-con-status-draft-does-not-follow-history-task-activates-en-un-desk-con-el-ciclo-de-vida-anterior-a-cc31
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

# advance falla con 'status draft does not follow history task_activates' en un desk con el ciclo de vida anterior a CC31

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-advance-falla-con-status-draft-does-not-follow-history-task-activates-en-un-desk-con-el-ciclo-de-vid.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-advance-falla-con-status-draft-does-not-follow-history-task-activates-en-un-desk-con-el-ciclo-de-vid.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Reporte de AntonIA (kit Chatbot_Infra, /srv/repos/Chatbot_Infra rama dev; tareas task-ola-2-niveles-de-modelo… en 1e8a5258 y task-ola-2-criterios… en 2623eda4) con deskops-runtime 5ccc29a3: 'deskops advance task' falla dos veces con 'Validation error: TaskCodeDoc … lifecycle is inconsistent: status draft does not follow history task_activates; expected active'. Causa raíz: el desk del kit tiene desk/lifecycle/execution-task_activates.md con 'attributes: {}' (de la migración 2d69e9c6). La semilla managed de deskops desde CC31 trae 'attributes: {sets: {status: active}, terminal: false}'. advance agrega task_activates a history pero no mueve status, y el validador de CC37 rechaza la escritura. Arreglo del kit: 'deskops desk update --apply', que reescribe las semillas managed. Defectos de deskops: (1) doctor dice 'Desk is healthy' con semillas managed del ciclo de vida desactualizadas; (2) el error de advance no nombra la causa (la arista sin efecto sets) ni sugiere desk update --apply. Comprobado en un desk limpio con el runtime 5ccc29a3: init, add task, review record preflight/bundle, review dispose accepted y advance pasa draft→active sin error. El síntoma anchor_state lost que vi antes fue un error de mi reproducción (recibos pending sin disponer), no un bug.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
