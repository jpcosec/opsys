---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-29T01:36:59'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout verify ignora el campo atoms de la tarea y solo lee references

_Describe the incoming message with enough evidence to triage._

closeout verify falla con missing_atom_or_materialization_link ('No atom reference ... found') aunque la tarea tenga atoms: [atom-..., atom-...] en su frontmatter (campo tipado a AtomDoc). La compuerta solo lee referencias con prefijo atom- dentro de references, no el campo atoms. Reproducción (2026-10-29, task-integrar-fix-closeout-ignora-archivos-ignorados-en-main): deskops edit task T atoms '["atom-x"]' -> verify falla; deskops edit task T references '[..., "atom-x"]' -> verify pasa. Esperado: la compuerta cuenta los atoms vinculados en el campo atoms (o el mensaje dice que solo mira references).
