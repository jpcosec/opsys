---
id: task-test-gitignore-policy-qued-viejo-sldb-core-se-versiona-entero
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

# test_gitignore_policy quedó viejo: .sldb/core se versiona entero

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261106-180230-suggestion-test-gitignore-policy-qued-viejo-sldb-core-se-versiona-entero.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261106-180230-suggestion-test-gitignore-policy-qued-viejo-sldb-core-se-versiona-entero.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado en la suite completa de deskops (f0a4a476, repetido con sldb 88f19ac8): tests/test_gitignore_policy.py::test_sldb_store_declaration_is_tracked_and_derived_state_is_ignored falla porque espera que .sldb/core/store_index.yaml esté ignorado. La regla del dueño vigente es que .sldb/core y .sldb/store.yaml se versionan enteros (migración de layout a .sldb versionado y .sldb_cache ignorada); el test es el que quedó viejo. Arreglo: ajustar el test a la política (.sldb/core y .sldb/store.yaml trackeados; .sldb_cache y .sldb/runtime ignorados), sin tocar .gitignore para volver atrás la política. Aceptación: test_gitignore_policy verde con la política actual. Decisión del overlord, 2026-11-06.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
