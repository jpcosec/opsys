RESTATEMENT:

1. Confirm prerequisite `task-rw-f3-drawer-routing-service` is closed and the drawer task has been promoted to `desk/tasks/` (supervisor does promotion + commit).
2. Read `deskops/operations.py` and `deskops/services/` (especially the drawer-routing service) to mirror its established service pattern.
3. Verify each dead item with `grep -rn '<name>' deskops tests`: `_default_*_payloads` (lines 1296-1487), `PRIMITIVE_DIRS`, and the duplicate `_setup_logging`; capture outputs for closeout.
4. Determine which of the two `_setup_logging` definitions the entrypoint calls and keep that one.
5. Delete `_default_*_payloads`, `PRIMITIVE_DIRS`, and the non-entrypoint `_setup_logging`.
6. Create `deskops/services/primitives.py` with `PrimitivesService(root)`, carrying `root` and `desk_root` itself.
7. Move into the service as methods (same params minus `self` state): `PRIMITIVE_KINDS`, `create_primitive`, `list_primitives`, `show_primitive`, `parse_primitive_input`, `_normalize_primitive_payload`, `_primitive_path`.
8. Add one-line delegation wrappers on `DeskopsOperations` for each moved helper so `deskops/cli/commands/operations.py` and `tests/test_operational.py` keep working.
9. Do not touch `deskops/specs/mermaid.py` or `deskops/materializers/atoms.py`; do not touch `RunDoc` or the self-reflection ledger.
10. Run `pytest tests`; run `python -m deskops next --diagram`.
11. Verify: `deskops/services/primitives.py` exists, `grep -n '_default_.*_payloads\|PRIMITIVE_DIRS' deskops` is empty, `_setup_logging` defined once, pytest green.
12. Hand diff to supervisor; supervisor makes the closeout commit.

AMBIGUITIES:

1. Task `status: deferred` — no stated trigger or confirmation that the depends_on task is actually closed, so whether this task is executable now is unverifiable from the document alone.
2. Which of the two `_setup_logging` definitions the entrypoint calls is not stated; I would have to inspect the entrypoint to decide, with no listed criteria if both are reachable.
3. Service shape is underspecified: `__init__(root)` but `desk_root` is also "carried" — unclear whether `desk_root` is derived from `root`, passed separately, or a second constructor parameter.
4. "Same parameters minus `self` state" is ambiguous about whether the original functions were module-level (taking `root`/`desk_root`) or methods, and whether service methods drop those params entirely.
5. No list of callers of the helpers, so I cannot tell which names must survive as wrappers versus which are fully private (e.g., do tests call `_normalize_primitive_payload` or `_primitive_path` directly?).
6. Wrapper signature requirements are unstated: must wrappers keep exact names, visibility (leading underscore preserved?), and positional/keyword signatures?
7. Deletion order vs. stated line numbers is unspecified; if I delete first, lines 1296-1487 shift, making the given coordinates unusable as verification anchors.
8. `PRIMITIVE_DIRS` has no line number and no description; whether its only occurrence is its definition (making grep ambiguous) is unresolved.
9. The dead-code grep scope is `deskops tests`, but the final acceptance grep scope is `deskops` only; whether `desk/`, docs, or other repos must be checked is unclear.
10. No instruction on whether the moved service needs its own tests, or whether existing coverage in `tests/test_operational.py` suffices.
11. No stated handling for imports/attributes left unused in `deskops/operations.py` after the move (e.g., whether to prune now-unused imports or leave them).
12. "One-line wrappers so callers keep working" gives no acceptance check that wrappers actually delegate rather than duplicate logic.
13. Validation lists `python -m deskops next --diagram` but states no expected output, so pass/fail for that command is undefined.
14. `_default_*_payloads` is a glob; the exact set of methods and their boundaries (does it include names outside that prefix?) is not enumerated.
