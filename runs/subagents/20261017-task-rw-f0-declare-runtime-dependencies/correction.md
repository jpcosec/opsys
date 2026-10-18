# Correction: task-rw-f0-declare-runtime-dependencies

The task rested on a false premise.

- kgdb no longer exists as a project. Its graph layer was merged into sldb (sldb merge 6deb222, ADR 2026-09-20); the public API is `sldb.api.graph.snapshot` (`snapshot_load`, `GraphSnapshot`) plus `sldb.store.graph.graph_io.load_graph`/`save_graph`.
- The kgdb 0.1.0 installed in the base environment is a leftover and is not a dependency.
- `task-graph-uses-sldb-graph-api-instead-of-kgdb` removed `"kgdb>=0.1.0"` from `pyproject.toml`, rewrote the graph imports in `deskops/graph/snapshot.py` and `deskops/cli/main.py` to sldb, updated `tests/test_graph_snapshot.py` and `tests/test_graph_cli.py`, and verified `pytest tests` and `deskops graph build` in a fresh venv without kgdb.
- The original task's venv install also failed for an unrelated kgdb packaging defect (kgdb requires the `sldb` distribution; the sibling checkout is `structuredLanguageDB`). That defect is moot now that kgdb is gone.
