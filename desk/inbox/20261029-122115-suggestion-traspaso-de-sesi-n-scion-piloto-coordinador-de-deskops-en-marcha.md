---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-29T12:21:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Traspaso de sesión: Scion piloto, coordinador de deskops en marcha

_Describe the incoming message with enough evidence to triage._

Estado al cerrar la sesión en esta máquina (2026-10-29). Scion corre local (hub 127.0.0.1:8080, proyecto sldb-1 = raíz SLDB_1 shared-plain, secret CLAUDE_AUTH desde ~/.claude/.credentials.json, hook deskops-tools, templates deskops-executor y deskops-coordinator). Piloto: agente deskops-coordinator lanzado con primer trabajo task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo; replicar a sldb/spec2viz/scion solo si cierra solo. Decisiones del dueño registradas: evidencia de closeout declarada al crear la tarea; journal = historia git de los shards; .sldb operacional versionado y .sldb_cache ignorado (tarea en sldb); dos tareas de diseño en sldb. Pendientes: secret CODEX_AUTH (lo pone el dueño), antigravity sin token en host, harness pi. Cómo seguir desde otra máquina: git pull en deskops/sldb/spec2viz/scion; en esta máquina 'scion server status', 'scion list' y 'docker exec -u scion sldb-1--deskops-coordinator tmux capture-pane -p -t scion:agent' muestran al coordinador; los commits del coordinador quedan locales en deskops y hay que pushearlos tras revisarlos.
