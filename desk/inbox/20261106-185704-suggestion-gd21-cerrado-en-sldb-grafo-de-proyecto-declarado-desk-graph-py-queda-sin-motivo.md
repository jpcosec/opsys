---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T18:57:04'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD21 cerrado en sldb: grafo de proyecto declarado; desk_graph.py queda sin motivo

_Describe the incoming message with enough evidence to triage._

GD21 cerrado en sldb (squash a2a0174f, closeout 27457ff7). Nuevo: sldb.api.project_graph(store) → ProjectGraph con la configuración declarada en .sldb/store.yaml bajo project_graph (ProjectGraphConfig.from_mapping/to_mapping, dato puro); ProjectGraph.edges_to(id); DocumentSurface.closed (predicado del lenguaje, p. ej. status = "closed"); CLI sldb graph project nodes [--kind K] | edges --from ID | --to ID | missing con envelope; GET /project-graph/nodes?kind=, /project-graph/edges?from=|to=, /project-graph/missing (mismo JSON que la CLI) y GET /edges?...&include_linked=false. Doc: docs/architecture/project-graph.md. Queda sin motivo en deskops: deskops/graph/desk_graph.py (desk_graph_config/desk_graph/extract_*: la configuración pasa a store.yaml y _closed_issue a closed: en la superficie issue), el mapa inverso de materializations de CloseoutGraph (usar edges_to) y el rescaneo del repo por petición en frontends/desk/serve.py (usar el memo o las rutas /project-graph/*). Transición: ProjectGraphConfig(closed_document=...) sigue aceptado con DeprecationWarning hasta que CC33 migre; después se borra. Pendiente de deskops: correr el oráculo de equivalencia v1 contra la configuración declarada (CC33).
