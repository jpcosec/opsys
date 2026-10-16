RESTATEMENT:

1. Confirm `task-rw-f3-primitives-service-and-dead-code` is closed; if not, stop (dependency not satisfied).
2. Read `deskops/operations.py` around `_closeout_reference_evidence`, `_reference_points_to_commit` (~line 2243), and `_build_closeout_graph_context`; map all call sites via grep.
3. Create `deskops/services/closeout_gates.py` containing the moved gate functions (`_reference_points_to_commit` equivalent, tests-path gate, `_closeout_reference_evidence`, `_build_closeout_graph_context`); keep thin wrappers with the old names in `operations.py` that delegate to the service.
4. Commit gate: validate `re.fullmatch(r"[0-9a-f]{7,40}", ref)`, then run `git merge-base --is-ancestor <ref> HEAD` in the repo root; accept only on exit code 0.
5. Tests gate: strip optional `::<node>` suffix, resolve the file part relative to repo root, require it under `tests/` and `os.path.exists`.
6. Wire gate results into the closeout evidence/reference check path unchanged for all other reference kinds.
7. Add tests to `tests/test_closeout.py`: reject `"HEAD"`, `"main"`, `"deskops/x.py"`; accept a real abbreviated/full ancestor commit hash and a `tests/...::node` id.
8. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`.
9. Run `pytest`.
10. Commit the task atomically (pill-001) with traceable evidence (pill-closeout-knowledge-gates-require-traceable-evidence).

AMBIGUITIES:

1. Task status is `deferred` and it depends on an unclosed task; whether I am authorized to start is unstated.
2. Exact current names/signatures of "`_closeout_reference_evidence` and friends" are not given; I must guess the full move set.
3. Whether wrappers must preserve names, signatures, return type (bool vs raise), and error messages is unspecified.
4. `git merge-base --is-ancestor` with an abbreviated (7+ hex) ref can fail as ambiguous in large repos; behavior for ambiguous abbreviations is unspecified.
5. Full 40-hex hash that is valid but not an ancestor: assumed rejected, not stated.
6. Behavior outside a git repo / no HEAD, or when `git` is absent: unspecified.
7. Whether a 7-40 hex string that is a valid tag/blob (not commit) should be rejected: unspecified.
8. Tests gate: whether nested paths (`tests/unit/test_x.py`) are accepted; whether the check is prefix `tests/` or immediate children.
9. Tests gate: must the path end in `.py`? "test file under tests/" is ambiguous (conftest, fixtures, data files).
10. Tests gate `::node` validation depth is unspecified ("optionally"), e.g. is `tests/test_x.py::NotARealTest` accepted since only path existence is checked?
11. Acceptance of absolute paths, `..` traversal, symlinks, and case sensitivity is unspecified.
12. Whether `references` mixing hash and test path is validated per-entry and how multiple entries combine (all-must-pass vs any) is unstated.
13. Test fixture requirements unspecified: temporary git repo? branch creation for `main`? how to obtain a non-ancestor hash.
14. `tests/test_lifecycle_end_to_end.py` existence/path not verified; may not exist.
15. "Done When" says branch names and non-test `.py` files "no longer satisfy closeout" but gives no check for `HEAD`-equivalent full hash or for non-git environments.
16. No coverage threshold, lint, or CLI smoke check specified beyond pytest commands.
17. Shared helper `_build_closeout_graph_context` may have other callers outside the listed `files`; whether to update them is unstated.
