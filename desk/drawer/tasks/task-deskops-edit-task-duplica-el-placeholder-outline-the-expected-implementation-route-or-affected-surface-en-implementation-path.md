---
id: task-deskops-edit-task-duplica-el-placeholder-outline-the-expected-implementation-route-or-affected-surface-en-implementation-path
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

# deskops edit task duplica el placeholder '_Outline the expected implementation route or affected surface._' en Implementation Path

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-deskops-edit-task-duplica-el-placeholder-outline-the-expected-implementation-route-or-affected-surfa.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-deskops-edit-task-duplica-el-placeholder-outline-the-expected-implementation-route-or-affected-surfa.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Visto el 2026-11-10 en el TaskDoc de CC33c (main 4305c7d9). Tras varias llamadas a deskops edit task (precisiones b9-b18 de la corrida scion), la sección Implementation Path tiene tres copias del placeholder '_Outline the expected implementation route or affected surface._' antes del texto real: una venía de antes y dos se agregaron, una por edición. Causa probable: al reescribir el campo, el render vuelve a anteponer el placeholder de la plantilla cuando el campo ya tiene contenido, o extract no lo reconoce como placeholder y lo conserva como contenido. Reproducir: deskops add task de prueba y deskops edit task <id> implementation_path dos veces; luego contar el placeholder. Arreglo esperado: el placeholder solo aparece si el campo está vacío, y una edición deja el texto idempotente. Limpiar el TaskDoc de CC33c con deskops edit task cuando esté el arreglo.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
