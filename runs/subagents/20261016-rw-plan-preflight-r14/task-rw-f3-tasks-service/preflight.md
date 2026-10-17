RESTATEMENT:
1. Verify dependency `task-rw-f3-closeout-gates-service` is closed and this task has been promoted to `desk/tasks/` (supervisor-side; executor does not commit).
2. Create `tests/test_taskdoc_read_without_overlay.py` that walks every TaskDoc under `desk/tasks/` and `desk/drawer/tasks/` (excluding `Board.md`) plus `tests/fixtures/`, and for each compares the overlay-parsed result with `extract_model_data`.
3. Run that test; for each divergence, edit the offending document so `extract_model_data` is authoritative; emit an explicit failure (no skip) for any TaskDoc `extract_model_data` cannot parse.
4. In `deskops/operations.py` remove the TaskDoc overlay branch in `_read_doc` (2366-2377) so TaskDoc reads go through `extract_model_data` only.
5. Move `parse_task_sections` (operations.py:127-181) into `deskops/cli/commands/promote.py` as a private helper and update its call site (promote.py:47).
6. Delete `parse_validation_section` (operations.py:184).
7. Create `deskops/services/tasks.py` owning create/advance/next, preserving signatures `create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, and the existing `next` report function.
8. Create `deskops/cli/parse_input.py` containing `parse_task_input` and `parse_artifact_input` plus `_load_yaml_mapping`/`_load_json_mapping`; allow `parse_input` to import `ARTIFACT_MODELS` from `operations.py`; ensure `operations.py` imports nothing from `parse_input`.
9. Repoint CLI command modules (`deskops/operations.py`, `deskops/cli/commands/operations.py`, `deskops/cli/commands/promote.py`) at the new service and parser module; leave no re-export of moved parsers in `operations.py`.
10. Keep `tests/test_taskdoc_read_without_overlay.py` as the regression guard that `_read_doc(TaskDoc) == extract_model_data`.
11. Run `pytest tests`; run `deskops list tasks --root .` and `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; confirm CLI output for add/show/list/advance/next matches `tests/test_cli.py:650,1440,772`.
12. Confirm `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` is empty.

AMBIGUITIES:
1. "Overlay output" is not a named callable: unclear whether step 1 compares `parse_task_sections` output, `_read_doc` output, or `_read_doc` vs `extract_model_data`. The test name (`read_without_overlay`) and step 2's regression-guard wording conflict with step 1's "compare overlay output."
2. Test lifecycle not specified: if step 1's test calls the overlay, the overlay no longer exists after step 2, but nothing says the test must be rewritten then or which comparison it uses afterward.
3. The `next` function has no name or signature (only "the `next` report function"); source location of create/advance/next in `operations.py` is not given.
4. Which "lifecycle methods" exactly move is undefined beyond create/advance/next; unclear whether CLI command wrappers, `TaskBundle` type, or adjacent helpers move too.
5. `parse_*_input` is a glob: only `parse_task_input`/`parse_artifact_input` are confirmed; no confirmation these are the only matches.
6. `_load_yaml_mapping`/`_load_json_mapping` are stated to be "used only by them" but their current location and that exclusivity are unverified in the doc.
7. `operations.py keeps no re-export` — external importers of the moved symbols (outside the listed files) are unknown.
8. `ARTIFACT_MODELS` import path/definition location in `operations.py` is not stated.
9. Validation `deskops show task task-write-end-to-end-deskops-operator-manual --root .` presumes that task doc is discoverable in `desk/tasks/`; no path or existence check is specified.
10. `deskops list tasks`/`deskops show task` subcommands are assumed to exist as written; not confirmed in the doc.
11. Board.md exclusion is stated for `desk/tasks/`, `desk/drawer/tasks/`; unclear whether it also applies to `tests/fixtures/`.
12. "Every TaskDoc" under `tests/fixtures/` is undefined: no rule for what counts as a TaskDoc vs other fixture models.
13. Divergence handling says "fix the document," but no acceptance criterion distinguishes a buggy document from a buggy `extract_model_data`.
14. Removing the overlay is described as TaskDoc-only, but `_read_doc`'s branch condition as written (2366-2377) is not shown; ambiguous whether other models share the branch.
15. Dependency `task-rw-f3-closeout-gates-service` state is unknown; this task is `status: deferred` and has no stated start precondition beyond the promotion note.
16. Step ordering conflict: scope lists the move first and overlay removal second, but Implementation Path orders the test/fix first; no single authoritative order.
