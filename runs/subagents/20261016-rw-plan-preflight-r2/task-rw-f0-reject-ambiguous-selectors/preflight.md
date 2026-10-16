RESTATEMENT:

1. Read `deskops/operations.py` around lines 2612–2619 to locate `DeskopsOperations._resolve_glob` and confirm the exact-match check and the `{doc_id}*.md` glob that currently returns `matches[0]`.
2. Read `_one_artifact_match` (~line 2738) to copy the ambiguity error shape.
3. Edit `_resolve_glob`: after the exact-file check, compute `matches` for `{doc_id}*.md`; if `len(matches) > 1`, raise `ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`; otherwise keep returning the single match as today.
4. Leave `deskops/cli/main.py:382-384` unchanged; verify it maps `ValueError` to `Invalid value: ...` on stderr with exit 1.
5. Read `tests/test_lifecycle_end_to_end.py` for `_make_repo` and `_cli`; copy that pattern into `tests/test_operational.py`.
6. Add test (a): in a `tmp_path` repo (git init + one seed commit, `python -m deskops desk install <root>`), create only `task-foo-bar` and `task-foo-baz`, run `subprocess.run([sys.executable, '-m', 'deskops', 'advance', 'task', 'task-foo'], cwd=root)`; assert exit 1, stderr contains both stems `task-foo-bar` and `task-foo-baz`, and neither task file changed.
7. Add test (b): with `task-foo` and `task-foo-bar` present, run the same command; assert exit 0 and that `task-foo` advanced.
8. Run `pytest tests/test_operational.py`, then `pytest tests`.
9. Do not commit; leave the diff for supervisor closeout.

AMBIGUITIES:

1. How the fixture tasks `task-foo-bar` / `task-foo-baz` (and `task-foo`) are created inside the throwaway repo — no command given (`deskops add task`? direct file write under scaffolded `desk/tasks/`?).
2. "neither task file changed" — no mechanism specified (git status, file hash, mtime, content compare).
3. "advances `task-foo`" — no observable assertion defined (which field/status changes, read via which command).
4. A lone single prefix match (only `task-foo-bar` exists, call `task-foo`) is stated in the Goal to keep resolving, but no test covers it; unclear if required for closure.
5. Helpers `_make_repo`/`_cli` live in `tests/test_lifecycle_end_to_end.py`, but `files:` lists only `tests/test_operational.py`; unclear whether to import across test modules or duplicate the helpers.
6. Status is `deferred` / `source:drawer`, while AGENTS.md requires drawer promotion (and a promotion commit) before implementation; task says "Do not commit" — contradiction on whether to promote first.
7. Line numbers (2612–2619, 1015, etc.) may be stale; unclear whether drift matters for acceptance.
8. Error-message exact wording/order is asserted only as "names both stems"; no requirement on candidate ordering or path form in the message.
