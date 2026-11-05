---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-05T00:22:36'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Falta un comando para disponer revisiones en frío (recibo y disposición)

_Describe the incoming message with enough evidence to triage._

Hoy las revisiones en frío se lanzan con el driver gobernado de cada plan (context_review.py) y la disposición del operador (accepted / corrected / rejected, más un renglón por hallazgo) no tiene comando: en la sesión del 2026-11-04 se escribió a mano en receipt.json y disposition.md, contra la regla de no editar a mano lo que corresponde a un CLI. Lo resuelve GC03 del plan gates-por-tipo (deskops review dispose con ReviewDoc). Mientras tanto, las disposiciones se registran como correcciones del TaskDoc con deskops edit task y no se escriben recibos a mano.
