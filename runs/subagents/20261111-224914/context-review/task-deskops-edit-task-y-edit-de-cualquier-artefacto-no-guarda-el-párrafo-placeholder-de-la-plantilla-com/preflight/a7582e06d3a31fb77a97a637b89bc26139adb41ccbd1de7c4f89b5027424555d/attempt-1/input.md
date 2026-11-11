FILE:desk/tasks/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com.md
---
sldb:
  by: agent
  at: '2026-11-11T22:48:42Z'
  authority: generated
  via: create_document
id: task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com
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
- deskops/operations.py
- deskops/doc_access.py
- deskops/workspace.py
- deskops/cli/commands/promote.py
- deskops/cli/commands/operations.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-deskops-edit-task-duplica-el-placeholder-outline-the-expected-implementation-route-or-affected-surface-en-implementation-path.md
---

# deskops edit task (y edit de cualquier artefacto) no guarda el párrafo placeholder de la plantilla como contenido: una edición con el texto de la sección no lo duplica

## Rationale

_Explain why this task exists or the business driver behind it._

Visto en el TaskDoc de CC33c: las ediciones b9-b18 de la corrida scion (4305c7d9) dejaron tres copias del placeholder de Implementation Path. Reproducido sobre main 9035ca60: si el valor que recibe edit trae el párrafo placeholder (por ejemplo, el texto crudo de la sección más lo nuevo), se guarda como contenido y el render vuelve a anteponer el placeholder como ancla, así que cada edición suma uno.

## Goal

_Describe the concrete result this task must produce._

Una edición por CLI de un campo de sección deja exactamente un placeholder de plantilla (el ancla) en el archivo, venga o no el placeholder dentro del valor. La edición es idempotente: el mismo valor dos veces deja el mismo archivo.

## Scope

_State what is in scope and what is out of scope._

En alcance: el camino de deskops edit <subject> (DeskopsOperations.edit_artifact_field y lo que normaliza el valor antes de escribir), para todos los modelos del desk con párrafos placeholder en su plantilla, más tests, docs y CHANGELOG. Fuera: el render y extract de sldb (si la causa resultara ser de sldb, va como hipótesis en el informe y no se escribe en sldb); limpiar TaskDocs ya cerrados (CC33c se cerró con un solo placeholder, 120bb672).

## Implementation Path

_Outline the expected implementation route or affected surface._

Drawer de origen 8d9c8f8c.

REPRODUCCIÓN (coordinador, deskops main 9035ca60, copia en /dev/shm con el fixture lifecycle_desk; runs/subagents/20261111-repro-placeholder/repro.log y test_repro_edit_task_placeholder.py). Se cuentan los placeholders del archivo al crear la tarea y después de cada edit task de implementation_path. (1) Valor limpio: [1, 1, 1], estable. (2) Valor extraído con extract_model_data y reescrito: [1, 1, 1], estable. (3) Valor igual al texto crudo de la sección (con su placeholder) más texto nuevo: [1, 2, 3], crece de a uno. Es lo que pasó en 4305c7d9 (de 1 a 3).

CAUSA (a confirmar): extract ya descarta el párrafo placeholder (cff4f30a, y sldb 9dcabd9a para el anclaje), pero la escritura no: edit_artifact_field guarda el valor tal cual, y el render de la plantilla antepone el placeholder como ancla. Un valor que ya lo trae queda con dos.

ARREGLO (r1-r4):
r1: antes de escribir un campo de sección, deskops quita del valor los párrafos que son exactamente un placeholder de la plantilla de ese campo (el mismo criterio con que extract los descarta), en un solo lugar que usen todos los subjects de edit. Un valor que es solo placeholder deja el campo vacío.
r2: si existe ya un normalizador de placeholders en deskops (promote.py _TASK_SECTION_PLACEHOLDERS, workspace.py), se reutiliza o se unifica; no se duplica la lista de placeholders.
r3: tests: el caso (3) de la reproducción pasa a [1, 1, 1]; el mismo valor dos veces deja el archivo idéntico; un valor que es solo placeholder deja el campo vacío; un texto que contiene la frase del placeholder dentro de un párrafo más largo no se toca. Al menos un subject además de task (por ejemplo atom o inbox-note) si su plantilla tiene placeholders.
r4: docs (operator-manual, sección de edit) y CHANGELOG.

VALIDACIÓN: el worker corre los tests que toca de a uno, y antes de entregar la suite completa de a un archivo desde /dev/shm con wait-pytest. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: editar con el texto crudo de la sección más texto nuevo deja un solo placeholder (caso 3 de la reproducción)
- Test nuevo: el mismo valor dos veces deja el archivo idéntico
- Test nuevo: un valor que es solo placeholder deja el campo vacío; una frase igual al placeholder dentro de un párrafo más largo no se toca
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r4 hechos, con la causa raíz escrita en el informe antes del arreglo, los tests verdes y la suite completa en verde; docs y CHANGELOG actualizados.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

