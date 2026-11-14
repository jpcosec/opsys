---
sldb:
  by: agent
  at: '2026-11-14T10:48:06Z'
  authority: generated
  via: create_document
id: task-test-domain-tree-vuelve-a-verde-sldb-rechaza-al-trackear-un-átomo-con-namespace-no-declarado
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# test_domain_tree vuelve a verde: sldb rechaza al trackear un átomo con namespace no declarado

## Rationale

_Explain why this task exists or the business driver behind it._

Desde sldb b51e9667 la regla rules/builtin:tag_namespace:undeclared bloquea el track. desk update --apply devuelve 1 y los 2 tests de tests/test_domain_tree.py que esperaban 0 fallan en main fd28aba3.

## Goal

_Describe the concrete result this task must produce._

tests/test_domain_tree.py pasa entero contra sldb main. desk update --apply ante un documento que sldb rechaza por regla devuelve 1, nombra el documento y el código de la regla, y no escribe nada. atoms validate --all sigue informando el namespace desconocido.

## Scope

_State what is in scope and what is out of scope._

En alcance: tests/test_domain_tree.py (test_an_atom_with_an_undeclared_namespace_is_an_sldb_finding y test_validate_all_reports_atoms_hanging_from_unwritten_paths), el mensaje de error de desk update --apply si no nombra documento y regla, CHANGELOG. Fuera: cambiar sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del coordinador (revisable): manda el rechazo de sldb al escribir. 1) Reproducir los 2 fallos en main. 2) Ajustar las aserciones: rc 1 y un mensaje con la ruta del documento y el código rules/builtin:tag_namespace:undeclared; el store queda sin cambios. 3) Para el segundo test, misma causa o causa propia: si es otra, informarla. 4) Correr tests/test_domain_tree.py y los archivos de tests que toque, de a uno.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q tests/test_domain_tree.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_domain_tree.py en verde contra sldb main, sin tocar sldb.
