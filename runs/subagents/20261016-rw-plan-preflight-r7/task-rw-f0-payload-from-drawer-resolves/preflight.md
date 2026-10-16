RESTATEMENT:

1. Read `deskops/cli/commands/operations.py` add-task branch in `OperationsCLI.run` (around line 21-27), plus `DeskopsOperations.resolve_drawer_source` (line ~551) and `attach_drawer_source` (line ~583), to see the existing flag-only flow.
2. Read `deskops/specs/compiler.py:64` to see how `from_drawer` flows into the payload for `--from-yaml`/inline JSON.
3. In `OperationsCLI.run` add-task branch, compute the selector as `args.from_drawer` if set, else `payload.get("from_drawer")`; if the selector is truthy, pass it through the existing resolve/attach step exactly as the flag path does.
4. Keep the existing `Error: ...` + `return 1` handling for `FileNotFoundError`/`ValueError`; do not otherwise change the flag path.
5. Create `tests/test_add_task_from_drawer.py`; use `_make_repo` and `_cli` helpers from `tests/test_lifecycle_end_to_end.py` (import or copy per that file's convention); build one sandbox repo in `tmp_path` with git init + seed commit, run `python -m deskops desk install <root>`, seed one drawer entry.
6. Test (a): run the CLI three times against the same drawer stem — via `--from-drawer`, via `--from-yaml` (`from_drawer:` field), and via inline JSON (`from_drawer` key), each with a distinct task `id` — assert three tasks are created and all three store the identical resolved repo-relative `from_drawer` path.
7. Test (b): run the CLI with a JSON payload carrying an unknown `from_drawer` selector; assert exit 1 and that no new `desk/tasks/` file was created.
8. Test (c): seed two drawer entries sharing a fragment; run the CLI with that fragment in a JSON payload; assert exit 1 and nothing created.
9. Run `pytest tests/test_add_task_from_drawer.py`, then `pytest tests`.

AMBIGUITIES:

1. "Both new tests pass" contradicts the three test scenarios (a), (b), (c) in Implementation Path.
2. Inline-JSON CLI surface is unnamed (flag or mechanism for passing inline JSON) — cannot execute (a)/(b)/(c) without guessing.
3. `payload` object identity and availability at the `OperationsCLI.run` add-task branch is unstated; if it is not already present there, plumbing is needed, which conflicts with the files-in-scope list.
4. `deskops/specs/compiler.py:64` is named as the bug source but absent from `files`, yet "In scope" limits work to `OperationsCLI.run` and one new test file — unclear whether the fix must touch the compiler.
5. Drawer selector format (filename stem, full path, prefix fragment) is never specified with an example, so the "same drawer stem" in (a) cannot be constructed deterministically.
6. Ambiguity detection for a shared fragment (c) assumes `resolve_drawer_source` raises `ValueError` on multiple matches; unverified, and out-of-scope routing service (`task-rw-f3`) suggests routing is elsewhere.
7. Exact text of the "existing `Error: ...` message" is not quoted.
8. How a task `id` is supplied in each payload (field name, required or optional) is not stated for (a).
9. Expected resolved `from_drawer` path format is asserted as "identical" but never specified (repo-relative path with `.md`? extensionless?).
10. Where the seeded drawer entry lives inside the sandbox (e.g. `desk/drawer/tasks/`) is implied but not stated.
