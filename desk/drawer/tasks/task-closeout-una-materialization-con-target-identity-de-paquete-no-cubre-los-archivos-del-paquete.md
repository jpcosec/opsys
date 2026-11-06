---
id: task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete
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

# closeout: una materialization con target_identity de paquete no cubre los archivos del paquete

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261106-163026-suggestion-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261106-163026-suggestion-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Al cerrar SV01-SV04 en sldb (2026-11-06), el gate atom|materialization de closeout verify exigio un enlace por archivo declarado en files. Los src/sldb/*.py no son nodos del grafo del desk (FILE_RULES solo hace source_file a desk/ y deskops/), asi que la unica cobertura real es una materialization por archivo con target_identity exacto: probe una con target_identity src/sldb/notations (paquete) y no cubrio ninguno de sus archivos. Resultado: 62 materializations para 66 archivos de cuatro tareas. Sugerencia para CC33 (closeout como regla): que un target_identity que nombre un directorio cubra los archivos bajo el, o que una materialization acepte una lista de targets; y que el mensaje del gate diga que el enlace es por archivo exacto. Registrado a pedido del supervisor deskops-sobre-sldb-config.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
