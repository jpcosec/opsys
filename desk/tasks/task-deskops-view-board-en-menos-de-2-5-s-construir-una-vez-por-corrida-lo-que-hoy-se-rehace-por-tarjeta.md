---
sldb:
  by: agent
  at: '2026-11-12T03:37:46Z'
  authority: generated
  via: create_document
id: task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta
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
- deskops/cli/commands/view.py
- deskops/services/tasks.py
- deskops/services/closeout_gates.py
- deskops/lifecycle.py
- deskops/graph/desk_graph.py
- deskops/operations.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops view board en menos de 2,5 s: construir una vez por corrida lo que hoy se rehace por tarjeta (transiciones, closeout, grafo del desk) y abrir el store menos veces

## Rationale

_Explain why this task exists or the business driver behind it._

Resto de la meta de CC52. Con la tarea H11 de sldb integrada, sldb views run board baja a 1,6 s, pero deskops view board sigue en 4,9 s (mediana de 3, store construido, proceso nuevo): el trabajo propio de deskops es unos 3,3 s. Lo midió el worker de H11: show_task de cada tarjeta (las transiciones con transition_findings, el closeout con build_closeout_graph_context y desk_graph, que arma un ProjectGraph de unos 2 s) se repite por tarjeta, y 31 open_store hacen cada uno migrate_store_layout y _already_canonical (unos 1,3 s bajo perfil, 16 000 Path.resolve).

## Goal

_Describe the concrete result this task must produce._

deskops view board, con el store construido y en un proceso nuevo, tarda 2,5 s o menos (mediana de 3, layout del benchmark de H11) y su salida es idéntica a la de hoy; lo que se construye una vez por corrida se comparte entre las tarjetas.

## Scope

_State what is in scope and what is out of scope._

En alcance: view board de deskops (la construcción de las tarjetas en deskops/cli/commands/view.py y lo que llaman show_task, el closeout de solo lectura y las transiciones), compartir entre tarjetas el grafo del desk, el contexto de closeout y el snapshot de lectura, reducir las llamadas de deskops que abren el store, tests, docs y CHANGELOG. Fuera: sldb (memoizar open_store o migrate_store_layout es una hipótesis para sldb, no se escribe aquí), cambiar lo que muestra el board o el contrato de la vista, y deskops view task salvo que comparta el mismo código.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: informe del worker de H11 (hipótesis para deskops) y decisión del coordinador de proyecto. Precondición: la tarea H11 de sldb está integrada en sldb main; esta tarea corre contra ese sldb. Si no lo está, el worker para y avisa.

REPRODUCCIÓN: la del worker de H11 sobre su layout (deskops 4904ddfe, sldb con H11, spec2viz b16c021, scion 4ead6d0bf; runs/subagents/20261112-repro-boardperf/repro.log), con caché frío y caliente: deskops view board caliente 4,94 s, y 1,59 s de sldb views run board en el mismo layout. Primera corrida tras el build, 11,3 s (compone y guarda la caché de composición).

ESTADO ACTUAL (de las lecturas del código; el worker lo confirma con un perfil): la tarjeta de cada tarea llama a show_task, que pasa por _lifecycle_gates y transition_findings, y al closeout de solo lectura; el closeout arma build_closeout_graph_context (que usa desk_graph) y desk_graph construye un ProjectGraph propio. Nada de eso se comparte entre tarjetas más allá del snapshot de lectura que ya existe.

CAMBIO (p1-p5), el worker mide cada paso antes y después:
p1: línea base propia y perfil con cProfile de deskops view board en el layout, commiteados, que cuentan las llamadas a open_store, a desk_graph y a build_closeout_graph_context por corrida.
p2: el grafo del desk y el contexto de closeout se construyen una vez por corrida de view board y se pasan a las tarjetas, por el snapshot de lectura que ya existe o por un parámetro explícito; sin estado global que sobreviva a la corrida.
p3: las llamadas de deskops que abren el store por tarjeta se reducen a las necesarias, con el mismo manejo de errores; el costo propio de open_store en sldb queda como hipótesis para sldb en el informe.
p4: la salida de view board y de view task es byte a byte la de antes sobre el mismo desk (un test la compara contra una corrida con el camino viejo, o con los goldens existentes si cubren el caso). Si un golden cambia, el worker para y muestra el diff antes de actualizarlo.
p5: docs y CHANGELOG. Si la meta de 2,5 s no se alcanza, el informe dice cuánto falta y qué lo explica, con la medición, y qué parte es de sldb.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de deskops de a un archivo desde /dev/shm, ci-knowledge-check y graph missing. Los 4 pasos del CI de deskops los corre el coordinador. Las mediciones van con caché frío y caliente.

## Validation

_List the checks required before this task can close._

- Benchmark: deskops view board, store construido, proceso nuevo, mediana de 3, 2,5 s o menos en el layout de H11; medidas antes y después en el informe
- Test: la salida de view board y de view task es idéntica a la de antes sobre el mismo desk
- Perfil antes y después que cuenta las llamadas a open_store, desk_graph y build_closeout_graph_context por corrida
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

p1-p5 hechos con las mediciones, salida idéntica, tests y suite completa en verde, y la meta de 2,5 s alcanzada o explicada con la medición; docs y CHANGELOG actualizados.
