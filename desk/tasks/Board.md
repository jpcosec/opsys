---
sldb:
  by: agent
  at: '2026-11-09T18:35:48Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados.md
- desk/tasks/task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests.md
- desk/tasks/task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb.md
- desk/tasks/task-cc32-gates-de-activación-de-cada-tipo-de-tarea-como-ruledoc-produce-g-consumer.md
- desk/tasks/task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents.md
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
- CC36: Plantillas del desk (board, rituales, drawer, faq) como datos escritos por el scaffold de sldb [draft] - Las plantillas del desk (config.json, Board, pills, rituales phase/execution/testing/closeout, drawer/README.md, atoms/tag-namespaces.yaml y el perfil runtime-pi-deepseek-flash) pasan a archivos de deskops/data/templates/ y a una declaración deskops/data/desk_declaration.yaml (folders y seeds if_missing) que deskops pasa a sldb.api.scaffold_store. desk update usa includes declarados en lugar de adivinar modelos por ruta. Se borran scaffold_desk, _write_if_missing, los *_template y guess_model_for_path. El resultado de init y de desk update es idéntico al golden capturado antes del cambio.
- CC32: Gates de activación de cada tipo de tarea como RuleDoc (produce G_CONSUMER) [draft] - El gate de activación de cada tipo de tarea de fábrica (task.code, task.docs, task.debug, task.refactor, task.decision, task.aggregate, task.external) es una RuleDoc semilla managed, on_transition sobre ritual-execution, que sldb evalúa al avanzar: exige los recibos de revisión que el tipo pide (accepted e intactos) y las dependencias cerradas. Los atributos __activation_receipts__ se borran. deskops advance, next y show muestran los findings de edges_blocked (cláusula, nodo, valor visto). El test de integración G_CONSUMER pasa en sus tres pasos.
- CC35b: Selectores - resolución de documentos por sldb.api.select_documents [draft] - La resolución de selectores de documentos trackeados de deskops pasa a sldb.api.select_documents (GD23), con la misma regla (nombre exacto antes que prefijo único) y los mismos mensajes de error, que deskops arma con los candidatos que sldb devuelve. desk_paths.resolve_selector y _tracked_task_paths (que lee .sldb crudo) desaparecen de las superficies trackeadas. Los alias privados que graph_ui importa se conservan, marcados CC34.
