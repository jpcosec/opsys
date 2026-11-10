---
sldb:
  by: agent
  at: '2026-11-10T02:37:18Z'
  authority: generated
  via: save_document_payload
id: task-rendimiento-cada-comando-cli-tarda-30-s-desde-cc32-cc35b
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
- deskops/
- tests/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# rendimiento: cada comando CLI tarda ~30 s desde CC32/CC35b

## Rationale

_Explain why this task exists or the business driver behind it._

Desde CC32 (6afc78b0, reglas de activación como RuleDoc) y CC35b (5328b664, selectores por select_documents), cada comando CLI de deskops tarda unos 30 s, también en main (lo reportó cc37-worker el 2026-11-10). test_activation_rules y test_lifecycle_end_to_end, que tardaban 45-75 s por archivo, ya no entran en timeout 900. Afecta a los workers, a la suite completa y al CI. Pedido del coordinador de proyecto: un fallo conocido sin tarea no existe.

## Goal

_Describe the concrete result this task must produce._

Se mide, se escribe la causa raíz y se arregla donde viva. Cada comando de deskops (show task, advance) vuelve a un tiempo del orden de antes de CC32, y test_activation_rules y test_lifecycle_end_to_end vuelven a quedar por debajo de ~90 s por archivo.

## Scope

_State what is in scope and what is out of scope._

En alcance: medir y arreglar la regresión de tiempo por comando CLI de deskops. Si la causa vive en deskops, se arregla aquí. Si vive en sldb (rule_graph, evaluación de reglas on_write/on_transition, select_documents, stores check), el arreglo va en una tarea del desk de sldb, como el de dirty.json, y esta tarea queda con la medición y la nota. Fuera: cambiar la semántica de las reglas de CC32, de los selectores de CC35b o de la transacción de CC35a, y los fallos de CI de main-en-verde (si alguno viene de esto, se coordina con esa tarea sin duplicar).

## Implementation Path

_Outline the expected implementation route or affected surface._

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan):
p1 (medición antes): sobre un desk temporal creado con deskops init en /dev/shm (no el desk real) y con una tarea task.code, medir con time y python -X importtime, y con cProfile (python -m cProfile -o ... -m deskops ...), cada uno de estos: deskops show task <id>, deskops next <id>, deskops advance task <id> (bloqueada y con recibos) y deskops add task. El informe trae, por comando, el tiempo total, el tiempo de import y las 15 funciones con más tiempo acumulado (pstats, sort cumulative). La misma medición se repite con el código de main anterior a CC32 (6afc78b0^) y anterior a CC35b, en copias detached en /dev/shm, para atribuir la regresión al commit.
p2 (causa raíz): escrita con evidencia (función, cuántas veces se llama por comando y qué lee de disco) antes de arreglar. Candidatos sin verificar: sldb rule_graph (~3 s por llamada según el informe de CC32, cacheado solo dentro de un ReadSnapshot), evaluación de reglas en cada escritura, select_documents sin caché, stores check o un rebuild de secciones al registrar RuleDoc en cada operación (ensure_rule_model en write_lifecycle_graph o en desk update).
p3 (dónde se arregla): si la causa está en deskops (por ejemplo, una llamada repetida que se puede hacer una vez por comando, o un registro de modelo que corre en cada comando), se arregla en esta rama. Si está en sldb, el worker para y avisa con la medición: el coordinador del plan abre la tarea en el desk de sldb y la despacha como la de dirty.json. Nada de cachés en deskops que escondan un problema de sldb (regla 7).
p4 (aceptación medible): la tabla «comando | antes de CC32 | main hoy | con el arreglo», y test_activation_rules y test_lifecycle_end_to_end corridos enteros, de a uno, desde /dev/shm, cada uno por debajo de ~90 s. Sin cambiar la semántica: test_activation_rules, test_tracked_selector_resolution, test_transaction, test_cli y test_output_goldens verdes, sin --update-golden.
p5 (coordinación con main-en-verde): si un fallo o timeout del CI que ataca main-en-verde viene de esto, el worker lo dice y los dos coordinan por el coordinador del plan; no se arregla dos veces.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-10):
b1 (umbrales): aceptación dura, cada archivo de test entero en menos de 90 s, medido con time desde /dev/shm sin otros pytest corriendo. Por comando CLI no hay umbral fijo: el objetivo es volver al orden del commit anterior a CC32 (6afc78b0^) con una tolerancia de +50 %. Si no se logra, el informe dice cuánto falta y por qué.
b2 (frontera deskops/sldb): se atribuye según dónde está la función que domina el tiempo acumulado en cProfile. Si está en el paquete sldb (sldb/...), es de sldb. Si deskops llama a una función de sldb más veces de lo necesario (por ejemplo, N veces por comando cuando alcanza una), es de deskops y se arregla aquí. Registrar un modelo en cada comando, aunque sea por medio de sldb, es de deskops si es deskops quien lo invoca sin necesidad.
b3 (regla 7 de alcance.md): «Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb». Aplicada aquí: no se agrega en deskops una caché, un atajo ni una evaluación propia que reemplace o esconda un costo de sldb. Lo que es de sldb se arregla en sldb.
b4 (precedente dirty.json): el worker para y avisa con la medición. El coordinador del plan crea la nota con deskops add inbox-note en un worktree limpio de sldb, la promueve con deskops promote inbox-to-drawer-task, promueve la tarea (add task --from-drawer), le corre el preflight y despacha un worker en una rama wt/ de sldb. El coordinador de proyecto la integra en sldb y avanza sldb-runtime.
b5 («main hoy»): origin/main en el momento de despachar, que el brief nombra. Antes de CC32: 6afc78b0^. Antes de CC35b: el commit anterior al squash de CC35b (5328b664 es su closeout; el squash es el commit de código inmediatamente anterior; el worker lo identifica con git log).
b6 (protocolo): el worker avisa al coordinador del plan con bash ~/setup/herdr/coordination.sh say w1:p1F "...". El coordinador del plan decide y, si hace falta, escala al coordinador de proyecto.

## Validation

_List the checks required before this task can close._

- Tabla de tiempos por comando antes de CC32, en main hoy y con el arreglo (p4)
- test_activation_rules y test_lifecycle_end_to_end enteros, de a uno desde /dev/shm, por debajo de ~90 s
- test_tracked_selector_resolution, test_transaction, test_cli y test_output_goldens verdes, sin --update-golden

## Done When

_Name the observable condition that makes the task complete._

La causa raíz está escrita con medición. El tiempo por comando antes y después está en el informe. test_activation_rules y test_lifecycle_end_to_end corren enteros por debajo de ~90 s por archivo. Los tests de semántica están verdes. Si la causa está en sldb, la tarea de sldb está abierta y despachada.
