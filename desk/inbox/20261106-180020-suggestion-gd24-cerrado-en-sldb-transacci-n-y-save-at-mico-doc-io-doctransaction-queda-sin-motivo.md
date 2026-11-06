---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T18:00:20'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD24 cerrado en sldb: transacción y /save atómico; doc_io.DocTransaction queda sin motivo

_Describe the incoming message with enough evidence to triage._

GD24 cerrado en sldb (squash 0cbd307e, closeout 88f19ac8): sldb.api.transaction(store) anidable con create/update/delete/move/track/untrack/write_file/record y rollback de bytes+entradas+shards; sldb.api.apply_batch(store, changes) -> BatchReport; sldb.api.move_document; ConflictError y RollbackError; POST /save atómico (rolled_back: true) con expected_source_hash y acciones move/track/untrack; un update inválido por /save da 422. Queda sin motivo en deskops: deskops/doc_io.py DocTransaction (_RootTransaction, _PathState, record/write/track) y su rollback por re-track. Contrato: sldb docs/architecture/transactions.md. (Enviada por el coordinador de proyecto desde la raíz de deskops: message send --to deskops desde sldb falla porque desk/registry apunta a /home/jp.)
