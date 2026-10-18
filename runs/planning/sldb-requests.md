# sldb API requests from deskops

## Export the model renderer from `sldb.api`

- **Function:** `sldb.runtime.validation.render_model_markdown(model_type, payload, ref_root=None)`
- **Why:** `deskops/doc_io.py` renders a payload for an untracked file before writing it.
  `sldb.api.create_document` renders and tracks in one step, but it cannot write a file
  that must stay untracked, and `save_document_payload` only handles already-tracked
  documents. Importing `sldb.runtime.validation` directly keeps that one write inside
  `doc_io`, listed in its `PRIVATE_SLDB_IMPORTS`.
- **Proposed API:** re-export `render_model_markdown` from `sldb.api` (or add
  `render_document_payload(store, model_name, payload)`), so consumers can render without
  reaching into `sldb.runtime.validation`.
