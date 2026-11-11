---
sldb:
  by: agent
  at: '2026-11-11T23:36:02Z'
  authority: generated
  via: create_document
id: task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas
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
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/identity.py
- deskops/cli/commands/closeout.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-c-digo-vive-en-otro-repo.md
---

# closeout resolved-by acepta referencias calificadas por repo (<repo>:<sha>, <repo>:<ruta de test>) verificadas contra un repo registrado, para cerrar una task.code cuyo código vive en otro repo

## Rationale

_Explain why this task exists or the business driver behind it._

Caso de AntonIA (inbox a79fe2d6): una task.code del desk de Governance cuyo código entró en Chatbot_Infra no puede cerrar, porque resolved-by exige un commit ancestro del repo del desk y un test .py de ese repo. La vía actual (tarea espejo en el repo del código, supersede en el desk coordinador) duplica tareas y pierde la traza.

## Goal

_Describe the concrete result this task must produce._

deskops closeout resolved-by cierra una tarea con --ref <repo>:<sha> y --test <repo>:<ruta>, donde <repo> es un repo del registro del ecosistema (deskops repo register), verificando en ese repo que el commit es ancestro de su HEAD y que el test existe y es un archivo de tests; con el mismo commit de cierre y los mismos trailers, que guardan la referencia calificada tal cual.

## Scope

_State what is in scope and what is out of scope._

En alcance: el parseo y la verificación de referencias calificadas en las compuertas de resolved-by (deskops/services/closeout_gates.py, deskops/services/closure.py), la resolución del repo por el registro (deskops/identity.py), la ayuda del CLI, tests, docs y CHANGELOG. Fuera: closeout verify y closeout commit (siguen exigiendo evidencia local); la sugerencia de task.external en add task o desk update (opción a de la nota, queda en el drawer); supersede (ya acepta una ruta o un commit local).

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox a79fe2d6 (AntonIA, 2026-11-11), opción b. Decisión del coordinador (revisable): se hace la opción b acotada a resolved-by; la opción a (sugerir task.external) queda en el drawer.

ESTADO ACTUAL: ClosureService.close_resolved_by exige al menos un --ref que sea un commit HEAD o ancestro del repo del desk (CloseoutGates.reference_points_to_commit, git rev-parse y merge-base con cwd en la raíz del desk) y al menos un --test que sea un .py existente bajo un directorio tests del repo del desk (reference_points_to_test). El registro de repos del ecosistema está en deskops/identity.py (load_repository_registry, RegisteredRepository con su raíz resuelta).

CAMBIO (c1-c5):
c1: una referencia calificada tiene la forma <repo-id>:<valor>, donde <repo-id> es la identidad de un repo del registro del ecosistema. Una referencia sin prefijo, o con un prefijo que no es un repo registrado, se trata como hoy. Una URL http(s) sigue siendo URL.
c2: --ref <repo-id>:<sha> cuenta como el commit exigido si, en la raíz registrada de ese repo, el sha resuelve a un commit que es ancestro de su HEAD (las mismas reglas que hoy: hex en minúscula, sin nombres simbólicos). Si la raíz registrada no existe en la máquina, se rechaza con un error que nombra el repo y la ruta.
c3: --test <repo-id>:<ruta> cuenta si la ruta existe en la raíz registrada de ese repo, con las mismas reglas que reference_points_to_test (un .py bajo un directorio tests, sin salir de la raíz). Los files de la tarea no amplían los tests de otro repo.
c4: los trailers del commit de cierre guardan cada referencia tal como se escribió (Closeout-Ref: Chatbot_Infra:87671716), y Closeout-Mode sigue siendo resolved-by.
c5: tests con dos repos git en tmp_path, registrados en el registro del ecosistema: cierra con commit y test del otro repo; rechaza un sha que no es ancestro del HEAD del otro repo, un test inexistente, un repo no registrado (se trata como local y falla como hoy) y una raíz registrada que no existe. Docs (operator-manual, sección de cierre) y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y, antes de entregar, la suite completa de a un archivo desde /dev/shm. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: resolved-by con --ref <repo>:<sha> y --test <repo>:<ruta> de otro repo registrado cierra con Closeout-Mode: resolved-by y guarda las referencias calificadas en los trailers
- Tests nuevos de rechazo: sha no ancestro, test inexistente, repo no registrado, raíz registrada ausente
- Los tests existentes de resolved-by y closeout siguen verdes; suite completa de a un archivo en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

c1-c5 hechos, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados; la opción a de la nota queda como ítem de drawer.
