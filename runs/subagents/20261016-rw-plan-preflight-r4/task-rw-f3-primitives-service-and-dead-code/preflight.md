RESTATEMENT:

1. Create branch/worktree state as-is; do not commit.
2. Grep to confirm dead code and capture exact names/line numbers: `grep -rn '_default_' deskops tests`, `grep -rn 'PRIMITIVE_DIRS' deskops tests`, `grep -rn '_setup_logging' deskops tests`.
3. Identify exact `_default_*_payloads` method names from grep output (task gives only lines 1296-1487, not names).
4. Delete the `_default_*_payloads` methods, delete `PRIMITIVE_DIRS`, and delete one of the two `_setup_logging` definitions — keeping the one with live callers (verify via grep of callers first).
5. Create `deskops/services/primitives.py` defining `PrimitivesService(root)` that stores `root` and derives/stores `desk_root`.
6. Move `create_primitive` (462), `list_primitives` (729), `show_primitive` (1012), `parse_primitive_input` (1115), `_normalize_primitive_payload` (1218), `_primitive_path` (2609) into `PrimitivesService` as methods, keeping identical parameters (only `self` differs).
7. Handle `PRIMITIVE_KINDS` (68): expose it via the service (constant or attribute) rather than as a free module constant.
8. Re-route collaborator calls from the moved methods to `deskops.doc_io`, `deskops.desk_paths`, or a shared helper module: `ensure_workspace`, `_write_new_doc`, `_read_doc`, `_resolve_glob`, `_coerce_list`.
9. In `DeskopsOperations`, add one-line delegating wrappers for the moved helpers so existing callers keep working.
10. Update `tests/test_operational.py:37` monkeypatch of `operations._write_doc` to patch the `doc_io` function the service now calls, preserving the rollback assertion.
11. Run `pytest tests`.
12. Run `python -m deskops next --diagram`.
13. Record the grep outputs as dead-code proof.
14. Confirm Done When: file exists, `grep -n '_default_.*_payloads\|PRIMITIVE_DIRS' deskops` empty, `_setup_logging` defined once, tests green.

AMBIGUITIES:

1. `_default_*_payloads` is given only as a wildcard and a line range; exact method names, count, and boundaries are not specified.
2. "`PRIMITIVE_KINDS` (68)" is a module-level constant, but the task says the helpers are "instance methods today, so only `self` changes" — contradiction for this item; no instruction on whether it becomes a class attribute or module constant.
3. Which of `deskops.doc_io`, `deskops.desk_paths`, or "a shared helper module" each of `ensure_workspace`, `_write_new_doc`, `_read_doc`, `_resolve_glob`, `_coerce_list` maps to is unspecified.
4. The test patch is described as `operations._write_doc`, but the moved-collaborator list contains `_write_new_doc`, not `_write_doc` — unclear which symbol the test patches.
5. "follow the pattern set by task-rw-f3-drawer-routing-service" is not executable without that task's content, which is not provided.
6. It is not stated how `desk_root` is derived from `root` inside `PrimitivesService`.
7. "one-line wrappers" — whether they must preserve exact signatures/`self`, and how a wrapper works for the `PRIMITIVE_KINDS` constant, is unspecified.
8. "keep the `_setup_logging` definition that the entrypoint calls" — the entrypoint is not named.
9. "record ... in the closeout as proof" conflicts with Resolved Decisions stating the executor does not commit; where the executor records proof (no `--run-dir` given) is unclear.
10. Whether `python -m deskops next --diagram` must produce specific output or just run without error is not specified.
