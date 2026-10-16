RESTATEMENT:
1. Read `deskops/bootstrap.py`; confirm `MODEL_REFS` is a dict `name -> "module:Class"`.
2. Read `.sldb/core/store_index.yaml`; extract the model names it lists (format to be determined from the file).
3. Build the discovered model set = union of `MODEL_REFS` keys and the index-listed names; resolve each to a class (`importlib.import_module("deskops.models")` + `getattr` for index-sourced names; the ref's own module for `MODEL_REFS` entries).
4. Import `sldb.store.hashing.hash_model_contract` and compute a hash per resolved class.
5. Generate `tests/fixtures/model_contract_hashes.json` once from current code: flat object `{"<ModelName>": "<sha256 hex>"}`, sorted keys.
6. Write `tests/test_model_contract_snapshot.py` with two assertions: (a) fixture key set == discovered set, message listing missing and extra names; (b) each fixture hash == computed hash, message listing changed names and printing new hashes, and stating a change requires a store migration (task-rw-f6-migrate-tracking-stores).
7. Run `pytest tests/test_model_contract_snapshot.py`, then `pytest tests`.
8. Manually edit one TaskDoc field description, rerun the test, confirm it fails naming `TaskDoc`, then revert the edit.
9. Leave all commits to the supervisor (no executor commit).

AMBIGUITIES:
1. `.sldb/core/store_index.yaml` schema unknown: key name, list vs map, and whether entries are bare class names or `module:Class` refs.
2. Whether index-listed names are guaranteed importable from `deskops.models`; no rule for non-deskops or unresolvable names (skip, fail, or ignore).
3. Whether `hash_model_contract` expects a class, a model ref, or a registered model, and whether the full registry must be registered first (ordering/side-effect dependency).
4. Return format of `hash_model_contract` (bare hex vs prefixed like `sha256:...`) and required case; unclear whether the fixture stores it verbatim.
5. "Generate the fixture once" — no specified mechanism (throwaway script, `__main__` block, CLI flag, manual).
6. JSON serialization details unspecified: indentation, trailing newline.
7. Whether the test creation path assumes `tests/fixtures/` already exists.
8. Behavior when `.sldb/core/store_index.yaml` is absent (CI, other checkouts): fail vs skip undefined.
9. Duplicate names present in both `MODEL_REFS` and the index: no precedence rule; same for conflicting module sources.
10. Failure-message wording ("a change requires a store migration") and "prints the new hashes": literal-string vs free-text, print vs assertion message — not testable as written.
11. One test function or two (set-diff vs hash-diff) unspecified.
12. Done When hand-check names no specific model/store and no acceptance threshold beyond "fails naming the model".
