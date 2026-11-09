---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-09T13:34:11'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Nombres de tarea con acentos: git cita las rutas y el hook de wt las rechaza

_Describe the incoming message with enough evidence to triage._

Reportado por el coordinador de AntonIA (vía overlord SLDB_1, 2026-11-09). Con tareas cuyo id/slug lleva acentos (p. ej. task-cc35a-transacción-...), git imprime las rutas citadas y con escapes octales (core.quotepath=true por defecto), y el hook de wt las rechaza. Hoy lo esquivan con core.quotepath=false por entorno. Opciones: que deskops pase -c core.quotepath=false (o use -z) en los git que parsea, que los slugs de id se normalicen a ASCII, o ambas. Ojo: ya hay ids con acentos commiteados (CC35a), así que normalizar exige migración o alias.
