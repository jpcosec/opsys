# task-rw-f2-selector-resolution-module — result

## What changed

- **`deskops/desk_paths.py` (new)**
  - `resolve_selector(desk_root, directories, selector, pattern, what, recursive) -> Path`
  - Tier 1: exact `name` or `stem` match; Tier 2: unique name/stem prefix match.
  - Zero matches -> `FileNotFoundError("No <what> file found for selector '<selector>'")`.
  - Multiple matches -> `ValueError("Ambiguous <what> selector '<selector>': <paths>")`, paths relative to `desk_root`, sorted, joined with `, `.
  - Rejects empty/whitespace-only selectors with the existing `Empty or whitespace-only selector provided for <what>` message.
  - `recursive` selects `rglob` vs `glob`; missing directories are skipped; duplicate candidate paths are deduped.
- **`deskops/operations.py`**
  - Added `from deskops.desk_paths import resolve_selector`.
  - `_resolve_glob` -> one-line delegation (`pattern=f"{doc_id}*.md"`, `what="task"`, `recursive=False`).
  - `_resolve_artifact_selector_multi` -> one-line delegation (`recursive=True`).
  - `_resolve_artifact_selector` -> one-line delegation (`recursive=True`).
  - Removed `_one_artifact_match`, whose only callers were `_resolve_artifact_selector`. Its signature (matches list, no selector/pattern) cannot delegate, and it became dead code.
- **`tests/test_desk_paths.py` (new)** — 10 tests: exact name, exact stem, unique prefix, recursive opt-in, zero matches, exact ambiguity ordering/format, prefix ambiguity, multi-directory candidates, missing directories, empty selector.

No existing test asserted the old wordings, so none needed updating:
- `tests/test_cli.py` asserts only prefixes such as `Ambiguous artifact.atom selector '...'` and `Empty or whitespace-only`, which still pass.
- `tests/test_cli.py::test_promote_rejects_ambiguous_inbox_selector` targets `deskops/cli/commands/promote.py`, outside the four resolvers.

## Validation

Commands run from `/tmp/rw/wt/selector` with the worktree pinned on `PYTHONPATH`:

```
PYTHONPATH=/tmp/rw/wt/selector python -m pytest tests/test_desk_paths.py -q
10 passed in 0.02s

PYTHONPATH=/tmp/rw/wt/selector python -m pytest tests -q
379 passed, 3 skipped in 315.67s (0:05:15)
```

Additional targeted run before the full suite:

```
PYTHONPATH=/tmp/rw/wt/selector python -m pytest tests/test_cli.py tests/test_operational.py tests/test_add_task_from_drawer.py tests/test_inbox_promote_cli_gaps.py tests/test_cli_contract.py -q
120 passed in 56.59s
```

`grep -n 'glob(\|rglob(' deskops/operations.py` now shows only unrelated listing/scan loops (list_tasks, drawer source search, graph walks); no selector-resolution loop remains outside the delegations.

## Test against unfixed code

Created `tests/test_desk_paths.py` before the module and ran:

```
PYTHONPATH=/tmp/rw/wt/selector python -m pytest tests/test_desk_paths.py -q
ERROR tests/test_desk_paths.py
E   ModuleNotFoundError: No module named 'deskops.desk_paths'
1 error in 0.07s
```

## Task issues / ambiguities encountered

- Cited line numbers had moved: `_resolve_glob` was at 2144 (not 2077), `_resolve_artifact_selector_multi` at 2157, `_resolve_artifact_selector` at 2183, `_one_artifact_match` at 2274. Used the real locations.
- The task calls `_one_artifact_match` the fourth method and says all four become one-line delegations, but its signature cannot delegate to `resolve_selector` (it receives an already-computed match list). It was dead after the refactor and was deleted.
- The empty-selector guard moved into `resolve_selector`, so `_resolve_glob` now rejects empty selectors too. No `_resolve_glob` caller can pass empty (task ids come from documents), so observable behavior is unchanged.
- The old `_one_artifact_match` ambiguity message included `in <directory>`; per the task's single message format, that suffix is gone.
- `dict.fromkeys` dedupes candidate paths when the same directory is passed twice. Not exercised by current callers.

## sldb

No sldb bug observed; no sldb files touched.
