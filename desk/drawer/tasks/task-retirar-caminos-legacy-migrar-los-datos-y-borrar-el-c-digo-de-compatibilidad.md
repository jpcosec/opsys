---
id: task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad
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

# Retirar caminos legacy: migrar los datos y borrar el código de compatibilidad

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261110-181552-suggestion-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261110-181552-suggestion-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Por DK3 (deskops-como-config: cada superficie se cambia y su código viejo se borra en el mismo paso), los caminos de compatibilidad que siguen vivos se retiran migrando a sus consumidores, no se arrastran. Inventario del 2026-11-10, un nodo por fila; cada nodo migra y borra en el mismo paso y se ejecuta en robocop2 (DK5), validando con los tests de los archivos tocados:

1. task_type viejo: deskops/workspace.py LEGACY_TASK_TYPE_KEYS y migrate_task_types (comando en cli/commands/desk.py:407). Consumidores: TraderBot (21 tareas) y sldb (1). Migrar con el comando de deskops desk en esos desks y luego borrar la migración, el mapa y sus tests (test_task_types.py legacy, test_task_lifecycle_validator.py legacy).
2. Snapshot en la ruta vieja: deskops/graph/snapshot.py LEGACY_SNAPSHOT_PATH (.sldb/runtime/knowledge_graph.kg.json) y el fallback en :68. Consumidor: TraderBot. Rehacer su snapshot en la ruta vigente y borrar el fallback y su test en test_graph_snapshot.py.
3. Detector de related_atoms: deskops/atom_references.py LEGACY_FIELD_VIOLATION y graph/checks.py:202. Ningún desk lo usa (deskops, sldb, spec2viz, scion, pron, kimun, TraderBot: 0). Borrar el detector y test_atom_reference_convention.py legacy.
4. Alias deskops inbox (deprecado a favor de deskops message). Ya migrado ~/.claude/CLAUDE.md. Falta: skill global ~/.claude/skills/deskops-workflow (SKILL.md:51, references/deskops-cli.md:42-43, references/vocabulary.md:40), .pi/skills/deskops-inbox-coordination/SKILL.md:34, docs/operator-manual.md:332-336, docs/faq.md:52,230. Luego borrar el alias del CLI, sus goldens de help y los tests de alias en test_message_cli.py y test_message_delivery.py.
5. Alias scaffold_desk y ensure_lifecycle_graph (commit b11a5282, agregados el 2026-11-10 contra DK3). Consumidor: UIs/graph_ui (tests/test_mindmap_deskops.py, test_desk_ui_routes.py, test_mindmap_workspace_explorer.py, e2e_mindmap_deskops.py). Renombrar a seed_desk / write_lifecycle_graph en graph_ui y borrar los alias.

Fuera de alcance: closeout retire de tareas pre-lifecycle (cierre oficial vigente) y la edición de tareas viejas del drawer (test_desk_replace).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
