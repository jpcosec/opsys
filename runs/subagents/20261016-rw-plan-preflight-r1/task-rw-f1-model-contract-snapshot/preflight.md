RESTATEMENT:
1. Inspect `../sldb/src/sldb/api.py` for a public `hash_model_contract` wrapper; if absent, import `hash_model_contract` from `sldb.store.hashing`.
2. Determine the concrete names/objects in `deskops.bootstrap.MODEL_REFS` and how models are registered from `.sldb/core/models/` (glob, loader, or registry API).
3. Create `tests/fixtures/model_contract_hashes.json` with one entry per model: model id → contract hash.
4. Create `tests/test_model_contract_snapshot.py` that: collects all target models, computes `hash_model_contract(model)` for each, loads the fixture, and asserts per-model equality, failing with a message naming the changed model.
5. Ensure the test also fails on added/removed models (or document why not).
6. Run `pytest tests/test_model_contract_snapshot.py` to confirm it passes on current code.
7. Temporarily edit a model field description to confirm the test fails and names the model; revert.
8. Run `pytest tests` and confirm no regressions.

AMBIGUITIES:
1. `deskops.bootstrap.MODEL_REFS` — module path, type (list of names, refs, or classes), and contents are not specified.
2. No SLDB API is named for enumerating/loading models in `.sldb/core/models/`; discovery method is unknown.
3. `.sldb/core/models/` path resolution (repo root vs store root vs cwd) is unspecified.
4. `hash_model_contract` signature (accepts class, instance, name, ref) is unspecified.
5. Fixture JSON schema (flat map, ordering, nesting) is unspecified.
6. Whether the snapshot must also detect added/removed models, or only changed hashes, is unspecified.
7. No mechanism is given for regenerating the fixture (script, CLI, or manual edit).
8. Failure-message format ("prints which model changed") is unspecified.
9. Whether `sldb` is an optional dependency requiring a skip/guard is unspecified.
10. Overlap between bootstrap models and `.sldb/core/models/` models (dedupe rules) is unspecified.
11. Task doc states "Open Ambiguities: None", contradicting the missing details above.
12. All listed `depends_on` tasks appear deferred/other-phase; whether they must be closed first is not stated here.
