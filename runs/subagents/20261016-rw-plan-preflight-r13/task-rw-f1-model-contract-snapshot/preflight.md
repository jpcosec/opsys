RESTATEMENT:
1. Confirm dependencies are satisfiable: all `task-rw-f0-*` items, `task-doctor-crashes-on-deskless-roots` are closed/available; task-rw-f1 is still `deferred` until the supervisor promotes it to `desk/tasks/`.
2. Read `deskops/bootstrap.py` to get `MODEL_REFS` (dict `name -> "module:Class"`).
3. Read `.sldb/core/store_index.yaml`; parse the model names it lists.
4. Build the discovered model set = union of `MODEL_REFS` names and the store-index model names; for each entry import `Class` from `deskops.models:<Class>` (or its `module:Class` value).
5. Import `hash_model_contract` from `sldb.store.hashing`.
6. Call `hash_model_contract` on each discovered model to get a sha256 hex string.
7. Write `tests/fixtures/model_contract_hashes.json` as a flat `{"<ModelName>": "<sha256 hex>"}` object with sorted keys (one-off generation from current code).
8. Write `tests/test_model_contract_snapshot.py`:
   - discover the model set as in step 4,
   - assert fixture key set == discovered set, message listing missing and extra names,
   - assert each discovered model's hash == fixture hash, message listing changed names, stating a change requires a store migration (task-rw-f6-migrate-tracking-stores) and printing the new hashes.
9. Run `pytest tests/test_model_contract_snapshot.py`.
10. Run `pytest tests`.
11. Manually edit a TaskDoc field description, rerun the test, confirm it fails naming TaskDoc, then revert the edit.
12. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:
1. `.sldb/core/store_index.yaml` schema is unspecified — which key/path yields "model names", and whether the file exists at the deskops root, is unknown.
2. Whether fixture keys use `MODEL_REFS` dict keys or the Python class `__name__` is unspecified ("<ModelName>" and "name -> module:Class" both support either reading).
3. Import source is contradictory: step 2 says MODEL_REFS values are `module:Class`, but step 1 says "import each `deskops.models:<Class>`". If a class is not re-exported by `deskops.models`, which module to import from is unclear.
4. `hash_model_contract` signature/semantics at `../sldb/src/sldb/store/hashing.py:80` are not given — whether it takes a class, instance, store, or registry is unknown.
5. Whether the union must include models present only in `store_index.yaml` but not importable, and how to handle duplicates under different names, is undefined.
6. No generator script is specified for step 4/7; whether to add one or generate ad-hoc is undefined.
7. The negative-case proof ("fails naming the model when a TaskDoc field description is edited locally") is manual and not automated, yet Validation only runs the two pytest commands — how CI substantiates the Done When's failure behavior is unresolved.
8. Scope says "Out of scope: changing any model (F6)" while Done When requires editing a TaskDoc field description; the "then revert" instruction resolves intent but leaves unclear whether any temporary model edit may appear in the diff.
9. Task `status: deferred` with a large `depends_on` list: whether execution must wait for all dependencies closed, or may proceed, is not stated.
10. Failure-message details (exact wording beyond "names the model", "requires a store migration (task-rw-f6-migrate-tracking-stores)", "prints the new hashes", and whether output goes to assertion message vs stdout) are unspecified.
11. Exact command for the supervisor closeout (`--run-dir <dir>`) references a run directory whose presence/format is not defined here.
