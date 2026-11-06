---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T20:43:19'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD25 cerrado en sldb: vistas declaradas; el tablero armado a mano queda sin motivo

_Describe the incoming message with enough evidence to triage._

GD25 cerrado en sldb (squash 05b4135f, closeout 2d5cf98e): vistas declaradas. Nueva función sldb.api.run_view(store, name, params) → {view, params, revision, sections} y sldb.api.list_views(store); ViewDoc (sldb.models.notation_models) tipa params (lista de {name, required, default}) y sections ({key, select, fields, edges, group_by, group_order, rules, transitions}) y valida al escribir (selectores y where que parsean, params referenciados declarados, nombre projection reservado). Nuevos comandos sldb views run NAME [--param k=v ...] y sldb views list (envelope) y rutas GET /views y GET /views/<name>?k=v con ETag = revision y 304 por If-None-Match. Doc: docs/architecture/views.md. Queda sin motivo en deskops el código que arma el tablero y sus columnas a mano (agrupar TaskDocs por estado en orden fijo, juntar dependencias entrantes/salientes, findings de reglas y transiciones posibles/bloqueadas por tarea), y cualquier provider o campo calculado en Python: un hecho externo (p. ej. de git) se escribe como documento del store (recibo, kind evidence) enlazado a la tarea y la vista lo lee por edges. Para migrar: una ViewDoc tablero con select: {model: TaskDoc}, group_by el campo de estado y group_order la lista de columnas, edges para depends_on y los recibos, rules con las RuleDocs del desk y transitions: {from_field: current_node, relation: <tipo>} (el campo debe contener el id del nodo, Model:name).
