# Task result: task-rw-f0-payload-from-drawer-resolves

## Changed

- `deskops/cli/commands/operations.py` — `OperationsCLI.run`, `add task` branch:
  - Selector now comes from `args.from_drawer` first; if falsy, from `payload.get("from_drawer")` (absent/empty/null/empty-string means no drawer source).
  - The single resulting selector runs through the existing `resolve_drawer_source` / `attach_drawer_source` step, so payload values are stored as the repo-relative path and unknown/ambiguous selectors print `Error: ...` and return 1.
  - Flag wins: when the flag is present the payload value is never inspected or validated.
- `tests/test_add_task_from_drawer.py` (new) — three tests using the `lifecycle_desk` fixture and the real CLI in subprocesses:
  - `test_payload_and_flag_resolve_the_same_drawer_path`: flag, YAML payload, and inline JSON payload all produce three tasks whose `from_drawer` equals `desk/drawer/tasks/task-rw-f0-x.md`.
  - `test_unknown_drawer_selector_in_json_payload_fails`: exit 1, `Error:` printed, no new `desk/tasks/*.md`.
  - `test_ambiguous_drawer_selector_in_json_payload_fails`: two drawer entries sharing `rw-f0`, exit 1, `Ambiguous drawer selector`, no new task file.

## Validation

- `PYTHONPATH=/tmp/rw/wt/payload python -m pytest tests/test_add_task_from_drawer.py -q`
  - Final: `3 passed in 8.15s`
- `PYTHONPATH=/tmp/rw/wt/payload python -m pytest tests -q`
  - Final: `338 passed, 3 skipped in 185.76s (0:03:05)`

## Unfixed-code run

- Stashed only `deskops/cli/commands/operations.py` and reran the new test file:
  - `3 failed in 17.57s` (`test_payload_and_flag_resolve_the_same_drawer_path`, `test_unknown_drawer_selector_in_json_payload_fails`, `test_ambiguous_drawer_selector_in_json_payload_fails`).
  - Unfixed JSON payload created `task-ambiguous-drawer.md` with exit 0, confirming the silent-accept bug.

## Notes / ambiguities

- Cited lines verified: `operations.py:21-27` (flag branch), `resolve_drawer_source` at 493, `attach_drawer_source` at 525, ambiguity raise at 520-522. All accurate.
- Task wording says "all in one sandbox repo with one drawer entry" but case (c) requires two entries. Interpreted as one sandbox per test (via `lifecycle_desk`); (a) and (b) use one drawer entry, (c) adds a second only for the ambiguity case.
- Full-suite environment issue: the worktree initially lacked the gitignored `.pi/skills` tree, so `tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path` failed with `missing use-deskops skill copy: /tmp/rw/wt/payload/.pi/skills/use-deskops/SKILL.md`. This is unrelated to the change (pre-existing, caused by `.pi/` being gitignored and absent from the worktree). Copied the ignored `.pi/skills` tree read-only from the main checkout into the worktree; no tracked files affected. Suite then green.
- No sldb bug observed.
