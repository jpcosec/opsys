---
sldb:
  by: agent
  at: '2026-11-09T20:36:30Z'
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
- desk/tasks/task-closeout-resolved-by-cerrar-una-tarea-cuyo-trabajo-ya-entró-por-pr.md
- desk/tasks/task-cc37-cerrar-vías-de-escape-ninguna-escritura-deja-el-ciclo-de-vida-fuera-de-las-reglas.md
- desk/tasks/task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador.md
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
- closeout resolved-by: cerrar una tarea cuyo trabajo ya entró por PR [draft] - deskops closeout resolved-by --task <id> --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] --reason <texto> cierra una tarea cuyo trabajo ya está en la historia. Exige al menos un --ref que sea commit ancestro de HEAD y al menos un --test que el gate de tests acepte, pero no exige un átomo por archivo. Hace un solo commit de cierre con Closeout-Mode: resolved-by, como supersede.
- CC37: Cerrar vías de escape - ninguna escritura deja el ciclo de vida fuera de las reglas [draft] - Ninguna vía de escritura deja una TaskDoc con un ciclo de vida inconsistente: un validador del modelo TaskDoc (DK6, mecanismo de CC38) exige que status, current_node, history y task_type sean coherentes con el grafo del ciclo de vida, y sldb lo aplica en toda escritura (fields update, docs update, /save, transacción). Las escrituras internas de deskops que cambian el ciclo de vida pasan solo por advance y closeout. El inventario de vías de escritura queda en el TaskDoc.
- CC33a: Recibos de evidencia - closeout verify escribe ReviewDoc kind evidence y queda como orquestador [draft] - deskops closeout verify corre los productores de hechos de git y archivos y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence (fact, value, verdict accepted o rejected, subject anclado al contrato de la tarea), sin duplicar recibos en una verificación repetida sin cambios. verify_task_closeout queda como orquestador y devuelve el mismo envelope que hoy. El gate de cierre todavía no cambia: lo cambia CC33b.
