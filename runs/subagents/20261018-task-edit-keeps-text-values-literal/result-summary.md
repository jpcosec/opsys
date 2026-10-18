# result summary: task-edit-keeps-text-values-literal

Done by the supervisor directly (small fix; no worker dispatched).

## What changed

- `deskops/operations.py` `_parse_field_value`: `str` and `str | None` fields return the raw value; a value starting with `"` that decodes as a JSON string is decoded (keeps the `json.dumps` workaround working). Other fields still go through `parse_data_value`.
- `tests/test_cli.py`: `test_edit_task_keeps_text_values_literal` (multi-line numbered list, `**Bold** reason.` into `why: str | None`, and a quoted goal).

## Validation

- Test on the unfixed code: fails (`edit ... why "**Bold** reason."` exits 3). With the fix: passes.
- Full suite: see validation.log.

## Reported by

graph-ui-59.
