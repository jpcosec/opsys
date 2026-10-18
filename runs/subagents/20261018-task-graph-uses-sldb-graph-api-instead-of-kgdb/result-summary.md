# task-graph-uses-sldb-graph-api-instead-of-kgdb — executor summary

## Changes

- `pyproject.toml` — `[project].dependencies`: removed `"kgdb>=0.1.0"`. Nothing else changed.
- `deskops/graph/snapshot.py` — `_validate_graph_snapshot`: import `GraphSnapshot` from `sldb.api.graph.snapshot`; on `ImportError` raise `GraphSnapshotCapabilityError` with an sldb-naming message ("sldb graph API unavailable (sldb.api.graph.snapshot); upgrade structuredLanguageDB before running `deskops graph build`."). Also updated the exception class docstring from KGDB to sldb.
- `deskops/cli/main.py` — `CLI._graph_build`: replaced `kgdb.graph` imports with `from sldb.api.graph.snapshot import snapshot_load` and `from sldb.store.graph.graph_io import save_graph`; now calls `save_graph(snapshot_load(output_path), networkx_path_for_snapshot(output_path))`. Imports stay function-local.
- `tests/test_graph_snapshot.py` — import `GraphSnapshot` from `sldb.api.graph.snapshot`.
- `tests/test_graph_cli.py` — replaced `test_graph_build_reports_missing_kgdb_capability` with `test_graph_build_reports_missing_sldb_graph_capability`; it sets `sys.modules["sldb.api.graph.snapshot"] = None` so the real validation path raises, then asserts exit 1, the sldb error text, and no snapshot written. Removed the now-unused `GraphSnapshotCapabilityError` import.
- `desk/contexts/pill-008-kgdb-sldb-boundary.md` — rewrote title/What/Why/When/Where/How/How Not to the current boundary (graph layer owned by sldb; no kgdb dependency); dropped `system:kgdb`; kept the filename and pill id.
- `runs/planning/rewrite-plan/gen.py` — in the `task-rw-f0-declare-runtime-dependencies` entry, prefixed `why` with the 2026-10-18 correction (false premise, kgdb merged into sldb, dependency dropped). Text only; not regenerated.
- `runs/planning/deskops-rewrite-inventory.md` — added a 2026-10-18 note under Estado.
- `runs/subagents/20261017-task-rw-f0-declare-runtime-dependencies/correction.md` — new file recording the same correction.

## Cited line numbers verified

- `deskops/cli/main.py:251-252` — still `from kgdb.graph import load_graph` / `save_graph` before edit.
- `deskops/graph/snapshot.py:119` — still `from kgdb.contracts.io import GraphSnapshot`.
- `tests/test_graph_snapshot.py:6` — still `from kgdb.contracts.io import GraphSnapshot`.
- `tests/test_graph_cli.py:165` — still `test_graph_build_reports_missing_kgdb_capability`.

## Validation (exact commands and final lines)

| Command | Result |
|---|---|
| `grep -rn "kgdb" --include=*.py deskops tests \| grep -v "_kgdb_\|kgdb_graph_snapshot\|kgdb_snapshot\|kgdb_coverage\|\.kgdb\.json\|integrate-kgdb\|write-kgdb"` | no output, exit 1 |
| `grep -rn "kgdb" pyproject.toml` | no output, exit 1 |
| `PYTHONPATH=/tmp/rw/wt/nokgdb python -m pytest tests/test_graph_snapshot.py tests/test_graph_cli.py -q` | `21 passed in 1.48s` |
| `PYTHONPATH=/tmp/rw/wt/nokgdb python -m deskops graph build --root .` | `Graph snapshot written: /tmp/rw/wt/nokgdb/.sldb/runtime/graphs/deskops.kg.json`, exit 0 |
| `PYTHONPATH=/tmp/rw/wt/nokgdb python -m pytest tests -q` | `351 passed, 3 skipped in 207.54s` |
| `/tmp/rw/f0/venv-nokgdb/bin/python -c "import kgdb"` | `ModuleNotFoundError: No module named 'kgdb'`, exit 1 |
| `PYTHONPATH=/tmp/rw/wt/nokgdb /tmp/rw/f0/venv-nokgdb/bin/python -m deskops graph build --root .` | `Graph snapshot written: ...`, exit 0 |
| `PYTHONPATH=/tmp/rw/wt/nokgdb /tmp/rw/f0/venv-nokgdb/bin/python -m pytest tests -q` | `351 passed, 3 skipped in 204.97s` |

Fresh venv: `/tmp/rw/f0/venv-nokgdb`, Python 3.13.5. Installed with
`pip install /home/jp/proyectos/SLDB_1/sldb -e /tmp/rw/wt/nokgdb pytest pytest-asyncio` (exit 0).
Versions: structuredLanguageDB 0.1.10, pytest 9.1.1, pytest-asyncio 1.4.0; deskops 0.1.0 editable.

## Test against unfixed code

- Exported HEAD with `git archive HEAD` to `/tmp/rw/f0/unfixed-nokgdb` and ran with the kgdb-free venv.
- `pytest tests/test_graph_snapshot.py tests/test_graph_cli.py -q` → `ERROR tests/test_graph_snapshot.py` / `ModuleNotFoundError: No module named 'kgdb'` / `1 error in 0.44s` (collection).
- `python -m deskops graph build --root .` → `Error: KGDB graph snapshot validation is unavailable; install kgdb before running 'deskops graph build'.`, exit 1.
- Both pass after the change.

## Wrong or ambiguous things found

- No line numbers had moved.
- `test_graph_cli.py:165` did not actually simulate kgdb being absent; it monkeypatched `write_graph_snapshot` to raise. Rewritten to exercise the real `_validate_graph_snapshot` import path by putting `None` in `sys.modules`.
- sldb's `snapshot_load` is a thin wrapper over `load_graph`, which branches on top-level `nodes` without `edges`/`links` and validates the current snapshot natively. Verified by the green snapshot/graph tests and `graph build`.
- No sldb bug found; no sldb changes made.
- Note: `deskops graph build --root .` writes only gitignored `.sldb/runtime/graphs/` files; `git status` shows only the intended eight modified files plus the new correction note.
