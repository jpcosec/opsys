FILE:desk/tasks/task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo.md
---
sldb:
  by: agent
  at: '2026-11-12T02:25:28Z'
  authority: generated
  via: create_document
id: task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo
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
- deskops/services/closure.py
- deskops/cli/commands/desk.py
- deskops/doctor_findings.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inv-lidas-en-el-mismo-modelo-ninguna-v-a-por-cli-escribe-sldb-h2.md
---

# deskops quita las guardas que esquivaban H1-H3 de sldb: cerrar por CLI dos tareas inválidas del mismo modelo y reparar un desk que tiene un documento inválido

## Rationale

_Explain why this task exists or the business driver behind it._

Parte 2 del ítem de drawer 75e33dab. Mientras sldb abortaba stores check ante el primer documento inválido (H1) y cada escritura re-extraía el modelo entero y caía en otro inválido (H2, con rollback incompleto, H3), deskops puso tres guardas: retire, supersede y resolved-by se niegan si hay otra tarea inválida en el modelo, con un mensaje que nombra sldb H2; y desk update --apply, si stores check no entrega un informe, se salta todas las reparaciones menos la migración. Cuando la tarea de sldb que corrige H1-H3 esté en sldb main, esas guardas dejan al dueño de un desk heredado (AntonIA, el gateway) sin salida por CLI para cerrar dos tareas inválidas.

## Goal

_Describe the concrete result this task must produce._

Con sldb corregido, deskops cierra por CLI dos o más tareas inválidas del mismo modelo (retire, supersede, resolved-by), y desk update --apply sobre un desk con documentos inválidos hace todas las reparaciones sin saltarse ninguna, mientras la migración de estados heredados y el listado de las tareas inválidas se quedan.

## Scope

_State what is in scope and what is out of scope._

En alcance: las guardas de closure.py (retire, supersede y resolved-by) y la rama de desk.py que se salta las reparaciones cuando stores check no entrega informe, los tests que fijaban esas guardas, docs y CHANGELOG. Fuera: la tabla de migración de estados heredados y su escritura por frontmatter (se quedan), el listado de tareas inválidas del doctor, y cualquier cambio en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: ítem de drawer 75e33dab (parte 2) y nota de sldb 3895e9f7. Precondición: la tarea de sldb que corrige H1-H3 (stores check no aborta ante un documento inválido, con el hallazgo store/doc-invalid) está en sldb main; esta tarea corre contra ese sldb.

ESTADO ACTUAL: en closure.py, close_superseded, close_retired y close_resolved_by llaman a _other_invalid_tasks y, si hay otra tarea inválida, devuelven _blocked_by_invalid_tasks, cuyo texto nombra sldb H2. En desk.py, si stores check no entrega un JSON y hay tareas inválidas o heredadas pendientes, se fija store_check_error, se imprime Store check failed y, con --apply, se imprime Skipped the other repairs y se sale con 1 sin reparar estructura, grafo de ciclo de vida, modelos, tracking, tipos ni índices.

REPRODUCCIÓN: el coordinador la arma con caché frío (sin caché de sldb ni XDG cache), como un clon limpio del gateway: dos tareas inválidas (draft con history task_activates y task_hands_to_closeout) en el mismo modelo. Hoy: supersede de una sale rc 1 con el mensaje de H2.

CAMBIO (g1-g5):
g1: se borran las llamadas a _other_invalid_tasks y a _blocked_by_invalid_tasks en retire, supersede y resolved-by, y las dos funciones si quedan sin uso. La escritura por frontmatter de una tarea que el modelo rechaza se queda (el modelo sigue sin poder leerla).
g2: en desk.py, con stores check entregando un informe aunque haya documentos inválidos, la rama store_check_error ya no se alcanza para ese caso: se quita el salto de reparaciones y desk update --apply sigue con todas. Si stores check falla de verdad (sin informe y sin documentos inválidos que lo expliquen) se conserva el error de hoy.
g3: el informe de desk update y el doctor listan los documentos inválidos por el hallazgo store/doc-invalid de sldb además del listado por frontmatter que ya existe, sin duplicarlos.
g4: tests, siempre con caché frío además del caliente: (a) retire, supersede y resolved-by cierran cada uno una de dos tareas inválidas del mismo modelo, y luego la otra, y sldb stores check termina con el hallazgo por la que queda; (b) desk update --apply sobre un desk con un documento inválido completa todas las reparaciones; (c) los tests que fijaban el rechazo con el texto de H2 se reescriben como (a), no se borran. Los demás tests de closeout y de estados heredados siguen verdes.
g5: docs (operator-manual, sección de estados heredados) y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y, antes de entregar, la suite completa de a un archivo desde /dev/shm contra un clon de sldb origin/main que ya tenga la corrección (variable de entorno SLDB_SRC si la tarea de SLDB_SRC ya entró, o la ruta hermana en la copia). Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo, con caché frío: retire, supersede y resolved-by cierran cada uno una de dos tareas inválidas del mismo modelo, y luego la otra
- Test nuevo: desk update --apply sobre un desk con un documento inválido completa todas las reparaciones
- Los tests de estados heredados y de closeout siguen verdes, con los de rechazo por H2 reescritos
- suite completa de deskops de a un archivo desde /dev/shm contra el sldb corregido
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

g1-g5 hechos, tests verdes con caché frío y caliente y suite completa en verde; docs y CHANGELOG actualizados; el ítem de drawer 75e33dab se da de baja por CLI.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

