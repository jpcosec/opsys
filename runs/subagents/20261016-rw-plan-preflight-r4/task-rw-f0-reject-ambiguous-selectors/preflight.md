RESTATEMENT:

1. Precondition: task promoted from `desk/drawer/tasks/` to `desk/tasks/` (supervisor, committed) before dispatch; executor does not commit.
2. Read bound pills `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and `desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md`; run the execution-ritual fresh-context review.
3. Read `deskops/operations.py` `_resolve_glob` (2612-2619), `_resolve_artifact_selector` (2647), `_one_artifact_match` (2738) to copy the ambiguity-message shape; confirm `ValueError -> "Invalid value: ..."`, exit 1 in `deskops/cli/main.py:382-384`.
4. Edit `_resolve_glob`: keep the exact-file check; after it, if `len(matches) > 1` raise `ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`; else return `matches[0]`.
5. Confirm callers (1015, 1021, 2388, 2436, 2454, 2492, 2511, 2527) need no change and already propagate the `ValueError` to the CLI.
6. In `tests/test_operational.py` add test (a): build a throwaway repo in `tmp_path` (`git init`, one seed commit), run `python -m deskops desk install <root>` to scaffold `desk/`, create `task-foo-bar` and `task-foo-baz` via `deskops add task --root <root> '<json with explicit ids>'` (so routine/primitives exist), read both task files' text, run `subprocess.run([sys.executable, '-m', 'deskops', 'advance', 'task', 'task-foo'], cwd=root)`, assert returncode 1, stderr names both stems `task-foo-bar` and `task-foo-baz`, and both files' text unchanged (read before/after).
7. Add test (b): create `task-foo` and `task-foo-bar`, run `advance task task-foo`, assert returncode 0, stdout contains `Task: task-foo`, and `task-foo-bar.md` text unchanged.
8. Use helpers `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`; never mutate the repo's own `desk/`.
9. Run `pytest tests/test_operational.py`, then `pytest tests`.
10. Done when both new tests pass and `pytest tests` is green; supervisor makes the closeout commit via `deskops closeout commit`.

AMBIGUITIES:

1. Tests are scoped to `tests/test_operational.py`, but the required helpers `_make_repo`/`_cli` live in `tests/test_lifecycle_end_to_end.py`; not stated whether to import them, duplicate them, or whether `test_operational.py` already has an equivalent harness.
2. Whether `test_operational.py` is subprocess-style or in-process-style is not stated; Resolved Decisions default to subprocess unless the task says "in-process", but that default may conflict with that file's existing conventions.
3. Exact stderr/error text assertions are unspecified beyond "names both stems": whether to assert the full `Invalid value: Ambiguous id '...' in ...` string, the `directory` portion, or only stem substrings is a guess.
4. Exact stdout assertion for test (b) is only "contains `Task: task-foo`"; the actual `advance` output format is not given, so it is unknown whether that substring exists today or must be produced.
5. Whether `advance task task-foo` (no target status) succeeds on a just-created task is not stated; if `advance` requires a state argument or a non-initial status, test (b) may not exit 0 as written.
6. Creating `task-foo` and `task-foo-bar` in the same repo (test b) may itself hit the same-prefix glob path or slug collision rules; not addressed.
7. Task says scope is "`_resolve_glob` and two CLI tests" but the changed behavior also affects the other callers (`inherits_from`, etc.); whether any of those need test coverage or doc updates is unspecified.
8. `matches` ordering is unspecified; tests must be order-independent for "names both stems", but any assertion on message order would be a guess.
9. Whether the raise happens only after the exact-match check, and whether a single prefix match must return `matches[0]`, is stated — but whether `matches` should be sorted/normalized before the length check is not.
10. It is not stated whether test (a) must also assert exit-code source (ValueError path vs argparse), nor whether stderr vs stdout for the ambiguity message is verified beyond "stderr".
11. Done-When says `pytest tests` green, but no baseline is given for pre-existing failures; unknown whether unrelated failures block closure.
