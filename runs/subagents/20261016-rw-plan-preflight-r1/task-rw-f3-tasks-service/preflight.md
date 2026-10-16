RESTATEMENT:
1. Verify dependency `task-rw-f3-closeout-gates-service` is closed before starting.
2. Read pills `desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md` and `desk/contexts/pill-007-phase-gated-task-flow.md`.
3. Inspect `deskops/operations.py` lines 154-208 and 2904-2910 for `_read_doc(TaskDoc)` and its regex section parser layered over `extract_model_data`.
4. Inspect `deskops/operations.py` lines 1068-1183 for `parse_*_input`.
5. Write a test that enumerates every TaskDoc in the repo (`desk/tasks/`, `desk/drawer/tasks/`, related dirs) and every TaskDoc in `tests/fixtures`, runs the current regex overlay and `extract_model_data`, and asserts identical output.
6. For each divergence, fix the source TaskDoc or its SLDB template (not the regex).
7. Create `deskops/services/tasks.py` owning create/advance/next for tasks; TaskDoc read only via sldb extraction.
8. Move `parse_*_input` into `deskops/cli/` (per file list, `deskops/cli/commands/operations.py`).
9. Delete the regex section overlay.
10. Update `deskops/operations.py` and `deskops/cli/commands/operations.py` imports/call sites.
11. Run `pytest`.
12. Run `deskops list tasks --root .`.
13. Run `deskops show task task-write-end-to-end-deskops-operator-manual --root .`.
14. Confirm no regex section parser remains for TaskDoc and suite passes.

AMBIGUITIES:
1. Task `status: deferred` and `depends_on` an unstarted task — start condition unspecified.
2. No function signatures, names, return types, or error contract for the new service's create/advance/next.
3. "create/advance/next" not mapped to existing operations.py functions or line numbers.
4. Scope of overlay deletion unclear: only `TaskDoc` path, or the shared `_read_doc` regex for all doc types.
5. Target module for `parse_*_input` ambiguous: file list names `deskops/cli/commands/operations.py`, but text says "deskops/cli/" (directory); new module allowed?
6. No path/name specified for the divergence test.
7. No rule for choosing "fix the doc" vs "fix the template" per divergence.
8. Existing tests asserting current regex behavior: update, delete, or leave unspecified.
9. No acceptance criteria for CLI-layer parse behavior parity (exit codes, messages, output format).
10. Validation command `deskops show task task-write-end-to-end-deskops-operator-manual` may be a nonexistent id (drawer uses `task-write-end-to-end-operator-manual`); no fallback given.
11. Pill bindings listed without stating which clauses apply or how compliance is verified.
12. No commit step in the task doc, though repo convention requires an atomic commit per closed task.
13. Circular-import direction between `operations.py` and the new service not specified.
14. "No regex section parser remains for TaskDoc" is the only done-when; no threshold for coverage of the comparison test or handling of docs that cannot be fixed.
