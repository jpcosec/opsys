RESTATEMENT:
1. Read `deskops/cli/commands/operations.py`; locate `OperationsCLI.run` add-task branch (rationale cites lines 21-27) and the existing helpers `DeskopsOperations.resolve_drawer_source` (~line 551) and `attach_drawer_source` (~line 583).
2. Read `deskops/specs/compiler.py` around line 64 to see how payload `from_drawer` currently reaches `run`.
3. In the add-task branch of `OperationsCLI.run`, compute selector as `args.from_drawer` if present, else `payload.get("from_drawer")`; if a selector exists, run the existing resolve/attach step on it so the stored value is the repo-relative `desk/drawer/tasks/task-<stem>.md` path.
4. Preserve current error handling: `FileNotFoundError` / `ValueError` → print existing `Error: ...` message and `return 1`, creating no `desk/tasks/` file.
5. Confirm the flag-wins rule when both flag and payload carry a value.
6. Create `tests/test_add_task_from_drawer.py`, copying `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`: git init throwaway repo in `tmp_path`, one seed commit, `python -m deskops desk install <root>`, drive real CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
7. Test (a): same drawer stem via `--from-drawer`, via `--from-yaml`, and via inline JSON → assert all three tasks record identical `from_drawer` paths.
8. Test (b): unknown selector in a JSON payload → assert exit code 1 and no new `desk/tasks/` file.
9. Run `pytest tests/test_add_task_from_drawer.py`, then `pytest tests`.

AMBIGUITIES:
1. Rationale points at `deskops/specs/compiler.py:64` copying the raw string, but Scope/Implementation Path and the `files:` list include only `operations.py` and the new test. Unclear whether `compiler.py` may/must be edited or must stay untouched.
2. Unclear whether the payload reaching `OperationsCLI.run` is the raw loaded dict or a compiled/normalized dict, and therefore whether resolving in `run` is sufficient or resolved too late/with a different key.
3. The flag name/mechanism for the "inline JSON payload" is not given (separate `--from-json`? JSON passed to `--from-yaml`?). Not stated what `--from-yaml` accepts (file path vs literal string).
4. "Ambiguous selector" is never defined, and the task never states whether `resolve_drawer_source` already raises on ambiguity. Cannot know if the ambiguity half of the Goal is already satisfied or needs new code, and no test covers it.
5. No acceptance test specified for the ambiguous-selector case, though Done When/Goal require it.
6. "Missing selector" behavior undefined: absent key vs empty string vs `null`.
7. Test (a) says "produces three tasks" — unclear whether all three live in one throwaway repo or three separate repos, and what payload schema (id/title/etc.) `add task --from-yaml`/JSON requires to succeed.
8. If the flag wins while the payload carries an unknown/ambiguous selector, unclear whether the invalid payload value is still validated/fails.
9. "Creates nothing" is only checkable as "no `desk/tasks/` file"; other side effects (git commit, index/store updates, partial writes) are unspecified.
10. Existing `Error: ...` message text is referenced but not given; cannot know the exact string to preserve or assert.
