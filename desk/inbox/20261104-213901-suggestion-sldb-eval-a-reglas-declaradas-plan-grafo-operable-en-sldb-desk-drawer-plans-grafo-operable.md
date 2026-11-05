---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-04T21:39:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb evalúa reglas declaradas: plan grafo-operable en sldb/desk/drawer/plans/grafo-operable

_Describe the incoming message with enough evidence to triage._

Ruta del plan en sldb: desk/drawer/plans/grafo-operable/ (dag.yaml rev 9, reviewed_pending_promotion; GO01 cerrado).

D1 | sldb se modifica a fondo para evaluar reglas sobre documentos, aristas y hashes ("operativicemos esto lo más posible en sldb; si hay que modificarlo a fondo, démosle"). La pill pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops se reescribe: evaluador genérico en sldb, reglas autoradas fuera. | Dueño | Chat de la sesión de deskops, 2026-11-04; pill editada con deskops edit pill | 2026-11-04

Para deskops queda el plan consumidor (gate G_CONSUMER): tipos de tarea como documentos con jerarquía, ReviewDoc como recibo, gate de activación como RuleDoc, cierre de advance --to y edit task status, y convertir el driver de revisiones en frío en un comando deskops review.
