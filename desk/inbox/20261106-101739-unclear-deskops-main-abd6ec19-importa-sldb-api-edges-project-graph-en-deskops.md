---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T10:17:39'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-06T10:20:17'
---

# deskops main (abd6ec19) importa sldb.api.edges.project_graph en deskops/

_Describe the incoming message with enough evidence to triage._

deskops main (abd6ec19) importa sldb.api.edges.project_graph en deskops/graph/checks.py y desk_graph.py (desde 7a6e2ff8), pero ese módulo no existe en ninguna rama de sldb (main 8d7bee13). Efecto: 'deskops closeout commit' de una tarea task.code falla en el verify con 'No module named sldb.api.edges.project_graph' y no hace el commit. Visto el 2026-11-06 en labchile_chatbots (robocop2), cerrando task-pr-49/56/57. Las tareas task.external sí cierran.
