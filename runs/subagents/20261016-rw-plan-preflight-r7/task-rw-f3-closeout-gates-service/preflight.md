RESTATEMENT:
1. Read pills `desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md` and `desk/contexts/pill-001-task-closure-commit.md`.
2. Read `deskops/operations.py` around lines 2200-2260 to locate `_closeout_reference_evidence`, `_reference_points_to_commit` (2243), `_reference_points_to_test` (2221-2240), `_build_closeout_graph_context`, and every caller of each.
3. Read `deskops/services/` layout and the sibling task doc `task-rw-f3-drawer-routing-service` to copy its move/wrapper pattern.
4. Create `deskops/services/closeout_gates.py` and move the four functions into it.
5. Implement commit gate: `re.fullmatch(r'[0-9a-f]{7,40}', ref)`; `git rev-parse --verify <ref>^{commit}`; `git merge-base --is-ancestor <full-sha> HEAD`; reject on any failure or non-zero exit.
6. Implement tests gate: split off `::<tail>`; reject `Path(ref).is_absolute()`; resolve against `root`; require `.py` suffix, existence, and `resolved.is_relative_to((root / 'tests').resolve())`.
7. Add wrappers in `deskops/operations.py` delegating to the service, preserving current call sites.
8. Edit `tests/test_closeout.py`: reject `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py`, `tests/../deskops/x.py`; accept a real ancestor hash and `tests/test_x.py::test_y`.
9. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
10. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:
1. Task status is `deferred`; unclear whether a deferred task should be executed now or only restated.
2. `task-rw-f3-drawer-routing-service` is not provided, so its "pattern" (module naming, wrapper shape, import style) must be guessed.
3. Wrapper contract is unspecified: keep private names as thin delegating functions, or re-export, or rename call sites.
4. Return contract of the gates is unspecified: bool vs raise vs (ok, reason); must match existing callers, which are not listed.
5. `_closeout_reference_evidence` semantics, signature, and whether its behavior changes are not described; it is only listed for "moving".
6. `_build_closeout_graph_context` signature, dependencies, and whether it mutates global state are not described.
7. `<root>` origin is unspecified: repo root, CWD, git toplevel, or a passed-in parameter.
8. `::` split rule is ambiguous for `tests/a.py::` (empty node) and `tests/a.py::a::b` (multiple separators).
9. `.py` case-sensitivity and symlink handling for the tests gate are unspecified.
10. `resolved.is_relative_to` requires Python >=3.9; project Python floor is not stated.
11. Whether `deskops/services/__init__.py` exists or must be created is unknown.
12. Commit-gate behavior when git is unavailable, not a repo, or `HEAD` is detached/unborn is unspecified.
13. No acceptance criteria for tests of `_closeout_reference_evidence` or `_build_closeout_graph_context`.
14. Boundary with out-of-scope `task-rw-f3-single-closure-path` is unspecified (who calls the service during closeout).
15. Commit-gate "ID that is HEAD" — whether the full 40-char HEAD hash must be accepted by equality (merge-base of HEAD against HEAD passes) is not stated explicitly.
