---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-29T12:20:44'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# declare --write ya conserva los globs autorados

_Describe the incoming message with enough evidence to triage._

Hecho en sldb fa408854 (tarea cerrada por closeout b2ad79f6 con el run dir del executor Scion sldb-declare-globs): 'sldb stores declare --write' ahora conserva cada regla include autorada (glob o paths) tal cual y solo agrega lo que falta (links, modelos, documentos que ningún glob cubre). Verificado contra deskops/.sldb/store.yaml: include queda sin diff; lo único que cambiaría al reescribir son ~31 líneas de re-wrap de descripciones de predicados (ancho 100 vs el envuelto a mano); pendiente menor: ancho de save_declaration. No poda entradas paths que ya no estén en el índice: la intención autorada gana y stores build reporta missing.
