---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-09T13:34:09'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout commit sin --paths dice Nothing staged aunque el CLI dejó cambios

_Describe the incoming message with enough evidence to triage._

Reportado por el coordinador de AntonIA (vía overlord SLDB_1, 2026-11-09). deskops closeout commit sin --paths responde 'Nothing staged' aunque haya cambios producidos por el propio CLI (TaskDoc, Board, .sldb). Hoy la vía que funciona es pasar --paths con el TaskDoc y desk/tasks/Board.md. Esperado: que closeout commit agregue lo que el cierre produjo (TaskDoc, Board, .sldb/core, .sldb/store.yaml) sin depender de que el operador lo stagee, o que el error diga qué rutas faltan y sugiera --paths.
