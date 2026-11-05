---
id: task-el-grafo-del-closeout-se-lee-del-índice-de-sldb-no-reescaneando-el-repo
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
- deskops/graph/extract_docs.py
- deskops/graph/extract_edges.py
- deskops/graph/extract_sources.py
- deskops/lifecycle.py
- deskops/operations.py
- deskops/services/desk_view.py
- tests/
- tests/test_desk_view.py
- tests/test_closeout_gates.py
- docs/
- CHANGELOG.md
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-deskops-should-read-through-sldb-compositions
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# El grafo del closeout se lee del índice de sldb, no reescaneando el repo

## Rationale

_Explain why this task exists or the business driver behind it._

El Board de la UI de deskops tarda 25 s en frío y 5 s caliente sobre el desk real (antes ~100 s): verify_task_closeout reconstruye el grafo del repo con extract_source_file_nodes y extract_declared_edges (miles de relative_to y yaml.load) en cada lectura, en vez de consultar lo que sldb ya indexó.

## Goal

_Describe the concrete result this task must produce._

Que build_closeout_graph_context y transitions_from consulten el índice compuesto de sldb (su API Python o sldb serve) y que deskops view board responda en menos de 1 s caliente sobre el desk real.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closeout_gates.py (build_closeout_graph_context), deskops/graph/extract_*.py, deskops/lifecycle.py (transitions_from), deskops/operations.py (read_snapshot de wt/board-perf 9ced34e5 como base). Evaluar sldb serve como proceso caliente para graph_ui frontends/desk/serve.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

Rama base wt/board-perf (9ced34e5: DeskopsOperations.read_snapshot ya comparte el grafo del closeout y las transiciones entre las tarjetas de una lectura). (1) Medición de partida, con un script reproducible guardado en runs/subagents/: frío = primera llamada de deskops view board (o de DeskopsOperations.read_snapshot) en un proceso Python nuevo sobre el desk real de deskops (/home/robocop/proyectos/SLDB_1/deskops, solo lectura); caliente = la misma llamada repetida en el mismo proceso, como hace graph_ui frontends/desk/serve.py. Tres corridas de cada una, se informa la mediana. (2) build_closeout_graph_context deja de reescanear el repo con extract_doc_nodes, extract_source_file_nodes y extract_declared_edges: los nodos de documentos y las aristas declaradas salen del índice compuesto que sldb ya mantiene (sldb.api: open_store, load_edge_index, edges, edges_from, edges_to, documents, records, store_fingerprint). Lo que el índice de sldb no tenga (p. ej. nodos de archivos fuente o aristas de materialización no indexadas) se registra como hipótesis en el informe con el dato exacto que falta; ese resto puede seguir extrayéndose pero solo para los archivos que el closeout necesita, no el repo entero. (3) transitions_from consulta las aristas una sola vez por huella de store (store_fingerprint): un proceso caliente no recarga el índice si la huella no cambió; nada de caché que sobreviva a un cambio del store. (4) Equivalencia: un test sobre desks temporales compara el camino viejo (las funciones de extracción actuales, conservadas como oráculo de test) con el nuevo y exige el mismo resultado de verify_task_closeout y de transitions_from en casos con materializaciones válidas, inválidas y sin materialización. (5) Medición final con el mismo script; meta: caliente < 1 s, frío < 5 s. Si no se alcanza, se informa el perfil (cProfile, top 15) y qué parte falta en sldb. (6) Evaluar sldb serve como proceso caliente para graph_ui frontends/desk/serve.py: solo una nota en el informe (latencias y API que haría falta); no se toca graph_ui. Reglas: no tocar el repo sldb (si falta algo, hipótesis y nota que manda el coordinador con deskops message send --to sldb); nada escrito a mano en desk/ ni .sldb/; el desk real solo se lee; ninguna bandera que salte un gate; CHANGELOG; suite completa sin fallas nuevas respecto de main (fallas previas conocidas: test_board_portable_references::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions, test_gitignore_policy::test_sldb_store_declaration..., y test_skill_cli_drift::test_use_deskops_copies... si falta .pi/skills/use-deskops).

## Validation

_List the checks required before this task can close._

- pytest -q tests/test_desk_view.py tests/test_closeout_gates.py
- test de equivalencia camino viejo/nuevo sobre desks temporales
- script de medición en runs/subagents/: deskops view board caliente < 1 s y frío < 5 s sobre el desk real
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Medición sobre el desk real de deskops con el proceso caliente: deskops view board < 1 s y en frío < 5 s; la compuerta de closeout da los mismos resultados que hoy (test que compara ambos caminos sobre desks temporales); suite completa en robocop2 sin fallas nuevas.
