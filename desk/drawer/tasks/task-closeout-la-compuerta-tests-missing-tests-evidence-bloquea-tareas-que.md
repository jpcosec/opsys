---
id: task-closeout-la-compuerta-tests-missing-tests-evidence-bloquea-tareas-que
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

# closeout: la compuerta tests (missing_tests_evidence) bloquea tareas que

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261027-200234-unclear-closeout-la-compuerta-tests-missing-tests-evidence-bloquea-tareas-que.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261027-200234-unclear-closeout-la-compuerta-tests-missing-tests-evidence-bloquea-tareas-que.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

closeout: la compuerta tests (missing_tests_evidence) bloquea tareas que solo cambian specs o docs. Caso: MEPU SPEC-2 (task-spec-2-spec-de-ingesta-..., PR #101, 1130d14b) cambió solo specs/etl/ingesta.yml, su render y el catálogo; no hay test que lo cubra y citar uno ajeno sería falso. Se cerró con 'deskops advance task --to closed' (override) el 2026-10-27; la compuerta de átomo sí pasó con átomos reales. Pedido: que closeout commit/verify acepten una tarea sin tests cuando los archivos cambiados son solo specs/docs/rendered (o un --no-tests --reason explícito que quede en el trailer, como Closeout-Mode: manual), en vez de obligar a forzar la transición, que no deja commit de cierre ni índice.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
