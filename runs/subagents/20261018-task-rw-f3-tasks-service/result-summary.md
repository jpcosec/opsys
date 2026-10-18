# task-rw-f3-tasks-service — result summary

## What changed

- `deskops/services/tasks.py` (new): `TasksService` owns `create_task_bundle`, `advance_task`, `next_action_report`, plus the task-only helpers `_task_path`, `_next_task_path`, `_board_pills`, `_auto_commit_task_closure`. It delegates shared document helpers (read/write/track, selector resolution, lifecycle facts, board append) to the bound `DeskopsOperations` instance.
- `deskops/operations.py`:
  - `_read_doc` no longer overlays `parse_task_sections`; TaskDoc reads are `extract_model_data` only.
  - Removed `TASK_SECTION_*`, `strip_markdown_frontmatter`, `parse_task_sections`, `parse_validation_section`, `_load_yaml_mapping`, `_load_json_mapping`, `_ensure_mapping_payload`.
  - Removed `parse_task_input` / `parse_artifact_input`.
  - `create_task_bundle`, `advance_task`, `next_action_report` are thin delegations to `self.tasks`.
  - `_append_task_to_board` stays in operations (shared/tested rollback hook); `_auto_commit_task_closure` kept as a delegating private hook because `tests/test_lifecycle_end_to_end.py` calls it.
  - Removed now-unused imports (`subprocess`, `compile_task_spec`, `match_workflow_state`).
- `deskops/cli/parse_input.py` (new): module-level `parse_task_input`, `parse_artifact_input`, `_load_yaml_mapping`, `_load_json_mapping`, `_ensure_mapping_payload`. Imports `ARTIFACT_MODELS` from operations; operations does not import this module.
- `deskops/cli/commands/operations.py`: calls `parse_task_input` / `parse_artifact_input` from `deskops.cli.parse_input`.
- `deskops/cli/commands/promote.py`: private `_parse_task_sections` (formerly `parse_task_sections`) and its frontmatter/placeholder helpers; passes it to the drawer service.
- `deskops/services/drawer.py`: no longer imports from `deskops.operations`; `promote_inbox_to_drawer_task(..., *, parse_sections)` receives the inbox-note parser.
- `desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md`: `## Resolved Decisions` → `### Resolved Decisions` so the H2 section map matches the TaskDoc model.
- `tests/fixtures/golden_desk/desk/tasks/task-golden-alpha.md`: `## Related Atoms` → `### Related Atoms` for the same reason.
- `tests/test_taskdoc_read_without_overlay.py` (new): asserts `_read_doc(path, TaskDoc) == extract_model_data(TaskDoc, raw)` for every `task-*.md` under `desk/tasks/`, `desk/drawer/tasks/`, and `tests/fixtures/`; unparseable docs fail, never skip.
- `tests/test_promotion_nesting.py`: `test_advance_task_reads_nested_task_sections_from_first_occurrence` became `test_advance_task_keeps_nested_h3_sections_inside_scope`; the constructed document uses H3 nested headings and asserts sldb/canonical reads. The old test pinned the deleted regex-overlay behavior and its document cannot round-trip through `extract_model_data`.

## Validation (exact commands / final lines)

- `PYTHONPATH=/tmp/rw/wt/tasksvc python -m pytest tests -q`
  - `398 passed, 3 skipped in 314.64s (0:05:14)`
- `PYTHONPATH=/tmp/rw/wt/tasksvc python -m deskops list tasks --root .`
  - printed `task-rw-f3-drawer-entry-removal-verb`, `task-rw-f3-tasks-service`, `task-write-end-to-end-deskops-operator-manual`
- `PYTHONPATH=/tmp/rw/wt/tasksvc python -m deskops show task task-write-end-to-end-deskops-operator-manual --root .`
  - printed `Task: task-write-end-to-end-deskops-operator-manual`, `Title: Write end-to-end deskops operator manual`, `Status: deferred`, `Current node: ritual-execution`
- `grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py`
  - no output (exit 1)
- `PYTHONPATH=/tmp/rw/wt/tasksvc python -m pytest tests/test_taskdoc_read_without_overlay.py -q`
  - after fix: `1 passed`
  - against unfixed code, before doc fixes: `1 failed in 0.61s` with `AssertionError: _read_doc no longer matches sldb extraction: {'desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md': 'done_when, goal, implementation_path, scope, validation', 'tests/fixtures/golden_desk/desk/tasks/task-golden-alpha.md': 'scope'}`

## Task issues / ambiguities

- The task says to move `parse_task_sections` into `deskops/cli/commands/promote.py`, but the real caller is `DrawerService.promote_inbox_to_drawer_task`. Implemented as a private helper in promote.py passed into the service as a `parse_sections` callable, keeping service → CLI direction absent.
- `tests/test_promotion_nesting.py` pinned overlay behavior that the task removes; it had to be rewritten (fixture document changed to H3) to keep `pytest tests` green.
- `tests/test_lifecycle_end_to_end.py` calls the private `DeskopsOperations._auto_commit_task_closure`; kept a delegating hook rather than editing that unrelated test.
- The task's `files:` list does not mention `tests/test_promotion_nesting.py` or `deskops/services/drawer.py`, both required by the implementation.

## sldb issues

None encountered.
