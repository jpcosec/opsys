RESTATEMENT:

1. Confirm prerequisites: read the three `depends_on` task docs (`task-rw-f1-model-contract-snapshot`, `task-rw-f1-cli-contract-tests`, `task-rw-f1-output-golden-files`) and the pill `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md`; confirm F1 is closed before touching code.
2. Open `deskops/operations.py` and read the four selector resolvers: `_resolve_glob` (~line 2077), `_resolve_artifact_selector_multi` (~2086), `_resolve_artifact_selector` (~2112), `_one_artifact_match` (~2203); record each caller's `glob` vs `rglob` use, `what`-equivalent label, and error wording.
3. Create `deskops/desk_paths.py` with `resolve_selector(desk_root: Path, directories: list[Path], selector: str, pattern: str, what: str, recursive: bool) -> Path`.
4. Implement tier 1: collect files under `directories` whose `name` or `stem` equals `selector`.
5. Implement tier 2: if tier 1 is empty, collect files whose `name` or `stem` starts with `selector`.
6. Dispatch the search by `recursive`: `rglob(pattern)` when true (`_resolve_glob` callers pass the `glob` behavior, artifact selectors pass `rglob`).
7. Zero matches → raise `FileNotFoundError("No <what> file found for selector '<selector>'")`.
8. More than one match → raise `ValueError("Ambiguous <what> selector '<selector>': <candidates>")` with candidates = matching paths relative to `desk_root`, sorted, joined `', '`.
9. Exactly one match → return its `Path`.
10. Pass `what` = artifact id for `_resolve_artifact_selector_multi` / `_resolve_artifact_selector` call sites, and the directory kind (`'task'`) for `_resolve_glob` call sites.
11. Rewrite all four methods in `deskops/operations.py` as one-line delegations to `resolve_selector`; leave `ARTIFACT_PATHS` and other layout constants in place.
12. Grep the test suite for assertions on the old two message formats; update each to the unified format and keep a list of the changed tests.
13. Create `tests/test_desk_paths.py` covering: tier-1 exact name, tier-1 exact stem, tier-2 unique prefix, zero matches (`FileNotFoundError` + new message), ambiguity (`ValueError` + sorted relative candidate list + new message); assert `recursive` toggles `glob` vs `rglob`.
14. Run `pytest tests/test_desk_paths.py`, then `pytest tests`, then run `pytest tests/test_cli_contract.py` explicitly to confirm F1 contract tests pass unchanged.
15. Run `grep -n 'glob(\|rglob(' deskops/operations.py` and confirm no selector-resolution loop remains outside the delegations.
16. Do not commit; hand the diff plus the list of tests whose wording changed to the supervisor for `deskops closeout commit --task task-rw-f2-selector-resolution-module --run-dir <dir>` (or `--no-run --reason <why>`).

AMBIGUITIES:

1. Task `status: deferred` and lives in the drawer, but Resolved Decisions say the supervisor promotes and commits promotion before dispatch — no statement that promotion has happened, so no basis to start.
2. `_one_artifact_match` (2203) is listed as one of the four resolvers yet the implementation path names only `resolve_selector`; unclear whether it becomes a delegation, a private helper kept in `operations.py`, or is deleted.
3. Tier semantics unspecified: whether tier 2 is evaluated only when tier 1 is empty, and whether one exact match plus a longer prefix match is ambiguity or a tier-1 win.
4. Whether tier-1 matches in multiple `directories` (same name in two dirs) count as >1 → `ValueError` is not stated.
5. `directories: list[Path]` — relative to `desk_root` or absolute is not specified; affects rglob base and candidate relativization.
6. Sort key for `<candidates>` (full path vs relative string, case sensitivity, separator normalization) is unspecified.
7. `pattern` semantics are unspecified (`'*.md'` vs `'task-*'`), including whether `rglob(pattern)` recurses without depth limit.
8. The exact `what` strings per call site are not enumerated; only "the artifact id" and "the directory kind (`task`)" are given, and the current artifact-id values are not in the doc.
9. `stem` vs `name` behavior for extension-less files is not defined.
10. Potential contradiction: Scope says two messages change wording for all callers, while Resolved Decisions say `tests/test_cli_contract.py` must pass unchanged; if that file asserts the old wording, the two requirements conflict.
11. Step 16-style closeout list has no destination: no `run-dir` value, and the executor does not commit, so where the list of reworded tests is recorded is undefined.
12. Done When's grep wording ("no selector-resolution loop outside the delegations") does not define an acceptable match set — e.g. whether `glob(`/`rglob(` may still appear in the delegating methods or comments.
13. Line numbers 2077/2086/2112/2203 are pre-F1 coordinates; the doc does not say what to do if F1 moved them.
14. Whether `deskops/desk_paths.py` must be exported, documented, or referenced anywhere (README, `__init__`, skills) is not stated.
15. No acceptance criterion for how candidates are displayed when `desk_root` is not a prefix of the match (out-of-tree templates/fixtures).
