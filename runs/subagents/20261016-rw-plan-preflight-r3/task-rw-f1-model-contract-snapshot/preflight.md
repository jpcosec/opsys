RESTATEMENT:

1. Read `deskops/bootstrap.py`; extract `MODEL_REFS` (dict `name -> "module:Class"`).
2. Read `.sldb/core/store_index.yaml`; extract the listed model names.
3. Union `MODEL_REFS` names with the store_index names into one discovered model-name set (dedupe).
4. Import each discovered model class from `deskops.models:<Class>` (per the task text) and resolve it to the class object.
5. Call `sldb.store.hashing.hash_model_contract(...)` for each resolved class to get its sha256 hex.
6. Build a flat dict `{ModelName: hex}`, sorted by key, indentation unspecified; write it once to `tests/fixtures/model_contract_hashes.json`.
7. Create `tests/test_model_contract_snapshot.py`:
   - load the fixture;
   - redo steps 1–6 discovery at test time;
   - assert fixture key set == discovered set, message listing missing and extra names;
   - assert each fixture hash equals the freshly computed hash, message listing changed names, referencing store migration `task-rw-f6-migrate-tracking-stores` and printing the new hashes.
8. Run `pytest tests/test_model_contract_snapshot.py`.
9. Run `pytest tests`.
10. Manually edit one TaskDoc field description locally, rerun the snapshot test, confirm it fails naming `TaskDoc`, then revert the edit.
11. Hand the diff to the supervisor (no commit by executor).

AMBIGUITIES:

1. `hash_model_contract` signature unknown: does it take a model class, an instance, a schema object, or a name+module? Return type also unclear ("sha256 hex" — prefixed or bare, length, case).
2. Which name is the JSON key: the `MODEL_REFS` dict key, the class `__name__`, or the store_index entry name? These may differ, and the "naming the model" requirement depends on it.
3. `MODEL_REFS` values are `"module:Class"`, but step 1 of the Implementation Path says to import each from `deskops.models:<Class>` — contradiction; which module string wins for names whose module is not `deskops.models`.
4. Exact structure of `.sldb/core/store_index.yaml` (top-level key, list vs map, name field) is not given, so extraction is guesswork.
5. Which `.sldb/core/store_index.yaml` is meant: the repo's own store root, the deskops cwd, or the machine-level one; and relative to what working directory.
6. Behavior when a name collides between `MODEL_REFS` and store_index but resolves to different classes — union silently masks the conflict.
7. What to do with store_index names that are not importable from `deskops.models` (foreign/legacy models): skip, fail, or error is unspecified.
8. No regeneration mechanism is specified for the fixture (no script, no `--update` flag); "generate once" is ad hoc, so updating it deliberately is undefined.
9. JSON formatting details (indent, trailing newline, `sort_keys` vs pre-sorted) are unspecified, so the fixture diff is non-deterministic against the intent.
10. No requirement pins the sldb version, so a legitimate sldb hashing change flips the whole fixture with no distinction from a deskops model change.
11. Exact failure-message wording is constrained only loosely ("says a change requires a store migration", "prints the new hashes"); no template, so acceptance of the message is subjective.
12. Done When's manual edit-and-revert check cannot be verified by the test suite; no automated fixture proves it.
13. Task text does not state whether the fixture is expected to be committed in this task or generated at test-collection time.
