RESTATEMENT:

1. Confirm `task-rw-f2-transactional-doc-io` is closed and `deskops/doc_io.py` exists; read `deskops/operations.py` around lines 491/493/525 and `deskops/cli/commands/promote.py` in full.
2. Create `deskops/services/__init__.py` (package marker; contents per repo convention).
3. Create `deskops/services/drawer.py` with `class DrawerService`, `__init__(self, root: Path)`, importing `deskops.desk_paths` and `deskops.doc_io` as modules.
4. Move `DRAWER_INDEX_FILES` from `operations.py` into `deskops/services/drawer.py` (keep the name/contents unchanged).
5. Implement `DrawerService.resolve_drawer_source(...)` and `DrawerService.attach_drawer_source(...)` by pasting the bodies from `operations.py` unchanged, adding `self` and reading `self.root` instead of the operations instance/root.
6. Move `PromoteCLI` helpers into the service, unchanged: `_inbox_to_drawer_task` (with all printing stripped), `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`.
7. Rewrite `DeskopsOperations.__init__` to build `self._drawer` (or equivalent) lazily, and change `DeskopsOperations.resolve_drawer_source` and `.attach_drawer_source` into one-line delegating wrappers (and same for any other moved member).
8. In `promote.py`, construct `DrawerService(root)` inside `PromoteCLI.run`, keep `run` in the CLI, and have it unpack the service return value into the existing print calls; delegate the moved helpers (or delete them, per the wrapper rule).
9. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py` with those files unmodified.
10. Run `pytest tests`.
11. Verify: `resolve_drawer_source` in `operations.py` is one line; `grep -n 'DrawerService(' deskops/cli/commands/promote.py` shows a match inside `PromoteCLI.run`.
12. Do not commit; report the diff for supervisor closeout review.

AMBIGUITIES:

1. Whether `PromoteCLI`'s moved helpers are deleted outright or kept as one-line delegating wrappers — Step 2 says "leave wrappers in operations.py and promote.py," but Done When only requires the operations.py wrapper and a `DrawerService(` construction inside `run`.
2. Unclear whether `DRAWER_INDEX_FILES` stays importable from `deskops/operations.py` for existing importers, or moves exclusively.
3. Lazy-construction pattern for the service in `DeskopsOperations` is unspecified (`cached_property`, `None` sentinel, property, etc.).
4. Return type of the service methods (string vs. list of lines vs. structured result) is unspecified, so how `PromoteCLI.run` prints is undetermined.
5. Contents/contract of `deskops/services/__init__.py` are unspecified.
6. Behavior-preservation requirement for helper bodies is stated, but their exact signatures, side effects, exceptions, and any other callers are unknown from the task text.
7. Whether `deskops/doc_io` and `deskops/desk_paths` expose every function the moved helpers need is not stated (depends on unread `task-rw-f2` output).
8. No stated acceptance criterion that the named test files are unchanged apart from "unmodified," and no instruction on what to do if they reference the old private helper locations.
9. Depends_on `task-rw-f2-transactional-doc-io` state is not verifiable from this document; no instruction if it is unclosed.
