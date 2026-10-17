RESTATEMENT:
1. Open `deskops/cli/commands/operations.py`; read the add-task branch of `OperationsCLI.run` (≈lines 21–27) plus `DeskopsOperations.resolve_drawer_source` (≈line 551) and `attach_drawer_source` (≈line 583).
2. In `OperationsCLI.run` add-task branch, compute the selector as `args.from_drawer` if truthy, else `payload.get("from_drawer")`; if falsy (absent/empty/null) skip drawer handling.
3. Run the existing resolve/attach step on that selector; preserve current behavior: `FileNotFoundError`/`ValueError` prints the existing `Error: ...` message and returns 1 without creating a task.
4. Confirm flag precedence: when both flag and payload carry a value, use the flag and ignore the payload value without validating it.
5. Create `tests/test_add_task_from_drawer.py` using one sandbox repo: `tmp_path`, `git init`, one empty seed commit, store/desk/lifecycle via `python -m deskops init <root>` or the `lifecycle_desk` fixture; seed one drawer entry; drive CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (or `_make_repo`/`_cli` helpers from `tests/test_lifecycle_end_to_end.py`).
6. Test (a): give the same drawer stem via `--from-drawer`, via `--from-yaml`, and via inline JSON; assert three created tasks (each with its own `id`, payloads include `title`) all record the same repo-relative `from_drawer` path.
7. Test (b): pass an unknown selector in a JSON payload; assert exit code 1 and no new file under `desk/tasks/`.
8. Test (c): create two drawer entries sharing a fragment; pass that fragment in a JSON payload; assert exit code 1 and nothing created.
9. Run `pytest tests/test_add_task_from_drawer.py`, then `pytest tests`.
10. Do not commit; leave the diff for the supervisor's closeout commit.

AMBIGUITIES:
1. The CLI flag name for the "inline JSON payload" is never given; cannot construct the test command.
2. `payload` in `OperationsCLI.run` is referenced via `.get(...)`; not stated whether it is a dict at that point (vs a spec/object), so the required extraction code form is a guess.
3. Not stated whether `resolve_drawer_source` already detects "ambiguous" selectors or whether ambiguity handling must be added; affects which file the change lands in.
4. Definition of "ambiguous"/"share a fragment" is unspecified (substring vs stem-prefix vs glob); test (c) cannot be written deterministically.
5. Placement of the selector-resolution step relative to payload/spec parsing and task creation in the add-task branch is unspecified.
6. Assertion mechanism for "identical `from_drawer` paths" is unspecified (parse front matter vs CLI query).
7. "Creates no `desk/tasks/` file" leaves unspecified how to prove nothing was created (path listing vs store check) and whether partial artifacts elsewhere must also be absent.
8. Exact error message text for the payload path is not given; only "keep the existing `Error: ...` message" for the resolve/attach failures.
9. Whether the sandbox drawer entry is created by CLI or by writing files directly is unspecified.
10. `status: deferred` contradicts the instruction set to execute now; not stated whether to treat it as active.
