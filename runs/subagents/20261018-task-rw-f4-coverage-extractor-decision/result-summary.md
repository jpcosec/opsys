# Result: task-rw-f4-coverage-extractor-decision (delete branch)

## Changes

- Deleted `deskops/graph/extract_coverage.py` (907 lines) and `tests/test_graph_extract_coverage.py`.
- `deskops/graph/__init__.py`: removed `CoverageExtraction`, `CoverageGraphEdge`, `CoverageGraphNode`, `extract_coverage_graph`.
- `deskops/graph/snapshot.py` (`build_graph_snapshot`): removed the coverage import, `extract_coverage_graph` call, coverage node merge, coverage edge merge, and `desk_kgdb_coverage_v1` from `metadata.source_extractors`. Narrowed `_edges_by_source`/`_kgdb_node`/`_kgdb_edge` types to `DeclaredGraphEdge` and removed the coverage-only edge metadata loop (`atom_id`, `facet`, `score`, `match_basis`, `evidence`, `source_field`).
- `tests/test_graph_snapshot.py`: removed the coverage-extractor assertion, the facet-node/`answers`-edge assertions, and changed the golden read test to assert the declared `task:task-golden-alpha -> atom:atom-golden-one` edge. Changed `edge_count > 2` to `>= 2` because two declared edges remain in the synthetic fixture.
- Re-recorded only `tests/fixtures/golden/graph_snapshot.kg.json` and `.nx.json` with `-k "graph_snapshot_golden or graph_networkx_golden" --update-golden`.
- Added `desk/drawer/issues/issue-coverage-extractor-removed.md` with the extractor description, scorers/thresholds, snapshot output, and last containing commit `c378d15641e423ca1cee29da0809eb45a74ddf8a`.

## Golden count difference

- `graph_snapshot.kg.json`: nodes 13 -> 7 (-6 facet nodes), edges 9 -> 7 (-2 `answers` edges), source extractors 4 -> 3.
- `graph_snapshot.nx.json`: 6 facet nodes and 2 links removed (7 nodes remain).

## Validation

- `PYTHONPATH=/tmp/rw/wt/coverage python -m pytest tests/test_graph_snapshot.py tests/test_graph_extract_coverage.py -q` (before any change): `11 passed in 0.36s`.
- `PYTHONPATH=/tmp/rw/wt/coverage python -m pytest tests/test_graph_snapshot.py tests/test_output_goldens.py -q` (after deletion, before fixing the stale edge-count assertion): `1 failed, 14 passed`; failure was `assert 2 > 2` at `tests/test_graph_snapshot.py:45`.
- `PYTHONPATH=/tmp/rw/wt/coverage python -m pytest tests/test_graph_snapshot.py -q`: `9 passed in 0.30s`.
- `PYTHONPATH=/tmp/rw/wt/coverage python -m pytest tests -q`: `408 passed, 3 skipped in 324.85s (0:05:24)`.
- `PYTHONPATH=/tmp/rw/wt/coverage python -m deskops graph build --root .`: `Graph snapshot written: /tmp/rw/wt/coverage/.sldb/runtime/graphs/deskops.kg.json` (exit 0).
- `grep -rn extract_coverage deskops/`: empty (also removed stale `__pycache__` pyc files).

## Task issues / ambiguity

- Cited line numbers were stale as warned: coverage merge is at `snapshot.py:138-141`, not 75-78; the `source_extractors` entry is at `snapshot.py:158`, not 92; the test assertion is at `tests/test_graph_snapshot.py:46`, not 43.
- The delete branch also required touching `deskops/graph/__init__.py` (coverage re-exports) and coverage-only type hints/metadata in `snapshot.py`; the task did not list these.
- Removing coverage required updating three additional assertions in `tests/test_graph_snapshot.py` beyond the `source_extractors` assertion: facet-node presence, `answers` edge presence, and the golden read test that expected `atom:atom-golden-one -> facet:what`; plus `edge_count > 2`.
- No sldb bug observed.
