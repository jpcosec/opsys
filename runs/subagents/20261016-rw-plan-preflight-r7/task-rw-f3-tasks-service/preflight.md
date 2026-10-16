RESTATEMENT:

1. Enumerate TaskDocs: list files under `desk/tasks/`, `desk/drawer/tasks/` (excluding `Board.md`), and `tests/fixtures/` that are TaskDocs.
2. Write `tests/test_taskdoc_read_without_overlay.py`: for each enumerated TaskDoc, compare current `_read_doc` overlay output (`parse_task_sections` on top of `extract_model_data`) against `extract_model_data` alone; fail on any divergence; fail (not skip) any doc `extract_model_data` cannot parse.
3. Run that test; for each divergent doc, edit the document itself (not the overlay) until overlay and `extract_model_data` agree.
4. Edit `deskops/operations.py::_read_doc`: delete the TaskDoc overlay branch so TaskDoc reads only via `extract_model_data`; delete `parse_validation_section` (~operations.py:211).
5. Move `parse_task_sections` into `deskops/cli/commands/promote.py` as a private helper; update its call site (~promote.py:47).
6. Create/populate `deskops/services/tasks.py` with create/advance/next lifecycle methods, keeping existing signatures (`create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, and the existing `next` report function).
7. Move `parse_*_input` functions (operations.py:1068-1183), plus helpers `_load_yaml_mapping` and `_load_json_mapping`, into `deskops/cli/parse_input.py`; have parse_input import `ARTIFACT_MODELS` from operations.py; ensure operations.py does not import parse_input.
8. Update all callers of the moved methods/parsers (operations.py, cli/commands/operations.py) to the new locations; remove any re-export from operations.py.
9. Run `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` and confirm empty.
10. Run `pytest tests`.
11. Run `deskops list tasks --root .` and `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; confirm both print the task.

AMBIGUITIES:

1. "`parse_*_input`" names are not enumerated; only the line range 1068-1183 is given — must guess which functions qualify and whether any outside that range move.
2. `next` function: no name or signature given ("the `next` report function"), so the method name in `deskops/services/tasks.py` must be guessed.
3. `deskops/services/tasks.py` existence is not stated (new file vs existing module to extend).
4. No criterion for *how* a divergent or unparseable TaskDoc should be fixed (which field/format), only "fix the document."
5. `tests/fixtures/` is not enumerated; unclear which fixtures are TaskDocs, and whether any are intentionally malformed (fixing them could break other tests).
6. Whether `Board.md` is the only non-TaskDoc file to exclude under `desk/tasks/` and `desk/drawer/tasks/` is not stated.
7. F1 contract tests pinning create/advance/next CLI output are referenced but not named/path'ed.
8. Whether `parse_validation_section` has callers other than the overlay is asserted, not verified — if it does, deletion is unsafe.
9. Whether `_load_yaml_mapping`/`_load_json_mapping` or `parse_task_sections` have callers beyond the cited sites is not established.
10. `task-rw-f3-closeout-gates-service` dependency status/closure requirement before execution is not stated.
11. Validation expects `deskops show task task-write-end-to-end-deskops-operator-manual`, but that task lives in `desk/drawer/tasks/` (deferred) — whether `show task` resolves drawer tasks is unstated.
12. No assertion that `ARTIFACT_MODELS` actually lives in operations.py or that moving parsers creates no other import cycles beyond the stated pair.
