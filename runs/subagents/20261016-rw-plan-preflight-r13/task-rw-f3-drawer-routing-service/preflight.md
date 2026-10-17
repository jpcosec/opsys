RESTATEMENT:
1. Read `deskops/operations.py` around lines 491–540 to capture `DRAWER_INDEX_FILES`, `resolve_drawer_source`, `attach_drawer_source`; read `deskops/cli/commands/promote.py` to capture `PromoteCLI` and helpers `_inbox_to_drawer_task`, `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`.
2. `grep -rn` the repo for importers/callers of those names to find any non-promote consumers.
3. Create `deskops/services/__init__.py`.
4. Create `deskops/services/drawer.py` with `class DrawerService`, `__init__(self, root: Path)`, using `deskops.desk_paths` and `deskops.doc_io` as modules.
5. Move `DRAWER_INDEX_FILES`, `resolve_drawer_source`, `attach_drawer_source` bodies into `DrawerService`.
6. Move the six promote helpers into `DrawerService`; strip printing from `_inbox_to_drawer_task` and return data instead.
7. In `DeskopsOperations.__init__`, lazily construct `DrawerService`; replace old members with one-line delegating wrappers.
8. In `promote.py`, keep `PromoteCLI.run`; have it obtain `DrawerService` and print what the service returns; leave remaining wrappers/delegation.
9. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py`.
10. Run `pytest tests`.
11. Confirm Done When: `resolve_drawer_source` in `operations.py` is a one-line wrapper; `grep -n DrawerService deskops/cli/commands/promote.py` matches; named tests pass unmodified.

AMBIGUITIES:
1. "Builds it lazily" is unspecified: cached property, `functools.cached_property`, or construct-on-first-call `if self._drawer is None`. No pattern named.
2. `deskops/services/__init__.py` contents undefined (empty vs re-export `DrawerService`).
3. `_inbox_to_drawer_task` "minus its printing" — the return shape is unspecified: path, result object, tuple, or None. Cannot know what `PromoteCLI.run` should print.
4. No acceptance criterion covers `attach_drawer_source` or `DRAWER_INDEX_FILES` wrappers; unclear whether those must remain as delegating wrappers in `operations.py`.
5. External callers of the moved names/helpers are not listed; unclear whether to add backwards-compat shims in `operations.py`/`promote.py` for other modules.
6. `grep -n DrawerService deskops/cli/commands/promote.py` — "matches" is undefined (import-only vs method call vs construction).
7. No spec for whether `PromoteCLI` constructs `DrawerService` itself or receives it from `DeskopsOperations`; no spec for how `PromoteCLI` obtains `root`.
8. `root: Path` — unclear if resolved/absolute, and whether it equals `DeskopsOperations`'s existing root attribute and its type.
9. Method vs module-level function design on `DrawerService` is unspecified (do the moved helpers become private methods, module functions, or stay free functions?).
10. Whether to add direct `DrawerService` unit tests is not stated; only pre-existing tests are named, so no new-test requirement.
11. `depends_on: task-rw-f2-transactional-doc-io` status is unknown; if incomplete, `deskops.doc_io` module may not exist or have the assumed API.
12. Type annotations/signatures to preserve on wrappers and service methods are unspecified.
13. Task `status: deferred` and status transition are not restated in the task body; only the Resolved Decision covers promotion timing.
14. `runs/planning/deskops-rewrite-inventory.md` is referenced but not listed in `files` or `Selected Source Documents`; availability/needed extent unclear.
