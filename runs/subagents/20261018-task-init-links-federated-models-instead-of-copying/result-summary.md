# Result summary

## Changed

- `deskops/bootstrap.py`
  - Added `DESKOPS_STORE_LINK = "deskops"`.
  - Replaced `_add_model` (`models add`) with `_register_models`, which:
    - links the owner store (`<deskops installation>/.sldb`) with `sldb.api.link_store`;
    - inherits each `MODEL_REFS` entry with `sldb.api.inherit_model("deskops:<Model>")`;
    - converts existing copies in place (skips inherited entries and local overrides);
    - runs `sldb.api.init_relations` (`sldb edges init`);
    - runs `sldb.api.update_store_indexes` (`sldb stores update`) so a fresh store passes `stores check`.
  - Added `_deskops_owner_store`, `_ensure_owner_link`, `_inherit_model`, `_init_relations`, `_update_store_indexes`, `_registered_model_entries`, `_store_link_names`.
  - `ensure_global_store_and_models` and `init_local_store` now use `_register_models`.
- `deskops/cli/commands/desk.py`
  - `desk update` detects copied deskops entries (`origin` empty, `model_ref` equals the MODEL_REFS ref) and reports `- Copied deskops models: ...`.
  - `--apply` calls `init_local_store`, which converts them via `inherit_model`; conversion is idempotent.
- `tests/test_federated_models.py` (new)
  - Fresh `deskops init` store: every deskops model has `origin: deskops`, `path: ""`, and `sldb stores check` exits 0.
  - Copied store: `desk update --apply` converts every deskops model, preserves the tracked `BoardDoc/Board` document, `stores check` exits 0, and a second update reports `Desk is up to date.`
- `tests/e2e_agent/scenarios/first-task-to-closeout.yaml`
  - Edge check now uses `sldb edges check --store .sldb --local` (see ambiguity/bug note below).

## Validation

- `PYTHONPATH=/tmp/rw/wt/federated python -m pytest tests -q`
  - `371 passed, 3 skipped in 312.84s`
- `PYTHONPATH=/tmp/rw/wt/federated python -m sldb stores check --store .sldb`
  - `PASS: store integrity — 223 documents in 17 models` (exit 0)
- `PYTHONPATH=/tmp/rw/wt/federated python -m deskops --help`
  - exit 0
- `PYTHONPATH=/tmp/rw/wt/federated python -m pytest tests/test_federated_models.py -q`
  - `2 passed`

### Against unfixed code

Restored HEAD versions of `deskops/bootstrap.py` and `deskops/cli/commands/desk.py` temporarily, then ran the new tests:

- `2 failed in 6.71s`
- Both failed at `assert entry.origin == "deskops"` (fresh init left a copied entry; update left `origin=None`), then the files were restored (sha256 verified).

## Incorrect or ambiguous task points

- The task says “16 deskops models”, but `deskops/bootstrap.py` registers 12 (`MODEL_REFS`). `init` now inherits exactly those 12. The repo’s owner store also has `RuntimeProfileDoc`, `RunDoc`, `MaterializationContractDoc`, `RelationTypeDoc`, and `RelationDoc`; `init_relations` registers the two relation models locally, the other three are not registered by `init` (same as before this task).
- The task cites `sldb edges init`; the Python API is `sldb.api.init_relations`.
- The task says `sldb stores check` passes for a fresh store. After `inherit_model` on an empty store, it fails until `stores update`:
  - Command: `sldb stores check --store <fresh store>`
  - Output: `FAIL: store integrity — 0 documents in 12 models — 12 roster-only` with `roster stale: roster hash disagrees over 0 documents on disk`
  - `sldb stores update --store <fresh store>` fixed it, so `_register_models` calls `update_store_indexes` after inheriting. This looks like an sldb behavior/gap, not fixed here.
- With the owner linked, `sldb edges check --store .sldb` follows links and reports the owner’s pre-existing stale edge index (`0 error(s), 223 stale`), even though `sldb edges check --store .sldb --local` is `Edges OK`. The e2e scenario check was changed to `--local` to keep `pytest tests` green without mutating the owner store.
