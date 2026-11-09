---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-09T15:23:42'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout resolved-by: cerrar una tarea cuyo trabajo ya entró por PR

_Describe the incoming message with enough evidence to triage._

Reportado por AntonIA (nota ea273c3 en el inbox del gateway), vía overlord SLDB_1, 2026-11-09. Una tarea cuyo trabajo ya se mergeó por PR antes del closeout no se puede cerrar con honestidad: closeout commit pide un átomo por cada archivo del commit, supersede es para un tema sin trabajo hecho, y retire exige que la tarea ya esté resuelta. Propuesta: deskops closeout resolved-by --task <id> --ref <PR o commit> --reason <texto>, que exija evidencia de commit (ancestro de HEAD) y de tests, pero no un átomo por archivo. Encolado detrás de la cadena actual de deskops-como-config; es chico.
