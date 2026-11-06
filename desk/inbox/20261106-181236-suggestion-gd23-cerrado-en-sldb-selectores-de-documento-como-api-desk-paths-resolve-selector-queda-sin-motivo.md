---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T18:12:36'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD23 cerrado en sldb: selectores de documento como API; desk_paths.resolve_selector queda sin motivo

_Describe the incoming message with enough evidence to triage._

GD23 cerrado en sldb (squash 850f8fca, closeout 0b72a473): sldb.api.select_documents(store, selector, expect=many|one) con claves ref, prefix, path_glob, model, where, include_linked (conjunción); filas {export_id, model, name, path}; errores SLDBDocumentTargetError (ninguno) y AmbiguousSelectionError.candidates (varios); sldb.api.Selector es el mapa validado. Comando: sldb docs select [--ref] [--prefix] [--path-glob] [--model] [--where] [--one] [--include-linked] [--format json] (--envelope: docs/missing, docs/ambiguous). Ruta: GET /docs/select con los mismos nombres como query params; 404/409(candidates)/400. Doc: docs/architecture/selectors.md. Código de deskops que queda sin motivo: deskops/desk_paths.py resolve_selector (y _relative_candidates), junto con los llamadores que arman directories/pattern/recursive para él; se retira en CC35 reemplazándolos por select_documents(store, {prefix: selector, model: <modelo del artefacto>}, expect=one).
