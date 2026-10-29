---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-22T17:55:39'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Cierre de task con un commit como evidencia

_Describe the incoming message with enough evidence to triage._

En Chatbot_Infra el dueño (JP, 2026-10-22) fijó que la evidencia de cierre de una task es al menos un commit, y que los atoms son principios arquitectónicos (specs/ADR), no evidencia. Hoy 'closeout commit' exige además tests y atom o materialización (missing_tests_evidence, missing_atom_or_materialization_link), así que las tasks de trabajo ya mergeado no pueden cerrar por el ciclo. Para cerrarlas se usó 'deskops edit task <id> status resolved' + 'closeout retire --ref <merge>', que no es su uso previsto (es para tasks de antes del ciclo de vida). Propuesta: que la condición de cierre se pueda configurar por desk (p. ej. solo commit), o un 'closeout commit --ref <sha>' que acepte un commit ya mergeado como única evidencia.
