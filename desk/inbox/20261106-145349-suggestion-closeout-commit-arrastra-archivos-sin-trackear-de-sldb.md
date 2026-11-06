---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T14:53:49'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout commit arrastra archivos sin trackear de .sldb

_Describe the incoming message with enough evidence to triage._

deskops/services/closure.py:445-448: si git status --porcelain -- .sldb no está vacío, el closeout hace git add -A -- .sldb, que también agrega archivos SIN TRACKEAR ajenos a la tarea. En sldb (2026-11-06) el closeout de task-go03 (ec15bd27) commiteó 202 PythonSymbolDoc y dos TaskDoc huérfanos que estaban sin trackear en el clon; se corrigió con e1805fc6. Sugerencia: agregar solo los paths ya trackeados (git add -u -- .sldb) más los que la propia transacción del closeout escribió, o respetar --paths. Aparte: el registro de repos resuelve deskops a /home/jp/proyectos/SLDB_1/deskops en robocop2 (PermissionError con --to deskops).
