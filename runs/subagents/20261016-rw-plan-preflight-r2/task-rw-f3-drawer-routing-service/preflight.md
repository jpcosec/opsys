RESTATEMENT:

1. Open `deskops/operations.py` and read the drawer members: `DRAWER_INDEX_FILES` (~549), `resolve_drawer_source` (~551), `attach_drawer_source` (~583), plus `DeskopsOperations.__init__`.
2. Open `deskops/cli/commands/promote.py` and read `PromoteCLI`; separate CLI-facing code from the inbox-to-drawer promotion logic.
3. Create `deskops/services/__init__.py` (new package).
4. Create `deskops/services/drawer.py` defining `class DrawerService` with `__init__(self, root: Path)`, importing `deskops.desk_paths` and `deskops.doc_io` as modules.
5. Move drawer lookup logic into `DrawerService`: `DRAWER_INDEX_FILES`, `resolve_drawer_source`, `attach_drawer_source` as members/methods.
6. Move the non-CLI logic of `PromoteCLI` into `DrawerService` (promotion logic only).
7. In `deskops/operations.py`, have `DeskopsOperations` construct `DrawerService` lazily; replace old drawer members with one-line wrappers that delegate to it.
8. In `deskops/cli/commands/promote.py`, make `PromoteCLI` delegate to `DrawerService`; leave CLI surface intact.
9. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py` with tests unmodified.
10. Run `pytest tests`.
11. Run `grep -n 'def resolve_drawer_source' deskops/operations.py` and confirm only a wrapper remains.
12. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:

1. `depends_on: task-rw-f2-transactional-doc-io` — its completion status is unknown; cannot confirm prerequisites are met.
2. Contradiction: "`DeskopsOperations.__init__` builds it lazily" — lazy construction is not normally in `__init__`; cache-vs-eager mechanism unspecified.
3. `DRAWER_INDEX_FILES` is a module constant, not a method; no defined form for its "one-line wrapper" in `operations.py`.
4. "non-CLI logic of `PromoteCLI`" boundary is undefined; no list of methods/functions to move.
5. "uses `deskops.desk_paths` and `deskops.doc_io` as modules" — semantics unclear (module-level imports vs injection); whether other imports are permitted.
6. `deskops/services/__init__.py` contents unspecified (empty vs exporting `DrawerService`).
7. "shows only a wrapper" — wrapper shape and signature-preservation expectations undefined.
8. Test baseline unknown: whether the three named tests currently pass and whether tasks f1/f2 exist in this branch.
9. No acceptance criteria for `promote.py` delegation beyond the word "delegate".
10. "unchanged behavior" — whether a pure move is required or edits are allowed is not stated.
11. `references: []` and no `--run-dir` given; closeout run dir for `deskops closeout commit` is unknown.
12. Task `status: deferred` — whether an executor should execute now is not stated.
13. No failure/rollback guidance if named tests or full suite fail.
