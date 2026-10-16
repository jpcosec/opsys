RESTATEMENT:

1. Confirm `deskops/operations.py` contains `DRAWER_INDEX_FILES` (~549), `resolve_drawer_source` (~551), `attach_drawer_source` (~583), and read `deskops/cli/commands/promote.py` for `PromoteCLI`, `_inbox_to_drawer_task`, `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`.
2. Confirm `deskops.doc_io` (from dependency task-rw-f2) and `deskops.desk_paths` modules exist and their public surface.
3. Create `deskops/services/__init__.py` (package init) and `deskops/services/drawer.py`.
4. Define `class DrawerService` in `deskops/services/drawer.py` with `__init__(self, root: Path)`, storing `root`; import `deskops.desk_paths` and `deskops.doc_io` as modules (not classes).
5. Move `DRAWER_INDEX_FILES` into the service module; move bodies of `resolve_drawer_source` and `attach_drawer_source` into service methods; route drawer reads/writes through `deskops.doc_io`.
6. Move `_inbox_to_drawer_task` logic (minus printing), `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug` from `promote.py` into `DrawerService` methods, preserving behavior.
7. In `DeskopsOperations.__init__`, add lazy construction of `DrawerService(self.root)` (property/cached attribute) using `deskops.desk_paths` for root.
8. Replace `resolve_drawer_source` and `attach_drawer_source` bodies in `operations.py` with one-line wrappers delegating to the service.
9. In `promote.py`, keep `PromoteCLI.run` in the CLI; have it call `DrawerService` methods and print the returned values; leave no moved helper logic in the CLI.
10. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py` unmodified.
11. Run `pytest tests`.
12. Verify Done When: `def resolve_drawer_source` in `deskops/operations.py` is a one-line wrapper, and `grep -n DrawerService deskops/cli/commands/promote.py` matches.
13. Do not commit; hand the diff to the supervisor.

AMBIGUITIES:

1. `DRAWER_INDEX_FILES` is a module-level constant, not a method; task says "moving those members" but the class-based pattern and Done When only cover methods. Whether it stays in `operations.py` (re-exported), moves to `services/drawer.py` as a module constant, or becomes a `DrawerService` attribute is unspecified.
2. Done When names only `resolve_drawer_source` as a one-line wrapper; whether `attach_drawer_source` (and any other member) must also be a one-line wrapper is not stated.
3. "lazily" is unspecified: no mechanism (property, `cached_property`, nullable attr), and the accessor name/attribute convention is not given.
4. "each service is a class constructed with `root: Path` that uses `deskops.desk_paths` and `deskops.doc_io` as modules" — whether service methods must keep the exact old signatures/bodies unchanged or may be reshaped (and whether signatures matter for the wrappers) is unclear.
5. `_inbox_to_drawer_task` "minus its printing": the split between returned value and printed output, and the return type `PromoteCLI.run` prints, are not specified.
6. Behavior of `_read_markdown` vs `deskops.doc_io` read API is unspecified — whether it should be replaced by `doc_io` or moved as-is.
7. Dependency `task-rw-f2-transactional-doc-io` is not confirmed complete; if `deskops/doc_io` does not exist, the required imports cannot be made.
8. No requirement is stated for exporting/registering `DrawerService` from `deskops/services/__init__.py`.
9. No statement of which tests (or new tests) directly exercise `DrawerService`; "pass unmodified" is the only oracle.
10. The named test files' existence is assumed, not verified by the task text.
11. Scope says "with unchanged behavior" but does not state whether `deskops/operations.py`'s public API (imports by other modules) must remain intact beyond those two methods.
