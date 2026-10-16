RESTATEMENT:

1. Read `deskops/bootstrap.py` to inspect `MODEL_REFS` (dict name -> `module:Class`) and confirm its structure.
2. Read `.sldb/core/store_index.yaml` to extract the model names it lists.
3. Union the two name sets to form the discovered model set.
4. For each name, import the class from `deskops.models:<Class>` (resolving via `MODEL_REFS` mapping; for store-index-only names, assume `deskops.models:<Name>`), then call `sldb.store.hashing.hash_model_contract(Class)` to get a sha256 hex.
5. Write `tests/fixtures/model_contract_hashes.json`: flat JSON object `{"<ModelName>": "<sha256 hex>"}` with sorted keys, generated once from current code.
6. Write `tests/test_model_contract_snapshot.py` that:
   - discovers the same model set (MODEL_REFS ∪ store_index names),
   - loads the fixture JSON,
   - asserts fixture key set == discovered set, listing missing and extra names in the failure message,
   - asserts each hash matches, listing changed names; failure message states a change requires a store migration (task-rw-f6-migrate-tracking-stores) and prints new hashes so the fixture can be updated deliberately.
7. Run `pytest tests/test_model_contract_snapshot.py`.
8. Run `pytest tests`.
9. Manually edit a TaskDoc field description locally, confirm the test fails naming the model, then revert the edit.
10. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:

1. Resolution rule for store-index names not present in `MODEL_REFS` (assume `deskops.models:<Name>` vs. some other mapping) is unspecified.
2. Whether store_index entries include non-deskops models (e.g., sldb-internal models) that should be excluded from the discovered set is not stated.
3. Store index key format is unspecified (may be names, paths, or refs), so extraction of "model names" is guesswork.
4. `deskops.models` module existence/location is not confirmed; models may live elsewhere.
5. Fixture regeneration procedure (script vs. one-off manual command) is not specified.
6. `hash_model_contract` signature/return type (function vs. expects schema input) is not documented in the task; assumed to take a class and return hex.
7. No acceptance criterion for how "listing missing and extra names" must be formatted in the failure message.
8. Task status is `deferred` but the prompt asks to execute; whether deferred tasks are executable is unclear.
