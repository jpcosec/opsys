---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-12T13:22:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Board no refleja edit task goal

_Describe the incoming message with enough evidence to triage._

En ftcourier, 'deskops edit task <id> goal ...' actualiza la tarea pero desk/tasks/Board.md sigue mostrando el goal viejo en la línea de la tarea. No hay verbo para refrescarlo: 'deskops edit board <Board|board-001|desk/tasks/Board.md> ...' responde 'No artifact.board file found', y 'deskops desk replace desk/tasks/Board.md' lo rechaza porque es un documento modelado de tareas. Caso: FTC-26, 12-11-2026.
