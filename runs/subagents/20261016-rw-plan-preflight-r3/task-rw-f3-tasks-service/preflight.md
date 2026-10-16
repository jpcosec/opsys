RESTATEMENT:
1. Add a test under tests/ that, for every TaskDoc found under `desk/` and under `tests/fixtures/`, compares the legacy overlay result (`parse_task_sections` applied on top of `extract_model_data`, per `_read_doc` at deskops/operations.py:2904-2910) against the result of `extract_model_data` alone.
2. Make the test fail (not skip) on any document `extract_model_data` cannot parse, and assert `deskops list tasks` surfaces such documents as malformed.
3. For each divergence, fix the underlying TaskDoc document (not the overlay) until overlay output == `extract_model_data` output.
4. In deskops/operations.py, delete the overlay branch inside `_read_doc` (lines ~2904-2910) so TaskDoc reads use `extract_model_data` only.
5. Move `parse_task_sections` (deskops/operations.py:154-208) and, if it is used solely by `parse_task_sections`, `parse_validation_section`, into deskops/cli/commands/promote.py as private helpers; update promote.py:47 to call the private helper.
6. Move the TaskDoc lifecycle methods (create/advance/next) out of their current home into `deskops/services/tasks.py`.
7. Move the `parse_*_input` functions (deskops/operations.py:1068-1183) into new `deskops/cli/parse_input.py`; update all callers (operations.py internals, deskops/cli/commands/operations.py, deskops/cli/commands/promote.py) to import from the new module.
8. Run `pytest tests`.
9. Run `deskops list tasks --root .` and `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; confirm both print the task.
10. Confirm `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` is empty and that deskops/services/tasks.py defines `create`, `advance`, `next`.

AMBIGUITIES:
1. No test file path/name/module given for the new comparison test.
2. `tests/fixtures/` root and which fixture TaskDocs count is unspecified.
3. "Overlay output" vs `extract_model_data` output shape is undefined (section dict vs field dict), so equality criteria are unknown.
4. Fixing divergences requires editing documents, but no document files are in the `files:` list and the authorized fix scope is unclear.
5. Which functions exist in the current lifecycle surface (names, signatures, current locations) for create/advance/next is not stated.
6. Required API/signature for `deskops/services/tasks.py` functions is unspecified.
7. Whether `parse_validation_section` is used only by `parse_task_sections` must be determined by the executor; no criterion is given.
8. The exact set of `parse_*_input` functions is not enumerated, only a line range.
9. Whether other modules import `parse_task_sections`/`parse_*_input` beyond promote.py and whether re-exports are allowed is unknown.
10. Whether compatibility re-exports in operations.py are forbidden by the Done When grep criterion is unclear.
11. Circular-import risk between `deskops/cli/parse_input.py` and operations.py is unaddressed.
12. How `_read_doc` routes non-TaskDoc models after removing the overlay branch is not described.
13. The comparison test's expected behavior for malformed docs depends on `deskops list tasks` malformed rendering, whose behavior/API comes from the unresolved `task-rw-f3-closeout-gates-service` dependency.
14. Validation uses task id `task-write-end-to-end-deskops-operator-manual`, but that id appears in the drawer as `task-write-end-to-end-operator-manual`; the referenced task may not exist in `desk/tasks/`.
15. No acceptance criterion for which specific documents are expected to be malformed.
16. Whether the new service must preserve existing CLI behavior/output for create/advance/next is not stated.
