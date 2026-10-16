RESTATEMENT:

1. Open `deskops/cli/commands/operations.py` and locate `OperationsCLI.run` and its add-task branch (referenced lines 21-27).
2. Compute the selector: use `args.from_drawer` if set, else `payload.get("from_drawer")` (flag wins when both present).
3. Run the existing resolve/attach step on that selector (`DeskopsOperations.resolve_drawer_source` ~line 551 and `attach_drawer_source` ~line 583) so it becomes a repo-relative drawer path, replacing the raw-string copy currently at `deskops/specs/compiler.py:64` for this path.
4. Ensure resolution happens before any `desk/tasks/` file is written, so a failure creates nothing.
5. On `FileNotFoundError`/`ValueError`, print the existing `Error: ...` message and `return 1`.
6. Create `tests/test_add_task_from_drawer.py`, copying `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py` (tmp_path + git init + seed commit + `python -m deskops desk install <root>` + `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`).
7. Test (a): seed a drawer task, then run add-task three times — via `--from-drawer`, via `--from-yaml`, via inline JSON — and assert three tasks with identical `from_drawer` repo-relative paths.
8. Test (b): unknown selector in a JSON payload exits 1 and creates no `desk/tasks/` file.
9. Run `pytest tests/test_add_task_from_drawer.py` then `pytest tests`.
10. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:

1. The inline JSON payload transport is unspecified: flag name, whether it is a path or a raw string, and its schema.
2. `--from-yaml` source form (file path vs inline string) and expected key layout are unspecified.
3. How to seed the drawer task in the throwaway repo for test (a) (path, filename convention, front matter) is not stated.
4. "Ambiguous selector" is undefined and untested; no rule for what makes a selector ambiguous or its expected output.
5. Required `add task` arguments for the three runs (id, title, body, etc.) are not specified.
6. Precedence between `--from-yaml` and inline JSON when both carry `from_drawer` is undefined (only flag-vs-payload is defined).
7. Where `payload` is defined in `OperationsCLI.run` and whether YAML and JSON share the same dict is not stated.
8. Whether the selector is the stem without the `task-` prefix (rationale implies yes) or the full filename is not explicit in Scope/Goal.
9. Signatures and contracts of `resolve_drawer_source` / `attach_drawer_source` (both required vs one) are not given; must be read.
10. It is unstated whether resolution must be relocated before task creation or is already ordered correctly in the existing code.
