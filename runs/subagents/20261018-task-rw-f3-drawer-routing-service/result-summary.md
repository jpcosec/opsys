# task-rw-f3-drawer-routing-service — execution summary

## Changes

- **New `deskops/services/__init__.py`** — package docstring establishing the service pattern (class constructed with `root: Path`, path/store work via `deskops.desk_paths` / `deskops.doc_io`).
- **New `deskops/services/drawer.py`** — `DrawerService(root)`:
  - `DRAWER_INDEX_FILES` (class constant, moved from `DeskopsOperations`).
  - `resolve_drawer_source(selector)` — body moved verbatim (same path/exact/substring/ambiguity rules).
  - `attach_drawer_source(payload, drawer_file)` — moved verbatim.
  - `promote_inbox_to_drawer_task(selector, title_override=None) -> DrawerPromotion` — orchestration of `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`, `_untrack_note`, with all printing removed.
  - `_untrack_note(transaction, source)` now calls `transaction.untrack(source.stem)`; `transaction.record(target)` and `transaction.record(source)` (via untrack) give rollback coverage for the drawer file and the deleted note. The `try/except` best-effort behavior and warning text are unchanged; `source.unlink(missing_ok=True)` still runs even when untracking fails.
  - `DrawerPromotion(exit_code, messages)` dataclass carries what the CLI prints.
- **`deskops/operations.py`**:
  - Removed the three drawer members; `resolve_drawer_source` is now a one-line body delegating to `self.drawer.drawer.resolve_drawer_source` (and `attach_drawer_source` likewise).
  - Added lazy `drawer` property (imports `DrawerService` inside the property to avoid an import cycle with `parse_task_sections`) and `self._drawer = None` in `__init__`; `TYPE_CHECKING` import for the annotation.
- **`deskops/cli/commands/promote.py`**: `PromoteCLI` reduced to `run`, which constructs `DrawerService(root)`, prints `result.messages` in order, and returns `result.exit_code`. All helpers moved; now-unused imports (`re`, `yaml`, `doc_io`, `parse_task_sections`) removed.

## Task text vs. real code

- The cited line numbers (491/493/525) were stale; members were at `deskops/operations.py:469` (`DRAWER_INDEX_FILES`), `:471` (`resolve_drawer_source`), `:503` (`attach_drawer_source`) before the edit.
- Docs of `attach_drawer_source` use `self.desk_root.parent.resolve()`; in the service this is `self.root.resolve()` (identical, root is resolved in `__init__`).

## Validation

All commands run from `/tmp/rw/wt/drawersvc`.

- `PYTHONPATH=/tmp/rw/wt/drawersvc python -m pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py -q`
  - `29 passed in 6.71s`
- `PYTHONPATH=/tmp/rw/wt/drawersvc python -m pytest tests -q`
  - `395 passed, 3 skipped in 315.59s (0:05:15)`
- `PYTHONPATH=/tmp/rw/wt/drawersvc python -m deskops --help` — exit 0.
- Sandbox smoke (`desk install` + `promote inbox-to-drawer-task` in `mktemp -d`): exit 0, output order unchanged (`Created drawer task candidate …`, `Deleted source file …`, `Path: …`).
- Done-When checks:
  - `grep -n "def resolve_drawer_source" -A 2 deskops/operations.py` → wrapper at 481-482.
  - `grep -n "DrawerService(" deskops/cli/commands/promote.py` → line 24, inside `PromoteCLI.run`.

## Baseline (unfixed code)

- `git stash push -u` then the three named test files: `29 passed in 6.65s`; stash restored. These tests are green both before and after, as expected for a behavior-preserving refactor (no pre-existing failure reproduces the change).

## Ambiguities / deviations

- The service pattern says services use `deskops.desk_paths` and `deskops.doc_io` as modules, but `deskops/services/drawer.py` imports only `doc_io`: drawer lookup deliberately uses exact name/stem then substring-of-stem matching, which `desk_paths.resolve_selector` (exact then prefix/startswith) cannot express without changing behavior, which the task forbids. No unused `desk_paths` import was added.
- `_untrack_note` gained a `transaction` parameter (was `(root, source)`); external behavior and message text are unchanged. `_inbox_to_drawer_task`'s printing became a structured `DrawerPromotion` returned to `PromoteCLI.run`.
- `PromoteCLI`'s private helpers no longer exist as attributes of the CLI; no test or caller referenced them.
- No sldb bug encountered.
