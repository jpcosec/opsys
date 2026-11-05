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
files: []
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



## Validation

_List the checks required before this task can close._

- pytest -q tests/test_desk_view.py tests/test_closeout_gates.py

## Done When

_Name the observable condition that makes the task complete._

Medición sobre el desk real de deskops con el proceso caliente: deskops view board < 1 s y en frío < 5 s; la compuerta de closeout da los mismos resultados que hoy (test que compara ambos caminos sobre desks temporales); suite completa en robocop2 sin fallas nuevas.
