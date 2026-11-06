---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados.md
- desk/tasks/task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests.md
- desk/tasks/task-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09.md
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
- desk/rituals/context-review.md
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

- CC30: Limpieza previa - operations.py como fachada y fuera los spec YAML duplicados [draft] - deskops/operations.py queda como fachada que solo delega; los helpers privados que piden los servicios viven en deskops/doc_access.py o en su servicio dueño; ningún servicio construye DeskopsOperations; _normalize_task_payload y compile_task_spec son una sola función; task_lifecycle.yaml se carga solo por lifecycle.load_lifecycle_spec; spec/artifacts y spec/fields (y SpecRegistry, specs/mermaid.py si solo lo usan tests) borrados, con id_pattern, status_default y tags por artefacto como atributo de clase de cada modelo. Sin cambio de comportamiento: goldens de ayuda y salida idénticos.
- CC38: Invariantes de documento al modelo - validadores pydantic en lugar de chequeos sueltos y tests [draft] - Cada chequeo de UN documento que hoy vive fuera del modelo (domain_tree, atom_tags, atoms validate, doctor y el inventario que dejó CC30) pasa a un validador pydantic de su modelo en deskops/models/ y el chequeo viejo se borra en el mismo paso; los chequeos entre documentos quedan inventariados y asignados a CC32 o CC33; los tests prueban que el modelo, sldb fields update y sldb docs update rechazan el payload malo. Sin cambio de gramática ni de texto de error: goldens idénticos.
- test_model_contract_snapshot: actualizar deliberadamente el hash de RelationDoc tras GO09 [draft] - tests/fixtures/model_contract_hashes.json registra deliberadamente el contrato nuevo de RelationDoc (a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6) citando GO09, y test_model_contract_snapshot.py pasa; la migración del store de deskops ya está hecha en main (09b5075c: .sldb/core/models/RelationDoc.yaml con ese contract_hash).
