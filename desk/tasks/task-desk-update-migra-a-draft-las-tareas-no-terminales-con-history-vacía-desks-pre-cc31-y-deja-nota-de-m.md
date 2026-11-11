---
sldb:
  by: agent
  at: '2026-11-11T05:54:20Z'
  authority: generated
  via: create_document
id: task-desk-update-migra-a-draft-las-tareas-no-terminales-con-history-vacía-desks-pre-cc31-y-deja-nota-de-m
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
files:
- deskops/models/task_lifecycle.py
- deskops/workspace.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inv-lidas-en-el-mismo-modelo-ninguna-v-a-por-cli-escribe-sldb-h2.md
---

# desk update migra a draft las tareas no terminales con history vacía (desks pre-CC31) y deja nota de migración

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión del overlord (2026-11-11), prioridad. Es lo último que bloquea el desk de Governance. Una tarea active o ready_for_testing con history vacía no tiene respaldo, y hoy desk update la reporta como no migrable y no repara nada más.

## Goal

_Describe the concrete result this task must produce._

deskops desk update --apply migra a draft, en el nodo de entrada, las tareas no terminales con history vacía, con una nota de migración en summary, y sigue con el resto de las reparaciones.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/models/task_lifecycle.py, deskops/workspace.py, tests/, docs/, CHANGELOG.md. Fuera: history no vacía incoherente, el validador y los status terminales.

## Implementation Path

_Outline the expected implementation route or affected surface._

DECISIÓN DEL OVERLORD (2026-11-11, revisable): las tareas no terminales sin history, como active o ready_for_testing con history vacía, las migra desk update a draft. Nada respalda ese estado avanzado: no hay transición registrada ni recibos. Desbloquea el desk de Governance (task-rol-de-robocop-en-antonia-dev-y-mepu-dev-sin-llaves); la reproducción va en un desk de prueba, nunca en Governance.

REPRODUCCIÓN (coordinador, desk desechable en /dev/shm; log runs/subagents/20261111-repro-nonterm/repro.log): dos tareas task.code en ritual-execution con status active y ready_for_testing y history []. desk update (dry-run y --apply) las reporta como 'Invalid task documents (not written)' con la sugerencia fija de decidir su estado, rc 1, y salta el resto de las reparaciones porque sldb no lee el store.

CAUSA: deskops/models/task_lifecycle.py legacy_state_migration (CC37 + task.debug de estados heredados) solo decide superseded y los status resueltos o de drawer. Un status no terminal con history vacía cae en 'return None' (no migrable).

ARREGLO (n1-n5):
n1 (tabla): con history vacía y un status no terminal que no es entrada (cualquiera que no esté en ENTRY_STATUSES, OUTSIDE_LIFECYCLE_STATUSES ni sea superseded; por ejemplo active, ready_for_testing, blocked o in_progress), la migración da status draft y current_node = el entry_node del ciclo de vida (lifecycle_table().entry_node) si current_node no está vacío y no es ya ese nodo. El resultado se comprueba con lifecycle_errors, como el resto de la tabla.
n2 (nota de migración en la tarea): la migración antepone al campo summary una línea fija: "Migrada a draft por deskops desk update: estado heredado '<status>' sin history (<fecha ISO>)." Si summary ya tenía texto, se conserva después. Se escribe por la misma vía de frontmatter que el resto de la migración.
n3 (línea de reporte): como las demás de b4 del task.debug de estados heredados, "<archivo>: status <antes> -> draft", más "current_node <antes> -> <entry>" si cambia.
n4 (fuera): history no vacía con status incoherente sigue siendo no migrable (el dueño decide); los status terminales siguen con su tabla; no se relaja el validador.
n5 (tests): sobre tmp_path, las dos formas de la reproducción (active y ready_for_testing) más una en otro nodo (ritual-testing con history vacía), con --apply. Se comprueba: status draft, current_node entry, la nota en summary, rc 0, segunda corrida sin cambios y sldb stores check que pasa. Goldens de salida de desk update solo si cambia una línea existente; si no, golden nuevo para la línea de n3.

REGLAS COMUNES: tests de a uno con TMPDIR=/dev/shm y la guarda de pgrep anclada (sin esperar a pytest con cwd fuera de proyectos/SLDB_1); nada a mano en desk/ ni .sldb/; nunca git add -A; CHANGELOG (Fixed) y doc en docs/operator-manual.md (desk update); informe runs/subagents/nonterm-worker-report.md con causa raíz; 4 pasos del workflow de deskops en clon limpio, los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test sobre tmp_path con active, ready_for_testing y un tercer nodo con history vacía: draft, nodo de entrada, nota en summary, rc 0 y segunda corrida sin cambios
- sldb stores check pasa después de --apply
- Goldens de ayuda idénticos; salida, solo la línea nueva
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

n1-n5 hechos con causa raíz escrita y tests verdes; doc y CHANGELOG.
