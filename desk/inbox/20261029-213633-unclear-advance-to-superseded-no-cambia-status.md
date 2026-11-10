---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-29T21:36:33'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# advance --to superseded no cambia status

_Describe the incoming message with enough evidence to triage._

En shared_llm-gateway, 'deskops advance task <id> --to superseded' movió current_node a 'superseded' y dejó status en draft. Para retirar una tarea obsoleta hubo que usar 'deskops edit task <id> status superseded'. Falta un verbo CLI para marcar una tarea superseded. Ademas 'deskops message send --to deskops' falla desde repos cuyo registry no conoce a deskops.
