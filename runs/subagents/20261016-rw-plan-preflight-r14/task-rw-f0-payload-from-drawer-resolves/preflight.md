RESTATEMENT:
1. Read `deskops/cli/commands/operations.py`: the add-task branch of `OperationsCLI.run` (selector handling at ~L21-27), `resolve_drawer_source` (~L493), the ambiguity raise (~L520-522), and `attach_drawer_source` (~L525). Read `deskops/specs/compiler.py:57` to see how a payload `from_drawer` currently reaches the task.
2. In the add-task branch, compute the selector as `args.from_drawer` if truthy, else `payload.get("from_drawer")`. Treat absent/empty/null payload value as no drawer source (mirror the existing flag `if`).
3. Run the existing resolve/attach step on that selector; keep the existing `Error: ...` message and `return 1` on `FileNotFoundError`/`ValueError`.
4. Ensure flag precedence: when `args.from_drawer` is set, ignore the payload value without validating it.
5. Create `tests/test_add_task_from_drawer.py` using the `tmp_path` throwaway-repo pattern (git init, one empty seed commit, `python -m deskops init <root>`) and the `_cli` subprocess helper from `tests/test_lifecycle_end_to_end.py`.
6. Seed the sandbox with drawer entry/entries under `desk/drawer/tasks/`; payloads carry at least `title` and a unique `id` per task.
7. Test (a): add the same drawer stem via `--from-drawer`, via `--from-yaml`, and via inline JSON; assert the three created tasks store identical repo-relative `from_drawer` paths.
8. Test (b): JSON payload with an unknown selector; assert exit 1 and no new file in `desk/tasks/`.
9. Test (c): two drawer entries sharing a fragment; JSON payload with that fragment; assert exit 1 and nothing created.
10. Run `pytest tests/test_add_task_from_drawer.py`, then `pytest tests`; confirm both new tests pass and the suite is green.

AMBIGUITIES:
1. Step 2 says "all in one sandbox repo with one drawer entry", but test (c) needs two drawer entries sharing a fragment — contradiction on fixture contents and on whether cases (a)/(b)/(c) share state or are isolated.
2. Exact CLI flag(s) for the inline JSON payload and for `--from-yaml` (file path vs inline string) are not stated.
3. How to read back the stored `from_drawer` value from a created task (frontmatter parser or helper) is unspecified.
4. Whether `deskops/specs/compiler.py:57` must also change, or whether `attach_drawer_source` overwrites the copied raw string; scope lists only `OperationsCLI.run` while the rationale cites `compiler.py`.
5. Payload shape/type at that point (always a dict? one `payload` for both YAML and inline JSON?) is unspecified, and "empty" is undefined (empty string only, or also whitespace/None).
6. Flag-precedence rule (flag wins, payload ignored unchecked) has no test in the implementation path; unclear whether a test is required for Done When.
7. Scope states unknown/ambiguous selectors fail with exit 1 generally, but tests (b)/(c) cover only JSON — unclear whether YAML failure cases are required.
8. How the sandbox drawer entry is created (hand-written file vs a drawer/CLI command) and its exact required frontmatter fields beyond `title` and `id` are unspecified.
9. Exact error message text and whether payload misses/unknown selectors raise `FileNotFoundError` or `ValueError` is not quoted; must be read from existing code.
10. `runs/planning/deskops-rewrite-inventory.md` is referenced but absent from `files`; phase-F0 plan cannot be verified.
11. Frontmatter `status: deferred` contradicts the resolved decision that the supervisor promotes the task to `desk/tasks/` before dispatch.
