---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T20:06:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD22 cerrado en sldb: referencias entrantes y reescritura

_Describe the incoming message with enough evidence to triage._

sldb (squash 2570b710, closeout 680adcc4) trae sldb.api.referrers(store, target) y sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None, dry_run=False, pythonpath=None) con Referrer {source, field, index, location, origin} y RewriteReport {changed, skipped}; CLI sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO | --remove [--dry-run] (envelope); rutas GET /edges/referrers?target= y POST /edges/rewrite {target, replacement|null, dry_run}; doc docs/architecture/references.md. Las referencias salen del índice de aristas (campos declarados, anclas de __doc_anchors__) y del project_graph declarado en store.yaml (menciones por MentionPattern, token completo, punto final de frase excluido); la reescritura va en sldb.api.transaction (todo o nada) y conserva la forma del valor. Queda sin motivo en deskops: services/atoms.py _find_inbound_atom_references y _rewrite_inbound_atom_references (y sus envoltorios en operations.py), el rglob sobre desk/ con el regex atom:<id>, y el chequeo inbound de services/retire.py (_inbound_references); el merge/split de átomos puede llamar a rewrite_references con la transacción abierta. Satisface G_GD22.
