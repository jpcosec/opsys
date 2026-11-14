---
sldb:
  by: agent
  at: '2026-11-14T11:35:18Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper.md
- desk/tasks/task-test-domain-tree-vuelve-a-verde-sldb-rechaza-al-trackear-un-átomo-con-namespace-no-declarado.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- context-review
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- Los tests de deskops leen la ruta del sldb hermano de la variable de entorno SLDB_SRC, con un helper común [draft] - Un solo helper común resuelve la ruta de sldb para los tests: lee la variable de entorno SLDB_SRC y, si no está definida, usa la ruta hermana de hoy; los 18 archivos lo usan y ninguno repite la línea fija.
- test_domain_tree vuelve a verde: sldb rechaza al trackear un átomo con namespace no declarado [draft] - tests/test_domain_tree.py pasa entero contra sldb main. desk update --apply ante un documento que sldb rechaza por regla devuelve 1, nombra el documento y el código de la regla, y no escribe nada. atoms validate --all sigue informando el namespace desconocido.
