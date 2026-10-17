## RESTATEMENT

1. Read repo routing docs per `AGENTS.md` startup route: `README.md`, `docs/faq.md`, `desk/tasks/Board.md`, the two bound pills (`desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md`, `desk/contexts/pill-007-phase-gated-task-flow.md`), and the phase/execution/testing/closeout rituals.
2. Confirm dependency `task-rw-f3-closeout-gates-service` is closed before starting.
3. Read the inventory's phase F3 (`runs/planning/deskops-rewrite-inventory.md`) for the exact move list.
4. Inventory current code: `deskops/operations.py` `_read_doc` (~2366-2377) and its overlay branch; `parse_task_sections` (127-181); `parse_validation_section` (184) and its sole caller; `parse_task_input`/`parse_artifact_input` (991-1037); `_load_yaml_mapping`, `_load_json_mapping`; `ARTIFACT_MODELS`; `deskops/cli/commands/promote.py:47` (`parse_task_sections` call); existing `deskops/services/` package; existing `deskops/cli/parse_input.py`; existing `tests/fixtures/`.
5. Grep all importers of `parse_task_sections`, `parse_validation_section`, `parse_task_input`, `parse_artifact_input`, `_load_yaml_mapping`, `_load_json_mapping` to build the edit set.
6. Write `tests/test_taskdoc_read_without_overlay.py`: enumerate TaskDocs under `desk/tasks/`, `desk/drawer/tasks/` (excluding `Board.md`) and `tests/fixtures/`; for each, compare `_read_doc` (overlay) output against `extract_model_data`; fail (never skip) on any document `extract_model_data` cannot parse.
7. Run the new test; for each divergence, edit the offending TaskDoc under `desk/tasks/` or `desk/drawer/tasks/` so `extract_model_data` output is correct.
8. Remove the overlay branch from `_read_doc` so TaskDoc reads go only through `extract_model_data`.
9. Move `parse_task_sections` into `deskops/cli/commands/promote.py` as a private helper; update its call site at line 47.
10. Delete `parse_validation_section` from `deskops/operations.py`.
11. Keep `tests/test_taskdoc_read_without_overlay.py` as a regression guard asserting `_read_doc(TaskDoc) == extract_model_data` for every TaskDoc.
12. Create/populate `deskops/services/tasks.py` with `create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, and the `next` report function, preserving today's signatures.
13. Move `parse_task_input`, `parse_artifact_input`, `_load_yaml_mapping`, `_load_json_mapping` into `deskops/cli/parse_input.py`; allow `parse_input` to import `ARTIFACT_MODELS` from `operations.py`; ensure `operations.py` has no import of `parse_input`.
14. Update `deskops/operations.py`, `deskops/cli/commands/operations.py`, `deskops/cli/commands/promote.py` to import from the new homes; remove all re-exports from `operations.py`.
15. Run `pytest tests`.
16. Run `deskops list tasks --root .` and `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; confirm both print the task.
17. Confirm `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` is empty and `deskops/services/tasks.py` defines create, advance, next.
18. Do not commit; hand the diff to the supervisor.

## AMBIGUITIES

1. Chicken-and-egg: step 1 requires comparing against the overlay, step 2 removes the overlay; unclear how the guard test compares once `_read_doc` no longer has an overlay branch (compare against a frozen snapshot, or against `extract_model_data` only).
2. Comparison form unspecified: raw dict equality, field-by-field, or normalized values.
3. "A document that `extract_model_data` cannot parse at all is listed by the test as a failure, never skipped" conflicts with `pill-list-surfaces-must-expose-malformed-docs` if any fixture is intentionally malformed; no rule for that case.
4. How to identify which files under `tests/fixtures/` are TaskDocs is unspecified.
5. Whether `Board.md` under `tests/fixtures/` is also excluded is unspecified.
6. Which fixtures directory: `tests/fixtures/` is relative and not confirmed to exist at repo root.
7. Destination filename for the moved `parse_task_sections` (private name unstated) and whether its name/behavior changes.
8. Callers of `parse_task_sections` outside `promote.py:47` are unknown; no instruction for them.
9. Callers of `parse_task_input`/`parse_artifact_input`/`_load_yaml_mapping`/`_load_json_mapping` outside the listed files are unknown.
10. The `next` report function's exact name, signature, and return type are not given.
11. Whether `deskops/services/` and `deskops/cli/parse_input.py` already exist is not stated.
12. Whether `deskops/services/tasks.py` is new or replaces existing code is not stated.
13. No named F1 contract test files; cannot verify "CLI output ... stays as pinned by the F1 contract tests."
14. `deskops show task task-write-end-to-end-deskops-operator-manual` in Validation vs `desk/tasks/...` Done When "both CLI checks print the task": the manual task is in the drawer, so `show task` with `--root .` may not resolve it; contradiction unresolved.
15. Editing TaskDoc files under `desk/tasks/` for divergence fixes vs "the supervisor promotes this drawer task"—whether those doc edits belong in this task's diff is implicit but not stated.
16. Behavior when a TaskDoc cannot be fixed by document edits (no fallback defined).
17. Scope of "the move" — whether lifecycle methods' existing bodies are moved verbatim or rewritten is unspecified.
18. Whether removing `_read_doc`'s overlay branch affects non-TaskDoc document types is asserted but not stated.
19. Done When lists "create, advance and next" as defined names but neither enumerates them nor specifies `__all__`/public API surface.
