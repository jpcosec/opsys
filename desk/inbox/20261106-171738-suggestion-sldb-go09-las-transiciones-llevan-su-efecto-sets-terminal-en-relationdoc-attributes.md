---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T17:17:38'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb GO09: las transiciones llevan su efecto (sets, terminal) en RelationDoc.attributes

_Describe the incoming message with enough evidence to triage._

sldb 33b3c7a0 (plan grafo-operable, GO09): RelationDoc.attributes admite sets (campo -> valor, con {campo} desde el sujeto) y terminal (bool), validados al escribir; edges_holding devuelve cada arista que se cumple con effects = {sets resueltos, terminal}; apply_effects(subject, effects, model) da el payload nuevo validado, sin persistir. Doc: sldb docs/architecture/edges.md. Con esto deskops puede retirar sets_status/terminal de su YAML de lifecycle (gate G_CONSUMER del plan, lo verifica deskops).
