---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T18:23:48'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD26 cerrado en sldb: scaffold de store desde carpetas y semillas declaradas

_Describe the incoming message with enough evidence to triage._

GD26 cerrado en sldb (squash 96d7b823, closeout 713978e5). Nuevo: sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root=None) -> ScaffoldReport (created/rewritten/present/conflicts/applied, idempotente, escrituras en transacción), sldb.api.build_store(store, *, apply=True, generate=None) (build + scaffold en un reporte), modelos sldb.api.Seed y StoreDeclaration con folders y seeds (if_missing | managed; fuentes text, file relativa o pkg:modulo/ruta, document {model, name, payload} con track). CLI: sldb stores scaffold [--apply] [--format] con envelope; sldb stores build gana la sección scaffold. Doc: docs/architecture/store-declaration.md. Sin ruta de serve. Queda sin motivo en deskops el código que crea a mano la estructura del desk y sus archivos iniciales (carpetas, .keep, plantillas, documentos semilla): puede declararlos como folders/seeds en su paquete y pasarlos por declaration= con template_root o pkg:, sin cambiar su store.yaml si declara antes un include glob que cubra las semillas trackeadas (CC36 declara las semillas).
