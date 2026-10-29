---
id: task-requisitos-d4-d6-de-governance-pr-en-taskdoc-alertas-en-el-inbox-y-rundoc
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

# Requisitos D4–D6 de Governance: PR en TaskDoc, alertas en el inbox y RunDoc

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261020-104307-suggestion-requisitos-d4-d6-de-governance-pr-en-taskdoc-alertas-en-el-inbox-y-rundoc.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261020-104307-suggestion-requisitos-d4-d6-de-governance-pr-en-taskdoc-alertas-en-el-inbox-y-rundoc.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde Governance (sesión governance-00), 2026-10-20. El spec docs/spec/spec-procesos-modelables.md (draft) de heyantonia/Governance modela los hechos del proceso (PRs, corridas de CI, alertas, incidentes, pedidos, recursos) como documentos derivados y pide a deskops:
D4: que TaskDoc declare el PR o la rama que la realiza, como referencia a un PullRequestDoc (modelo de Governance), para que el grafo una tarea → PR → corridas.
D5: que InboxNoteDoc.kind admita 'alert' (hoy solo unclear y suggestion), o una forma de enrutar al inbox una alerta con un AlertDoc como fuente.
D6: que algo escriba RunDoc al lanzar un subagente; hoy está registrado pero run.py:7-16 dice que nada lo produce.
D7 ya llegó como nota aparte (closeout verify y la cobertura de archivos fuera del paquete indexado).
Ninguno bloquea hoy; son para la entrega que implementa los modelos.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
