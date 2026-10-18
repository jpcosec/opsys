# result summary: task-taskdoc-tags-optional-for-legacy-tasks

Done by the supervisor directly (a one-line contract fix; no worker dispatched).

## What changed

- `deskops/models/task.py`: `tags` marker `rev,list` -> `optrev,list`; `tags` added to `_ABSENT_FRONTMATTER_DEFAULTS`, so a missing key falls back to the `[]` default like the other optional frontmatter keys.
- `tests/test_model_templates.py`: `test_taskdoc_without_tags_key_validates` uses a legacy task with no `tags:` key.
- `tests/fixtures/model_contract_hashes.json`: TaskDoc hash 2fe27e8d… -> f4ea8492… (deliberate contract change; stores pick it up with `desk update --apply` / `stores update`).

## Validation

- Regression test against b4517c0's task.py: 1 failed. With the fix: tests/test_model_templates.py 14 passed; tests/test_model_contract_snapshot.py 2 passed.
- Copy of UIs/graph_ui (tasks 001..006 lack `tags:`), with the fixed deskops on PYTHONPATH: `deskops desk update --root . --apply`, then `sldb stores check` PASS (314 documents in 15 models), `sldb edges check` OK.
- Full suite: see validation.log.

## Reported by

graph-ui-59 (graph_ui store failed `stores check` and `desk update` after b4517c0).
