## RESTATEMENT

1. Read `deskops/operations.py` around lines 154-208 (`parse_task_sections`), 1068-1183 (`parse_*_input`, `_load_yaml_mapping`, `_load_json_mapping`), 2904-2910 (`_read_doc` overlay), 544-546 (list warning); read `deskops/cli/commands/promote.py:47`; read `deskops/cli/commands/operations.py`; confirm which functions implement create/advance/next today.
2. Create `tests/test_taskdoc_read_without_overlay.py`: enumerate every TaskDoc under `desk/tasks/`, `desk/drawer/tasks/` (excluding `Board.md`) and under `tests/fixtures/`; for each, compare current overlay output (`parse_task_sections` over `extract_model_data`) with `extract_model_data` alone; assert equality; treat any doc `extract_model_data` cannot parse as an explicit test failure.
3. For each divergence the test reports, edit the TaskDoc file (under `desk/tasks/`, `desk/drawer/tasks/`, `tests/fixtures/`) so `extract_model_data` yields the correct value; do not alter the overlay.
4. Re-run the new test until it passes with no divergences.
5. In `deskops/operations.py`, delete the overlay branch in `_read_doc` (2904-2910) so TaskDoc reads go through `extract_model_data` only.
6. Move `parse_task_sections` into `deskops/cli/commands/promote.py` as a private helper; also move `parse_validation_section` there if and only if that file is its only remaining user; update `promote.py:47` call site.
7. Move create/advance/next lifecycle methods out of `operations.py` into `deskops/services/tasks.py`, keeping today's signatures (`create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, and the existing `next` report function).
8. Move `parse_*_input` plus only the helpers they use (`_load_yaml_mapping`, `_load_json_mapping`) into new `deskops/cli/parse_input.py`; allow `parse_input` to import `ARTIFACT_MODELS` from `operations.py`; ensure `operations.py` has no import of `parse_input`; no re-export of moved parsers from `operations.py`.
9. Update import sites in `deskops/cli/commands/operations.py` and `deskops/cli/commands/promote.py` so create/advance/next and the moved parsers resolve to their new modules.
10. Run `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` and confirm empty.
11. Run `pytest tests`.
12. Run `deskops list tasks --root .` and `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; confirm both print the task.
13. Leave the diff uncommitted for the supervisor.

## AMBIGUITIES

1. `deskops/services/tasks.py` and `deskops/cli/parse_input.py` are listed as files but not stated to exist; unclear whether to create them or where the code currently lives.
2. "The `next` report function" is unnamed and its signature, module, and return/print behavior are unspecified.
3. Lifecycle method names in Scope are `create_task_bundle`/`advance_task`, but Done When says the service "defines create, advance and next"; unclear which names are required.
4. The "F1 contract tests" pinning CLI output are not identified; file list omits them, so I cannot know which tests constrain output.
5. How `_read_doc` detects "TaskDoc only" (to know which branch to remove) is not stated.
6. Step 1 compares overlay vs `extract_model_data`, but step 2 removes the overlay; post-removal, it is undefined what the retained test asserts, and against what reference it proves correctness.
7. "Fix any divergence by fixing the document" does not bound what may be changed (formatting vs semantic content), and conflicts with keeping changes scoped/semantic.
8. If `extract_model_data` genuinely cannot parse a doc (model gap), no resolution path is given; AGENTS routes that to the sibling `sldb` inbox, but the task does not.
9. Unclear whether `desk/drawer/tasks/` and `tests/fixtures/` must be scanned recursively, and which fixtures qualify as TaskDoc.
10. It is unspecified how non-`Board.md` markdown in those directories that is not a TaskDoc should be handled.
11. Moving `parse_validation_section` is conditional ("if only it uses it"); verification method and fallback if `promote.py` is not the only user are unspecified.
12. Whether the moved `parse_*_input` functions keep their exact names is unspecified, yet Done When greps for `def parse_.*_input`.
13. Validation id `task-write-end-to-end-deskops-operator-manual` conflicts with AGENTS' drawer file `task-write-end-to-end-operator-manual.md`; unclear which id/root resolves.
14. `deskops list tasks --root .` printing the task requires it to be promoted into `desk/tasks/`; promotion is the supervisor's step and the doc is `status: deferred`, so I cannot verify this condition as preflight.
15. CLI output parity is required, but no instruction says whether call sites in `deskops/cli/commands/operations.py` must be rewired; the file is listed without a described change.
16. No behavior-parity criterion for the moved parsers beyond the grep; unclear whether existing parser tests must move or be updated.
17. Unclear whether the service may import sldb directly, and whether `deskops/services/` currently exists.
18. Executor must not commit, but editing tracked TaskDoc files under `desk/` produces a working-tree change whose commit owner is unstated.
19. `depends_on: task-rw-f3-closeout-gates-service`; its completion/green state is not stated and cannot be verified from this document.
20. Interaction between the out-of-scope `list tasks` unreadable-doc warning and step 1's hard-fail rule is unspecified.
