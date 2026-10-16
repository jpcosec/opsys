RESTATEMENT:
1. Confirm task is active (doc says `status: deferred`; supervisor promotes first); do not commit.
2. Build the discovered model set: read `deskops.bootstrap.MODEL_REFS` (dict `name -> "module:Class"`), and read model names from `.sldb/core/store_index.yaml`; take the union of names.
3. For each discovered name, import the model class (doc says `deskops.models:<Class>`); keep a `name -> class` map.
4. Create `tests/fixtures/model_contract_hashes.json`: flat JSON object `{"<ModelName>": "<sha256 hex>"}`, keys sorted, generated once from current code.
5. Create `tests/test_model_contract_snapshot.py`: import `hash_model_contract` from `sldb.store.hashing`; for each model compute its contract hash.
6. In the test, load the fixture and compare key sets to the discovered name set; on mismatch, assert with message listing missing names and extra names.
7. For keys present in both, compare stored hash to computed hash; on mismatch, assert with message listing changed model names, stating a change requires a store migration (task-rw-f6-migrate-tracking-stores), and printing the new hashes so the fixture can be updated.
8. Run `pytest tests/test_model_contract_snapshot.py`.
9. Run `pytest tests`.
10. Verify Done When by hand: edit a TaskDoc field description locally, confirm the test fails naming the model, then revert the edit.

AMBIGUITIES:
1. `.sldb/core/store_index.yaml` schema is unknown — which key holds model names, and whether names match `MODEL_REFS` keys.
2. Which root the `.sldb/core/store_index.yaml` path resolves against (repo root vs CWD vs test file) is unspecified.
3. Doc says import `deskops.models:<Class>`, but `MODEL_REFS` values are `module:Class`; unclear whether to import from the value's module or always from `deskops.models`.
4. Union semantics for store_index.yaml names absent from `MODEL_REFS` — import source and how to locate the class unknown.
5. `hash_model_contract` signature/arguments (class vs instance vs store/path, and any extra params) are not stated; only a line reference is given.
6. Model name used as fixture key is `ModelName` — whether that is the class `__name__` or the `MODEL_REFS` key is unspecified; collisions across modules unresolved.
7. Deduplication rule when a name appears in both `MODEL_REFS` and store_index.yaml is unspecified.
8. Whether the test should skip/xfail (vs fail) when `.sldb/core/store_index.yaml` is missing is unspecified.
9. "Generate the fixture once" has no command or generator script; manual generation vs an in-test update flag (`--update`/env) undecided.
10. Fixture path resolution is not specified.
11. No acceptance criteria for hash stability/determinism; risk of flaky fixture regeneration unaddressed.
12. `.sldb/core/store_index.yaml` content is repo state, not the machine's 24 stores; the rationale's machine count is not a checkable criterion.
13. Done When depends on `hash_model_contract` covering field descriptions; unverified from the doc.
14. Contradiction: `status: deferred` vs a task_type of `implementation` with an execution-ready Implementation Path; blocking vs executing is not stated in the doc (Resolved Decisions say the supervisor promotes, not the executor).
