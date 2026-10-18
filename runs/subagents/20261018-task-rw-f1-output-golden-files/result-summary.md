# task-rw-f1-output-golden-files — result summary

## What changed

- `tests/fixtures/golden_desk/` (new): fixed fixture desk with
  - `desk/tasks/task-golden-alpha.md`, `desk/tasks/task-golden-beta.md`
  - `desk/atoms/atom-golden-one.md`, `desk/atoms/atom-golden-two.md`
  - `desk/contexts/pill-golden-rule.md`
  - `desk/drawer/tasks/task-golden-drawer.md`
  - `deskops/golden_sample.py` (unlinked source file, so `graph reflect` emits one finding instead of an empty report)
- `tests/fixtures/golden/` (new): committed goldens
  - `graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`
  - `run_index.jsonl`, `closeout_trailers.json`
  - `help/deskops*.txt` for the root and all 102 reachable subcommand paths
- `tests/test_output_goldens.py` (new): copies the fixture into `tmp_path`, `git init` + empty seed commit, drives the real CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...])`, normalizes `<root>`, `<ts>` and `<sha>`, and compares against the goldens. `--update-golden` rewrites them.
- `tests/conftest.py`: added `pytest_addoption("--update-golden")`.

No production code changed; no output format changed; no `desk/` mutation.

## Validation

- `PYTHONPATH=/tmp/rw/wt/goldens python -m pytest tests/test_output_goldens.py --update-golden -q`
  - `6 passed in 103.06s (0:01:43)`
- `PYTHONPATH=/tmp/rw/wt/goldens python -m pytest tests/test_output_goldens.py -q`
  - `6 passed in 104.46s (0:01:44)`
- Done When mutation check (temporarily renamed `metadata.confidence` to `confidence_renamed` in `deskops/graph/snapshot.py::_kgdb_edge`, then reverted):
  - `PYTHONPATH=/tmp/rw/wt/goldens python -m pytest tests/test_output_goldens.py -q -k "graph_snapshot or graph_networkx"`
  - `2 failed, 4 deselected in 2.08s`
  - `git diff --stat deskops/graph/snapshot.py` empty after revert.
- `PYTHONPATH=/tmp/rw/wt/goldens python -m pytest tests -q`
  - `1 failed, 364 passed, 3 skipped in 308.88s (0:05:08)`
  - Only failure: `tests/test_model_contract_snapshot.py::test_model_contract_hashes_match_the_snapshot`
  - Error: `Model contract changed for: RelationDoc`; fixture `tests/fixtures/model_contract_hashes.json` has `b9797de...` while the loaded model hashes to `e2ddf03...`.

## Pre-existing failure outside this task (not fixed)

- Re-ran with all local changes stashed: `PYTHONPATH=/tmp/rw/wt/goldens python -m pytest tests/test_model_contract_snapshot.py -q` → `1 failed, 1 passed`. The failure exists at HEAD without this task's changes.
- Cause is sibling `sldb`, not deskops: `/home/jp/proyectos/SLDB_1/sldb` HEAD `9ae689e` (2026-10-18) added `RelationDoc.attributes` (`src/sldb/models/relation_doc.py:62`) and re-signed its store model, so `hash_model_contract(RelationDoc)` no longer matches deskops's committed snapshot. Updating the deskops fixture is the separate deliberate migration owned by `task-rw-f6-migrate-tracking-stores`; it was left untouched.

## Ambiguities / notes

- The task says "2 tasks, 2 atoms, 1 pill and 1 drawer task". The fixture matches that; `deskops/golden_sample.py` was added solely so `graph reflect` produces a non-empty finding and the report's finding shape is pinned. It does not change any output format.
- Help pinning is exact text with `COLUMNS=80`. Subcommand discovery walks the real `positional arguments` output, so aliases such as `inbox` get their own snapshots.
- `run_index.jsonl` normalizes the `commit` field to `<sha>`; the fixed 64-hex `session_sha256` is intentionally left as a real value.
- Time cost: `tests/test_output_goldens.py` takes ~104s because it spawns the CLI for every help path (~100 subprocesses).
