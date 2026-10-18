# task-rw-f1-model-contract-snapshot — result

## Changes

- Added `tests/test_model_contract_snapshot.py`
  - `_model_refs()`: unions `deskops.bootstrap.MODEL_REFS` with every `name`/`model_ref` in `.sldb/core/store_index.yaml` (index entries only fill names absent from `MODEL_REFS`).
  - `_load_model(model_ref)`: imports `<module>:<Class>`.
  - `_contract_hashes()`: maps each discovered name to `sldb.store.hashing.hash_model_contract(class)`.
  - `_snapshot()`: reads the committed fixture.
  - `test_snapshot_covers_the_registered_model_set()`: fails listing missing/extra model names.
  - `test_model_contract_hashes_match_the_snapshot()`: fails naming changed models, states that a store migration is required (task-rw-f6-migrate-tracking-stores), and prints the full new hash map.
- Added `tests/fixtures/model_contract_hashes.json` (17 models, sorted keys, generated from current code).
- Model set: the 12 `MODEL_REFS` models plus `RuntimeProfileDoc`, `RunDoc`, `MaterializationContractDoc`, `RelationTypeDoc`, `RelationDoc` from the store index.

## Validation commands and results

All run in `/tmp/rw/wt/modelsnap`:

- `PYTHONPATH=/tmp/rw/wt/modelsnap python -m pytest tests/test_model_contract_snapshot.py -q`
  - `2 passed in 0.31s`
- `PYTHONPATH=/tmp/rw/wt/modelsnap python -m pytest tests -q`
  - `348 passed, 3 skipped in 286.71s (0:04:46)`

## Done When check (manual mutation, reverted)

- Edited `TaskDoc.title` description in `deskops/models/task.py`, ran the focused test:
  - `1 failed, 1 passed`; failure named `TaskDoc` (`assert not ['TaskDoc']`), printed new hashes.
- Reverted `task.py` exactly from backup; `git diff --stat` empty for tracked files.
- Removed `TaskDoc` from the fixture and ran the focused test:
  - `1 failed, 1 passed`; `test_snapshot_covers_the_registered_model_set` reported `TaskDoc` as missing.
- Reverted fixture.

## Task discrepancies / ambiguities

- Cited path `../sldb/src/sldb/store/hashing.py:80` does not exist under `/tmp/rw/wt`; sldb is installed from `/home/jp/proyectos/SLDB_1/sldb/src/sldb/store/hashing.py`. `hash_model_contract` is there at line 80 as stated.
- The task did not specify precedence when a name exists in both sources with different refs; implemented `MODEL_REFS` first (`setdefault`), so no ref-conflict detection is performed.
- The store index itself contains 17 models, including `RuntimeProfileDoc` and `RunDoc` that are absent from `MODEL_REFS`; the union therefore snapshots 17, not 12.

## sldb issues

None observed.
