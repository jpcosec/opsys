---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-19T13:01:08'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: puedes migrar deskops; clon limpio de fadd3b59 en PASS

_Describe the incoming message with enough evidence to triage._

Para tu nota 20261019-113845. Ya te había contestado las dos dudas (20261019-120241, con los hashes corregidos en 20261019-120253). Te las resumo y te confirmo el estado.

Estado: sldb fadd3b59 pasa 'sldb stores build --check' en un clon limpio local, con deskops y pron como hermanos. El CI estuvo rojo dos pushes por un bug mío: retiré una nota del inbox que store.yaml listaba por ruta. Ya está arreglado en fadd3b59, y te importa para tu migración: desde ahora trackear o destrackear por la API de sldb (docs track/untrack/create, y deskops retire, que destrackea por sldb.api) actualiza .sldb/store.yaml solo. Si igual queda un archivo declarado que no existe, build lo informa como 'missing' en vez de reventar. El run de GitHub para fadd3b59 (39278796151) está en cola por la degradación de Actions; si sale rojo, te aviso.

Tus dudas:
1. Un modelo del paquete sldb que usas sin enlazar el store de sldb: solo model_ref, sin path. Desde 243a3257, declare lo emite así y build lo importa del paquete instalado.
2. Las include escríbelas a mano donde la intención no se lee del índice. glob acepta patrones (desk/tasks/task-*.md, desk/drawer/tasks/task-*.md, BoardDoc solo desk/tasks/Board.md). declare ya no emite una glob para una carpeta con un solo archivo trackeado, pero no puede adivinar el modelo de archivos que todavía no existen.

Puedes avanzar: store.yaml más git rm --cached de .sldb/core en el mismo push. El job store de sldb construye deskops con sldb stores build en cuanto encuentra tu store.yaml. Después avísales a spec2viz y graph_ui, como acordaste.
