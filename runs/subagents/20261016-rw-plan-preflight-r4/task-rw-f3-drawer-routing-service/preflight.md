RESTATEMENT:
1. Read `deskops/operations.py` (around lines 549–600: `DRAWER_INDEX_FILES`, `resolve_drawer_source`, `attach_drawer_source`), `deskops/cli/commands/promote.py` (`PromoteCLI`), `deskops/desk_paths.py`, `deskops/doc_io.py`, and the F1/F2 task outputs for patterns.
2. Create package `deskops/services/__init__.py`.
3. Create `deskops/services/drawer.py` with class `DrawerService(root: Path)`.
4. Move into it: `DRAWER_INDEX_FILES`; `resolve_drawer_source`; `attach_drawer_source`; and the `PromoteCLI` helpers `_inbox_to_drawer_task` (strip its printing), `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug` — behavior unchanged.
5. Have the service import `deskops.desk_paths` and `deskops.doc_io` as modules (no injection).
6. In `operations.py`: add lazy `DrawerService` construction in `DeskopsOperations.__init__` (or first use); reduce `resolve_drawer_source` and `attach_drawer_source` to one-line delegating wrappers; keep `DRAWER_INDEX_FILES` reachable.
7. In `promote.py`: keep `PromoteCLI.run`; route its logic through `DrawerService` and print the value the service returns.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py`, then `pytest tests`, without modifying those tests.
9. Verify Done When: `resolve_drawer_source` in `operations.py` is a one-line wrapper; `grep -n DrawerService deskops/cli/commands/promote.py` matches; named tests pass.

AMBIGUITIES:
1. Placement of helpers `_slug`, `_read_markdown`, `_resolve_unique`: methods on `DrawerService` vs module-level functions in `drawer.py` (or moved to `doc_io`), unspecified.
2. Return contract of `_inbox_to_drawer_task`/service: what type (str, Path, dataclass) `PromoteCLI.run` receives and prints is not defined.
3. Which exact `print` calls inside `_inbox_to_drawer_task` are "its printing" versus logic-like output (e.g. dry-run, warnings) is not enumerated.
4. "Builds it lazily" — no pattern given (property, `functools.cached_property`, on-first-call attribute).
5. Whether `DRAWER_INDEX_FILES` must remain importable from `operations.py` (and its current type) is not stated.
6. `attach_drawer_source`: no description of behavior, return type, or callers; Done When names only `resolve_drawer_source`.
7. `_resolve_unique` semantics/signature unknown; makes the move non-mechanical.
8. `_read_markdown` may be shared with non-drawer code in `promote.py`; scope of removal not specified.
9. Whether `PromoteCLI` stores a `DrawerService` instance, builds per call, or receives it is unspecified.
10. Whether `deskops/services/__init__.py` must export `DrawerService` is not stated.
11. No new tests are required for `DrawerService`; whether internal unit tests are expected is unclear.
12. Dependency `task-rw-f2-transactional-doc-io`: how the service must use its transactional write/doc_io behavior is not specified.
13. Line numbers (549/551/583) and "15 domains" may be stale but are the only locators given.
