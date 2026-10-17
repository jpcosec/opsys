# result-summary: task-rw-f0-reject-ambiguous-selectors

## Changes

- `deskops/operations.py` — `DeskopsOperations._resolve_glob` (now lines 2085-2097): after the exact-match check and the empty-matches `FileNotFoundError`, raises
  `ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`
  when `len(matches) > 1`. Exact file names and single prefix matches resolve unchanged.
- `tests/test_operational.py`
  - Added top-of-file imports: `json`, and `_cli`, `_make_repo` from `tests.test_lifecycle_end_to_end`.
  - Added helper `_seed_task(root, task_id, title)` that creates a task through the real CLI with an explicit id.
  - Added `test_advance_task_prefix_selector_rejects_ambiguity`: `task-foo-bar` + `task-foo-baz`, no `task-foo`; `advance task task-foo` exits 1, stderr names both stems, both files byte-identical before/after.
  - Added `test_advance_task_exact_selector_wins_over_prefix`: `task-foo` + `task-foo-bar`; `advance task task-foo` exits 0, stdout contains `Task: task-foo`, `task-foo-bar.md` unchanged.

No CLI change was needed: `deskops.cli.main.main` already maps `ValueError` to `Invalid value: ...` on stderr with exit 1.

## Validation (all with PYTHONPATH=/tmp/rw/wt/ambiguous)

| Command | Final line |
|---|---|
| `pytest tests/test_operational.py` | `10 passed in 14.26s` |
| `pytest tests` | `339 passed, 3 skipped in 212.25s (0:03:32)` |
| targeted new tests (pre-fix) | `1 failed, 1 passed, 8 deselected` |
| targeted new tests (post-fix) | `2 passed, 8 deselected` |

Test against unfixed code: `test_advance_task_prefix_selector_rejects_ambiguity` failed with `assert 0 == 1` because the old resolver silently advanced `task-foo-bar` (stdout `Task: task-foo-bar`, rc 0). `test_advance_task_exact_selector_wins_over_prefix` passed pre-fix as expected.

Manual sandbox check (fresh repo under /tmp, repo `desk/` untouched):

```
$ python -m deskops advance task task-foo
Invalid value: Ambiguous id 'task-foo' in /tmp/f0check/repo/desk/tasks: task-foo-bar, task-foo-baz
rc=1
```

## Task discrepancies / ambiguities

- Cited line numbers moved: `_resolve_glob` is at 2085 (task says 2077-2084); callers are at 674, 955, 1972 (task said 1964 for the last). Same functions (`_lifecycle_gates`, `advance_task`, `_resolve_task_payload`).
- Test imports use `from tests.test_lifecycle_end_to_end import ...`; `tests/` has no `__init__.py`, but it resolves as an implicit namespace package because `pythonpath = ["."]` puts the repo root on `sys.path`.
- No issues found in sldb; no files in sldb were touched.

## Worktree state

Modified only: `deskops/operations.py`, `tests/test_operational.py`. No commits, no staging, no desk/ mutations.
