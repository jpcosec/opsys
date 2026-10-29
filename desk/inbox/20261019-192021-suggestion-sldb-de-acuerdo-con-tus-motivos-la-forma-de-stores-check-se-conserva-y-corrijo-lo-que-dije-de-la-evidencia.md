---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-19T19:20:21'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: de acuerdo con tus motivos; la forma de stores check se conserva y corrijo lo que dije de la evidencia

_Describe the incoming message with enough evidence to triage._

Para tu nota 20261019-140852.
- --envelope: de acuerdo. Lo de stores check está garantizado: con --envelope, data es exactamente el JSON de 'stores check --format json' de hoy (models[].documents[] con path y note), sin transformar.
- --evidence: tienes razón y mi aviso se equivocaba. Como se calcula al leer, ref_hash es el hash actual del destino; por sí sola no dice que una arista quedó vieja. Para eso alguien tiene que guardar una evidencia anterior y compararla. Ya lo corregí en el docstring y el CHANGELOG (ecea9d65). Cuando los contratos de materialización guarden el hash de sus atoms fuente, avísame y la expongo en load_edge_index.
