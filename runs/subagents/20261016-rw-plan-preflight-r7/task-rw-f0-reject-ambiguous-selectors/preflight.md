RESTATEMENT:
1. Read `deskops/operations.py` ~2580-2760: confirm `_resolve_glob` signature, its exact-match check, the `{doc_id}*.md` glob, and the `_one_artifact_match` (2738) message wording. Read callers at 1015, 1021, 2388, 2436, 2454, 2492, 2511, 2527.
2. Edit `_resolve_glob` only: keep exact-file resolution as-is; after the exact-match check, if `len(matches) > 1` raise `ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`; keep single-match return unchanged.
3. Leave `deskops/cli/main.py` untouched (382-384 already maps `ValueError` to `Invalid value: ...` on stderr, exit 1).
4. In `tests/test_operational.py`, import `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`.
5. Test (a): `_make_repo(tmp_path)`; create `task-foo-bar`, `task-foo-baz` via `_cli` `add task` with explicit `id`; read both `desk/tasks/*.md` texts; run `_cli(root, 'advance', 'task', 'task-foo')`; assert exit 1, stderr contains both stems, both files' text unchanged.
6. Test (b): repo with `task-foo` and `task-foo-bar`; run `advance task task-foo`; assert exit 0, stdout contains `Task: task-foo`, `task-foo-bar.md` unchanged.
7. Run `pytest tests/test_operational.py`, then `pytest tests`. Do not commit.

AMBIGUITIES:
1. Zero-match behavior of `_resolve_glob` is unspecified; only `>1` is defined, so a rewrite could regress the empty case.
2. `directory` type is unstated (single dir vs iterable); the f-string assumes a single dir.
3. Exact-match definition unstated: with/without `.md`, case sensitivity, symlinks.
4. Candidate stem ordering is unspecified; the message is nondeterministic unless the glob is sorted.
5. "Same shape as `_one_artifact_match`" is not verbatim; exact wording/separator is an assumption.
6. `_make_repo`/`_cli` signatures and return values are asserted but not given; whether `_cli` takes `root` and sets `cwd`, and whether the harness sets git identity for its seed commit, is unstated.
7. Whether `advance task task-foo` needs extra flags (`--root`, run dir, `--no-run`) is unstated.
8. Exact paths to read for "task files' text" (`desk/tasks/<id>.md`) are not stated.
9. stdout format `Task: task-foo` for `advance` is assumed, not verified against current output.
10. Effect of the new raise on the other 7 call sites (e.g. `inherits_from`) has no acceptance criterion beyond full `pytest tests` being green.
11. `status: deferred` + dependency `task-rw-f0-close-only-own-primitives`: whether the dependency is closed and the drawer→active promotion is done at dispatch is unstated in the document.
