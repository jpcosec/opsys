FILE:desk/tasks/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de.md
---
sldb:
  by: agent
  at: '2026-11-12T02:25:33Z'
  authority: generated
  via: create_document
id: task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de
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
- deskops/identity.py
- deskops/cli/commands/operations.py
- deskops/cli/commands/doctor.py
- deskops/doctor_findings.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-c-digo-vive-en-otro-repo.md
---

# add task y el doctor sugieren task.external (o una tarea espejo) cuando los files o las referencias de una tarea apuntan a otro repo

## Rationale

_Explain why this task exists or the business driver behind it._

Opción a de la nota de AntonIA a79fe2d6. Una task.code del desk de Governance cuyo código vive en Chatbot_Infra no puede cerrar: nada la avisa al crearla. La opción b (referencias calificadas por repo en resolved-by) deja cerrar el caso; esta evita llegar ahí, sugiriendo el tipo correcto desde el principio.

## Goal

_Describe the concrete result this task must produce._

Al crear una tarea cuyos files apuntan a otro repo, add task lo avisa con una línea (no bloquea) que nombra el repo y sugiere task.external o una tarea espejo en el desk de ese repo; y el doctor lista como alerta, sin cambiar su código de salida, las tareas existentes con esa forma que no son task.external.

## Scope

_State what is in scope and what is out of scope._

En alcance: la detección de un file que apunta a otro repo, el aviso de add task, la alerta del doctor, tests, docs y CHANGELOG. Fuera: closeout (ya resuelto con referencias calificadas), cambiar el tipo de una tarea sola, y cualquier cambio en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox a79fe2d6 (AntonIA, 2026-11-11), opción a. Precondición: las referencias calificadas por repo de resolved-by (tarea xrepo) están en deskops main; esta tarea reutiliza su lectura del registro del ecosistema.

QUÉ SIGNIFICA APUNTAR A OTRO REPO (a1): una entrada de files es de otro repo si (i) tiene la forma identidad-de-repo, dos puntos y ruta, con una identidad que está en el registro del desk (desk/registry, deskops repo register), (ii) es una ruta absoluta que cae bajo la raíz registrada de otro repo, o (iii) empieza por la carpeta padre y resuelve bajo la raíz registrada de otro repo. Lo que no encaja en ninguna se trata como local, como hoy. El worker confirma en el informe, con ejemplos reales de los desks, que (i)-(iii) cubren el caso de AntonIA.
AVISO EN add task (a2): una línea tras crear la tarea, a stdout, por ejemplo: la tarea declara files del repo <identidad>; si el trabajo vive allí considera task.external o una tarea espejo en su desk. No bloquea, no cambia el tipo y no se imprime para task.external ni cuando todos los files son locales.
ALERTA DEL DOCTOR (a3): cada tarea abierta, que no es task.external y tiene files de otro repo, sale como alerta con la tarea y el repo. No cambia el código de salida de doctor ni de desk update.
TESTS (a4): con dos repos registrados en tmp_path, el aviso sale para (i), (ii) y (iii), no sale para files locales ni para task.external, y la alerta del doctor aparece sin cambiar el código de salida. Goldens: la ayuda y la salida de un caso sin files de otro repo no cambian; si un golden cambia, el worker muestra el diff antes de actualizarlo.
DOCS (a5): operator-manual y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y, antes de entregar, la suite completa de a un archivo desde /dev/shm. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: el aviso de add task sale para files de otro repo en las tres formas (i)-(iii), y no sale para files locales ni para task.external
- Test nuevo: el doctor lista la alerta de la tarea con files de otro repo sin cambiar su código de salida
- Los goldens de ayuda y de salida sin files de otro repo no cambian
- suite completa de deskops de a un archivo desde /dev/shm
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

a1-a5 hechos, tests verdes y suite completa en verde; docs y CHANGELOG actualizados; el ítem de drawer de origen se da de baja por CLI.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

