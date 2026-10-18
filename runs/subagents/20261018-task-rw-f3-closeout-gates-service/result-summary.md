# Result summary — task-rw-f3-closeout-gates-service

## What changed

- **New `deskops/services/closeout_gates.py`**
  - `class CloseoutGatesService(root)`.
  - `closeout_reference_evidence(payload, *, points_to_atom, points_to_routed_follow_up)` — moved from `DeskopsOperations`; atom and routed-follow-up classification stay in `operations.py` (they were not in the move list) and are injected as callables.
  - `reference_points_to_test(reference)` — accepts a non-absolute `.py` file that resolves inside `<root>/tests/`, optionally with `::node` (node not validated) and the `pytest <path> [-flags]` form; absolute paths and `..` escapes rejected.
  - `reference_points_to_commit(reference)` — requires `re.fullmatch(r"[0-9a-f]{7,40}")`, resolves with `git rev-parse --verify <ref>^{commit}`, then requires the resolved full SHA to pass `git merge-base --is-ancestor <sha> HEAD`.
  - `build_closeout_graph_context()` — moved unchanged from `operations.py`.
  - `_test_path_candidates()` — preserves the existing `pytest ...` token extraction.

- **`deskops/operations.py`**
  - Added `TYPE_CHECKING` import, `_closeout_gates` field, and `closeout_gates` cached property.
  - Replaced bodies of `_closeout_reference_evidence`, `_reference_points_to_test`, `_reference_points_to_commit`, `_build_closeout_graph_context` with delegating wrappers (private names preserved).
  - No behavior change outside the two gates.

- **`tests/test_closeout.py`**
  - `test_closeout_verify_rejects_loose_commit_and_test_references`: `HEAD`, `main`, `deskops/x.py`, absolute existing test path, and `tests/../deskops/x.py` contribute no evidence; a real ancestor SHA is accepted.
  - `test_closeout_verify_accepts_ancestor_commit_and_test_node`: ancestor SHA and `pytest tests/test_x.py::test_y` are accepted and `report["ok"]` is true.

## Validation commands and final lines

1. `PYTHONPATH=/tmp/rw/wt/gates python -m pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py -q`
   - `24 passed in 35.73s`
2. `PYTHONPATH=/tmp/rw/wt/gates python -m pytest tests -q`
   - `397 passed, 3 skipped in 336.29s (0:05:36)`

## Test run against unfixed code

- Ran the two new tests before implementing (targeted `-k "rejects_loose or accepts_ancestor"`).
- `test_closeout_verify_rejects_loose_commit_and_test_references` failed on the original code: `assert rc == 1` → `assert 0 == 1` (loose references passed verification), confirming finding X6.
- `test_closeout_verify_accepts_ancestor_commit_and_test_node` passed on the original code, as expected (that behavior already worked).

## Task text issues / ambiguities

- Cited line numbers were stale (after F2): actual pre-edit locations were `_reference_points_to_test` at `deskops/operations.py:1787`, `_reference_points_to_commit` at 1808, `_build_closeout_graph_context` at 1824, `_closeout_reference_evidence` at 1207. Located with grep.
- Implementation Path step 3 says only "split off `::...`", but existing tests and task references use the `pytest tests/...::node` form. Kept the existing `pytest`-prefix candidate extraction so those references remain accepted.
- `_closeout_reference_evidence` also classifies atom and routed follow-up references, whose predicates were not in the move list. They remain in `operations.py` and are passed into the service, so the moved set matches the task exactly.
- No sldb bug observed.
