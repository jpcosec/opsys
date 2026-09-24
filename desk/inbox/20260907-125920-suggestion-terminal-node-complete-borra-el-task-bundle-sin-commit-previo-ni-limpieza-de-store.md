---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Upla
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-09-07T12:59:20'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Terminal node complete borra el task bundle sin commit previo ni limpieza de store

_Describe the incoming message with enough evidence to triage._

Bug de lifecycle: al alcanzar el terminal node 'complete', deskops elimina el bundle de la tarea (desk/tasks/<id>.md, routine, primitives) en el mismo paso, y el closeout commit posterior registra las deletions. Problema: se pierde la evidencia/e histórico del task bundle en desk/ y, si el agente no corre 'sldb stores update' + untrack de los 57 docs derivados inmediatamente, el store queda FAIL (docs 'missing' en documents index). Reproducido en legos/knowledge con 3 tareas (task-implement-knowledge-anchor-add, task-implement-canonical-write-ops-create-assert-ingest, task-auto-refresh-indexes-and-graph-after-writes): hubo que restaurar, detectar, untrackear a mano y regenerar índices/grafo. Comportamiento esperado: al completar, deskops debería (1) modificar/actualizar el estado, (2) guardar con commit atómico la versión final del bundle, y (3) recién entonces borrar el bundle + limpiar el store (untrack de documentos derivados) en el mismo flujo, dejando el store consistente sin intervención manual. Evidencia: commits 8253770/71da4bd/004019b (closeouts con deletions) y la reparación manual posterior en a809e3d.
