RESTATEMENT:
1. Inspect `deskops/bootstrap.py` for `MODEL_REFS` (dict name -> `"module:Class"`); read `.sldb/core/store_index.yaml` for its model entries and `model_ref` values; union the name sets.
2. For each name, import the class from `MODEL_REFS[name]` or the store index `model_ref`; additionally import `RelationDoc` and `RelationTypeDoc` from `sldb.models`.
3. For each imported class, call `sldb.store.hashing.hash_model_contract` to get its sha256 hex (reading `../sldb/src/sldb/store/hashing.py:80` to confirm call signature).
4. Write `tests/fixtures/model_contract_hashes.json` as a flat sorted-key JSON object `{ModelName: "<sha256 hex>"}` generated from current code.
5. Write `tests/test_model_contract_snapshot.py`: re-discover the name set and recompute hashes the same way; assert fixture keys == discovered keys, listing missing and extra names in the failure message; assert each hash matches, listing changed names.
6. Ensure the failure message states a change requires a store migration (task-rw-f6-migrate-tracking-stores) and prints the new hashes.
7. Run `pytest tests/test_model_contract_snapshot.py`, then `pytest tests`.
8. Manually edit one TaskDoc field description, confirm the test fails naming TaskDoc, then revert the edit.
9. Leave committing to the supervisor; do not commit.

AMBIGUITIES:
1. `hash_model_contract` input is not stated (class object vs. `"module:Class"` ref vs. name string), nor its return type/error behavior.
2. Precedence is unspecified when a name appears in both `MODEL_REFS` and the store index with a different `model_ref`.
3. `.sldb/core/store_index.yaml` schema is not described (top-level key holding models, per-entry field names, how `model_ref` is spelled).
4. The path `.sldb/core/store_index.yaml` is not anchored to a root/cwd; resolution is unclear.
5. Source of `RelationDoc`/`RelationTypeDoc` is stated only as "registered by the lifecycle graph"; no runtime mechanism is given for discovering them.
6. Whether store-index entries whose `model_ref` is not a deskops model should be included in the union is not stated.
7. "the registered set" is undefined: it is unclear whether registration means deskops bootstrap registration or sldb store registration, and how double counting is avoided.
8. Failure-message format beyond "names the model" and "prints the new hashes" is unspecified; no required ordering or exact text.
9. It is unclear whether the test should only print new hashes or also offer to rewrite the fixture (auto-update vs. print-only).
10. The location/lifetime of any fixture-generation script is unspecified (ephemeral vs. committed).
11. Done When only verifies the field-description case; no manual check is required for model added/removed, so that half of the Goal is unexercised by the stated acceptance.
12. Availability/importability of `sldb` in the test environment is assumed, not stated (F0 dependency `task-rw-f0-declare-runtime-dependencies` is only listed in `depends_on`).
13. No acceptance criterion covers fixture hash-format assumptions if the hashing algorithm changes.
