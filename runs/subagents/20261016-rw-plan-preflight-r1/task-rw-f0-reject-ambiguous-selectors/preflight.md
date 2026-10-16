RESTATEMENT:
1. Read `deskops/operations.py` around line 2612, `_resolve_glob`, and the listed callers (1015, 1021, 2388, 2436, 2454, 2492, 2511, 2527).
2. Read `deskops/cli/main.py` to confirm ValueError → exit 1.
3. Read `tests/test_operational.py` for existing fixtures/helpers for building task docs and invoking CLI.
4. Edit `_resolve_glob`: after the exact-match check, compute prefix matches; if `len(matches) > 1`, raise `ValueError("Ambiguous id '<doc_id>' in <directory>: matches <stem1>, <stem2>, ...")`; else keep `matches[0]`.
5. Add CLI test in `tests/test_operational.py`: create `task-foo-bar` and `task-foo-baz`; run `advance task task-foo`; assert exit 1, both stems present in output, and neither task doc changed.
6. Run `pytest tests/test_operational.py` then `pytest`.
7. Commit as one atomic change.

AMBIGUITIES:
1. Task status is `deferred` and `source:drawer` — AGENTS.md requires promotion to active before implementation; task does not say to promote.
2. `depends_on: task-rw-f0-close-only-own-primitives` — no evidence it is closed.
3. Pills are listed but the task does not say whether to bind/verify them.
4. `<directory>` in the error message: full path, relative path, or basename — unspecified.
5. `<stem1>, <stem2>, ...` — stem = filename without `.md` or the doc_id? Sort order not given.
6. Current `_resolve_glob` shape is described only by line number and behavior; the "exact-match check" is referenced but not shown.
7. `len(matches) == 0` behavior not specified beyond "keeps working as today."
8. Callers may rely on the current first-match fallback; task does not say whether to adjust them or add coverage.
9. Whether other existing tests assert first-match behavior and must be updated — not stated.
10. Where the CLI test creates `task-foo-bar`/`task-foo-baz` (repo `desk/` vs sandbox) — unspecified; AGENTS.md prescribes a sandbox for mutating CLI tests.
11. Exact CLI invocation syntax (`advance task task-foo`) and exit-code contract not verified against `deskops/cli/main.py`.
12. No acceptance criteria for the "exact id still resolves" half of Done When as a test.
13. Placeholder sections (Rationale, Goal, Scope, Implementation Path) contain "_Describe…_" prompts; whether to fill them is unstated.
14. Whether the closeout/phase rituals apply to this task handle are not indicated.
