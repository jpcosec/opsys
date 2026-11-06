---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T16:30:26'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout: una materialization con target_identity de paquete no cubre los archivos del paquete

_Describe the incoming message with enough evidence to triage._

Al cerrar SV01-SV04 en sldb (2026-11-06), el gate atom|materialization de closeout verify exigio un enlace por archivo declarado en files. Los src/sldb/*.py no son nodos del grafo del desk (FILE_RULES solo hace source_file a desk/ y deskops/), asi que la unica cobertura real es una materialization por archivo con target_identity exacto: probe una con target_identity src/sldb/notations (paquete) y no cubrio ninguno de sus archivos. Resultado: 62 materializations para 66 archivos de cuatro tareas. Sugerencia para CC33 (closeout como regla): que un target_identity que nombre un directorio cubra los archivos bajo el, o que una materialization acepte una lista de targets; y que el mensaje del gate diga que el enlace es por archivo exacto. Registrado a pedido del supervisor deskops-sobre-sldb-config.
