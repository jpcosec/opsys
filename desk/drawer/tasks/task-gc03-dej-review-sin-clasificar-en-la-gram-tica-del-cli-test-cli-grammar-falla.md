---
id: task-gc03-dej-review-sin-clasificar-en-la-gram-tica-del-cli-test-cli-grammar-falla
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

# GC03 dejó review sin clasificar en la gramática del CLI (test_cli_grammar falla)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261106-173650-suggestion-gc03-dej-review-sin-clasificar-en-la-gram-tica-del-cli-test-cli-grammar-falla.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261106-173650-suggestion-gc03-dej-review-sin-clasificar-en-la-gram-tica-del-cli-test-cli-grammar-falla.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Regresión de GC03 (squash 9df4c82a, closeout 52d37665), hallada en la suite completa de deskops sobre f0a4a476: tests/test_cli_grammar.py::test_top_level_nouns_are_classified_exactly_once falla con 'Extra items in the right set: review'. El sustantivo de primer nivel review está en command_registry() pero no en la clasificación de la gramática del CLI (ver task-classify-cli-grammar, f9081d80). Arreglo: clasificar review en la gramática como los demás sustantivos y actualizar la doc de gramática si la hay. Aceptación: test_cli_grammar en verde, goldens de ayuda sin cambios no explicados. gates-por-tipo está congelado, así que va como seguimiento suelto. Detectado por el coordinador de proyecto SLDB_1, 2026-11-06.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
