---
id: task-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references
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

# closeout verify ignora el campo atoms de la tarea y solo lee references

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261029-013659-unclear-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261029-013659-unclear-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

closeout verify falla con missing_atom_or_materialization_link ('No atom reference ... found') aunque la tarea tenga atoms: [atom-..., atom-...] en su frontmatter (campo tipado a AtomDoc). La compuerta solo lee referencias con prefijo atom- dentro de references, no el campo atoms. Reproducción (2026-10-29, task-integrar-fix-closeout-ignora-archivos-ignorados-en-main): deskops edit task T atoms '["atom-x"]' -> verify falla; deskops edit task T references '[..., "atom-x"]' -> verify pasa. Esperado: la compuerta cuenta los atoms vinculados en el campo atoms (o el mensaje dice que solo mira references).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
