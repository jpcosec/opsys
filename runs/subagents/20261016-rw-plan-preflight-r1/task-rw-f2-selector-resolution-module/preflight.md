RESTATEMENT:
1. Confirm deps closed: task-rw-f1-model-contract-snapshot, task-rw-f1-cli-contract-tests, task-rw-f1-output-golden-files.
2. Read `deskops/operations.py` around lines 2612 and 2621; capture exact current signatures, bodies, and call sites of `_resolve_glob` and `_resolve_artifact_selector_multi`.
3. Read `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` for constraints.
4. Create `deskops/desk_paths.py` exposing `resolve_selector(directories, selector, pattern)` plus any desk layout path constants/helpers that belong there.
5. Implement resolution order in `resolve_selector`: exact id match, then filename, then stem, then unique prefix; collect matches; raise on ambiguity (>1 match at a tier).
6. Rewrite `_resolve_glob` as a thin wrapper delegating to `desk_paths.resolve_selector` (or to layout helpers), preserving its current external behavior.
7. Rewrite `_resolve_artifact_selector_multi` as a thin wrapper delegating to `desk_paths.resolve_selector`, preserving current behavior.
8. Grep the repo for other selector/glob callers and route them through `desk_paths`.
9. Add `tests/test_desk_paths.py` covering exact id, filename, stem, unique prefix, ambiguous case (raise), and no-match case.
10. Run `pytest tests/test_desk_paths.py`.
11. Run `pytest tests` and confirm F1 contract tests and goldens pass unchanged.
12. Verify no CLI message or behavior changed; commit as one atomic closeout.

AMBIGUITIES:
1. `directories` type/format unspecified (list of `Path`? dict? iterable? include dirs or files?).
2. `selector` type unspecified (str? int id? path?).
3. `pattern` meaning unspecified (glob relative to what? matched against filename/stem/id?).
4. Precedence across tiers unspecified: whether exact id outranks filename, and what "id" means for a file (frontmatter id vs filename).
5. Ambiguity exception type and message unspecified ("raising on ambiguity").
6. No-match behavior unspecified (raise, return None, return empty list).
7. Return type unspecified (single path vs list); contradictory with `_resolve_artifact_selector_multi` returning multiple results while `resolve_selector` reads singular.
8. Case sensitivity of id/filename/stem/prefix matching unspecified.
9. Definition of "unique prefix" unspecified (character prefix? path prefix? minimum length?).
10. Whether `stem` and `prefix` apply only to files or also directories.
11. "Owns desk layout paths" — which path constants/helpers move into `desk_paths.py` is not enumerated.
12. Whether `deskops/desk_paths.py` already exists (dependency on F1) is unknown.
13. Whether current code already raises on ambiguity or whether adding a raise changes behavior, contradicting "Out of scope: changing any CLI message or behavior".
14. Ambiguity rule from task-rw-f0-reject-ambiguous-selectors is referenced but not stated.
15. "All selector callers go through desk_paths" is not machine-verifiable; no grep/exclusion list given.
16. F1 contract tests not identified here; cannot confirm what "pass unchanged" checks.
17. Contents of pill `pill-real-cli-surfaces-prove-operator-contracts.md` unknown; may impose unmet requirements.
18. Cannot verify the referenced line numbers (2612, 2621) or that these are the only two resolvers.
19. No coverage/threshold criteria for `tests/test_desk_paths.py`; test naming/fixtures conventions unknown.
20. Task `status: deferred` with unresolved dependencies — no instruction on whether to execute now.
