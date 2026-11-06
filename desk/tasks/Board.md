---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-gc06-cierre-de-las-vías-de-escape-advance-to-y-edit-task-sobre-campos-del-ciclo-de-vida.md
- desk/tasks/task-gc03-comando-deskops-review-que-reemplaza-a-los-dos-scripts-de-revisión-en-frío.md
- desk/tasks/task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados.md
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

- GC06: Cierre de las vías de escape: advance --to y edit task sobre campos del ciclo de vida [draft] - Se retira la opción --to de deskops advance (registry y tasks.py:179-192); cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede; blocked → nada que escribir (DC4: blocked es la regla que no se cumple; mientras GC05 no exista, el mensaje de bloqueo de advance ya lo dice). edit task rechaza status, current_node, task_type, closeout_evidence e history con un error que dice quién escribe cada campo (advance y closeout; add task para task_type) y con exit 1 (error de dominio); el resto de campos sigue editable. El inbox 20261029-213633 (advance --to superseded no cambia status) se cierra con ack porque la opción desaparece. Sin dependencia de sldb: con task_activates aún sin condición (hasta GC05) retirar --to no bloquea a nadie.
- GC03: Comando deskops review que reemplaza a los dos scripts de revisión en frío [draft] - Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado, vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md, brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc), bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos ligados + archivos que files nombra, menores de 60 KB + validación), status [<task> | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/ (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo, perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json) y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256. Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md con los flags de aislamiento (--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del script gobernado como texto del perfil; el perfil Scion queda como opción futura detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato de la tarea, y una repetición exige --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py es de sldb y no se toca: se le manda nota por deskops message send --to sldb de que deskops review lo cubre. Produce G_RECEIPTS.
- CC30: Limpieza previa - operations.py como fachada y fuera los spec YAML duplicados [draft] - deskops/operations.py queda como fachada que solo delega; los helpers privados que piden los servicios viven en deskops/doc_access.py o en su servicio dueño; ningún servicio construye DeskopsOperations; _normalize_task_payload y compile_task_spec son una sola función; task_lifecycle.yaml se carga solo por lifecycle.load_lifecycle_spec; spec/artifacts y spec/fields (y SpecRegistry, specs/mermaid.py si solo lo usan tests) borrados, con id_pattern, status_default y tags por artefacto como atributo de clase de cada modelo. Sin cambio de comportamiento: goldens de ayuda y salida idénticos.
