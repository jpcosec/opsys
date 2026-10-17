RESTATEMENT:

1. Open `deskops/operations.py`; locate `_resolve_glob` (~lines 2077-2084) and confirm it returns `matches[0]` of the `{doc_id}*.md` glob after the exact-file check.
2. Read `_one_artifact_match` (~line 2203) to copy its `ValueError` message shape.
3. Edit `_resolve_glob`: after the exact-match return, add `if len(matches) > 1: raise ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`; keep the single-match return unchanged; if zero matches, preserve existing behavior.
4. Verify callers at lines 674, 955, 1964 are unaffected structurally (no edits; they receive the propagated error).
5. Confirm `deskops/cli/main.py` `main` already maps `ValueError` to `Invalid value: ...` on stderr with exit 1; no CLI change.
6. In `tests/test_operational.py`, import `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`.
7. Test (a): `_make_repo` in `tmp_path` → create `task-foo-bar` and `task-foo-baz` via `deskops add task --root <root> '{...}'` → read both files' text → run `deskops advance task task-foo` → assert exit 1, stderr contains both stems (`task-foo-bar`, `task-foo-baz`), and both files' text identical before/after.
8. Test (b): create `task-foo` and `task-foo-bar` → read `task-foo-bar.md` → run `deskops advance task task-foo` → assert exit 0, stdout contains `Task: task-foo`, and `task-foo-bar.md` text unchanged.
9. Run `pytest tests/test_operational.py`.
10. Run `pytest tests`.

AMBIGUITIES:

1. Signature/return contract of `_make_repo` and `_cli` (args, cwd, captured stdout/stderr, exit-code access) is not given; helpers must be read from `tests/test_lifecycle_end_to_end.py` to write assertions.
2. Exact CLI error line format for `ValueError` (`Invalid value: ...` prefix vs raw message) is asserted only as "stderr names both stems"; whether the `Invalid value:` prefix must also be present is unspecified.
3. `advance task task-foo` may perform resolution before reaching `_resolve_glob` (Board routing / lifecycle node lookup), so it is unknown whether the ambiguous prefix actually reaches `_resolve_glob` for the `advance task` path at lines 674/955/1964.
4. Exact directory string in the error message is unpinned; tests only require stems, so whitespace/ordering of `', '.join(...)` output is unconstrained but glob ordering is unspecified.
5. Whether zero-match behavior must be preserved (currently likely an `IndexError`/other) is not stated; no test covers it.
6. Test function names, file placement within `tests/test_operational.py`, and whether existing imports/fixtures there conflict are unstated.
7. `task-foo` fixture fields are given by example only (`title/goal/scope/implementation_path/done_when/validation`); whether every field is required for `add task` to succeed is unstated.
8. Whether the two new tests must use `subprocess.run` (default) vs in-process `main([...])` is implied by "CLI tests" resolved decision but not restated in the task's Implementation Path.
9. Whether raising `ValueError` on ambiguity breaks any existing test that relies on first-match selection (e.g. `inherits_from`) is not enumerated; only `pytest tests` catches it.
10. "two CLI tests" scope vs. the untouched third caller (line 1964) means no test coverage is required for that path; whether its behavior change (now raising) is acceptable is unstated.
