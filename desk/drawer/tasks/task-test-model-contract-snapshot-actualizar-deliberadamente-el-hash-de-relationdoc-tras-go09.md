---
id: task-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09
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

# test_model_contract_snapshot: actualizar deliberadamente el hash de RelationDoc tras GO09

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261106-180227-suggestion-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261106-180227-suggestion-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado en la suite completa de deskops (f0a4a476, repetido con sldb 88f19ac8): tests/test_model_contract_snapshot.py falla con 'Model contract changed for: RelationDoc. This requires a store migration (task-rw-f6-migrate-tracking-stores)'. Causa: GO09 de sldb (transiciones como datos de la arista; código 33b3c7a0, closeout d39bf915) cambió el contrato de RelationDoc (validador de attributes sets/terminal). Arreglo: registrar el cambio como deliberado; actualizar tests/fixtures/model_contract_hashes.json solo junto con la migración de stores que el test pide (task-rw-f6-migrate-tracking-stores o su equivalente vigente), citando GO09 en el TaskDoc y en el CHANGELOG. Aceptación: test_model_contract_snapshot verde y los desks que trackean RelationDoc migrados (deskops doctor sin alerts de contrato de RelationDoc). Decisión del overlord, 2026-11-06.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
