# task-rw-f0-graph-missing-ignores-archived-records — executor summary

## What changed

- `deskops/graph/extract_edges.py`
  - Added `record: bool | None = None` to `DeclaredGraphEdge` and `MissingGraphTarget`.
  - Added `_is_record_document(text)`; it reads `record: true` from frontmatter on every extracted document (not only `desk/drawer/`).
  - `extract_declared_edges` sets `record=True` on missing targets and edges from record documents (else `None`).
  - `to_dict` on both dataclasses now drops `None`, so live findings keep today’s dict shape.
- `deskops/graph/checks.py`
  - Added `record: bool | None = None` to `GraphMissingFinding`.
  - `_finding_from_missing_target` copies `missing.record`; `to_dict` already drops `None`.
- `deskops/cli/main.py`
  - `_graph_missing` splits findings into `failing` and `informational`; prints `Missing graph references:` first, `Informational (archived records):` second, then `N missing, M informational`; exits 1 iff a non-record finding exists.
  - Added `_print_graph_missing_finding` shared by both sections.
- `desk/drawer/issues/diagnosis-archive.md`
- `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`
- `desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md`
  - Added `record: true` frontmatter.
- `tests/test_graph_declared_edges.py`
  - Added `test_live_issue_with_a_dangling_path_still_fails`.
  - Added `test_record_issue_with_the_same_dangling_path_is_informational`.

## Validation

- `PYTHONPATH=/tmp/rw/wt/gmissing python -m pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py -q`
  - `28 passed in 2.09s`
- `PYTHONPATH=/tmp/rw/wt/gmissing python -m deskops graph missing --root .`
  - Exit: **1**
  - Final line: `13 missing, 102 informational`
  - The 102 informational findings are exactly the three archived records: 98 `diagnosis-archive.md`, 3 `issue-session-20260910...`, 1 `issue-refactor-primitives...`.
  - The 13 non-record findings are pre-existing and outside the task scope; they are NOT hidden:
    - `task-rw-ci-tests-workflow-and-changelog` -> `desk/inbox/20261017-233236-...md` (1; file exists but is not a graph node)
    - `task-rw-f0-graph-missing-ignores-archived-records` -> `deskops/runtime/primitives.py` (1; quoted in this task’s Rationale)
    - `task-rw-f1-cli-contract-tests` -> `tests/test_cli_contract.py` (3)
    - `task-rw-f1-model-contract-snapshot` -> `tests/fixtures/model_contract_hashes.json` (2), `tests/test_model_contract_snapshot.py` (3)
    - `task-rw-f1-output-golden-files` -> `tests/test_output_goldens.py` (3)
- `PYTHONPATH=/tmp/rw/wt/gmissing python -m pytest tests -q`
  - `348 passed, 3 skipped in 285.82s (0:04:45)`

## Test against unfixed code

Added the two tests before the implementation; on unfixed code:

```
FAILED tests/test_graph_declared_edges.py::test_live_issue_with_a_dangling_path_still_fails
FAILED tests/test_graph_declared_edges.py::test_record_issue_with_the_same_dangling_path_is_informational
2 failed, 4 passed in 0.44s
```

The record test failed with `AttributeError: 'GraphMissingFinding' object has no attribute 'record'`; the live test failed on the same missing attribute.

## Wrong / ambiguous in the task

- Task cites `deskops/graph/extract_edges.py:93` for the `task`/`issue` scanner; it is at line 96 after the edit (line 93 before). `deskops/cli/main.py:280` for `_graph_missing` is exact.
- Task expects `graph missing --root .` to exit 0 with 102 findings, but this worktree is 3 commits ahead of the cited `56f49d5` (`5f86dd5`, `c1dd728` promoted F1/CI task docs). Those live draft task docs add 13 non-record `missing_declared_target` findings. Marking them as records would hide live work, which the task explicitly forbids (“list them in the closeout and do not hide them”). Exit 0 is therefore not achievable without hiding out-of-scope findings.
- The `task-rw-ci...` finding points at an existing inbox file; it is still “missing” because inbox documents are not graph nodes. That is existing behavior, not changed here.

## SLDB

No SLDB bug encountered; no SLDB files changed.
