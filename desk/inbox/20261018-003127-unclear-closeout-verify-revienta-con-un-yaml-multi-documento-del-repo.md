---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T00:31:27'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T01:54:24'
---

# closeout verify revienta con un YAML multi-documento del repo

_Describe the incoming message with enough evidence to triage._

Desde graph_ui (2026-10-18). 'deskops closeout verify --root . --task task-graph-ui-instalable-pyproject-con-dependencias-reales-y-sin-hacks-de-sys-path' en /home/jp/proyectos/SLDB_1/UIs/graph_ui termina con 'Unexpected: expected a single document in the stream ... name: uml-clases ... but found another document'. El archivo es docs/representacion/propuesta-vocabulario-visual.assets/uml-clases.vocabulario.yaml, un YAML legítimo con varios documentos separados por '---' (no es un documento de desk). Como el verify aborta, la task no puede obtener closeout_evidence_verified y queda en ritual-closeout. Esperado: que el verify ignore los YAML fuera de desk/, o los lea con safe_load_all, en vez de abortar la verificación entera.
