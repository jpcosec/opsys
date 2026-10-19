---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-19T12:02:53'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: corrección de hashes en mi nota 20261019-120241

_Describe the incoming message with enough evidence to triage._

En mi nota anterior puse dos hashes mal. Los correctos son: 08811873 (los tres tests que dejaron de depender del store del repo) y 243a3257 (declare ya no escribe rutas absolutas ni globs de un solo archivo). El CI en verde es el de 96854c75.
