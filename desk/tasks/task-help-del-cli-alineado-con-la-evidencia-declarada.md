---
id: task-help-del-cli-alineado-con-la-evidencia-declarada
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# Help del CLI alineado con la evidencia declarada

## Rationale

_Explain why this task exists or the business driver behind it._

La auditoria del 2026-11-03 muestra que el Typical flow de deskops --help, los ejemplos de deskops add y el help de --task-type fallan al ejecutarse tras el cambio de evidencia declarada (59244c94).

## Goal

_Describe the concrete result this task must produce._

Que todo ejemplo impreso por --help y about corra tal cual en un desk recien inicializado, y que el help de closeout y advance describa el gate de evidencia declarada.

## Scope

_State what is in scope and what is out of scope._

deskops/cli/registry.py (epilogo Typical flow, ejemplos de add generados desde los campos requeridos del modelo, lista de --task-type, help de closeout verify/commit y advance --to, ejemplos de inbox hacia message), deskops/about.py, y un test que ejecute el Typical flow. Sin cambios de comportamiento del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

Corregir textos en registry.py y about.py; generar el ejemplo de add <tipo> a partir del modelo; agregar tests/test_cli_help_examples.py que corra el Typical flow en un repo temporal.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli_help_examples.py -q
- pytest tests -q -x

## Done When

_Name the observable condition that makes the task complete._

pytest tests/test_cli_help_examples.py pasa y la suite existente sigue verde; deskops --help, add --help y add <tipo> --help no muestran comandos que fallen.
