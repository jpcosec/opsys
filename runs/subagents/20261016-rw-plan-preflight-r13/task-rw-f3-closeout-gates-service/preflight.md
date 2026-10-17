RESTATEMENT:

**Restatement**

1. Confirm prerequisites: `desk/tasks/task-rw-f3-closeout-gates-service.md` exists (promoted + promotion committed by supervisor) and `task-rw-f3-drawer-routing-service` is closed (its service/wrapper pattern is the template).
2. Read `deskops/services/drawer_routing.py` (or equivalent path created by the dependency task) plus its wrappers in `deskops/operations.py` to copy the module placement, naming, docstring, and wrapper/delegation style.
3. Create `deskops/services/closeout_gates.py` and move into it: `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test`, `_build_closeout_graph_context` (exact current bodies, minus the two gate tightenings).
4. Leave wrappers with the same names/signatures in `deskops/operations.py` that call the service so existing imports/callers keep working.
5. Commit gate in the service: reject unless `re.fullmatch(r'[0-9a-f]{7,40}', ref)`; run `git rev-parse --verify <ref>^{commit}` (non-zero → reject; also covers ambiguous abbreviations); then `git merge-base --is-ancestor <full_sha> HEAD` (non-zero → reject; equal-to-HEAD returns 0 → accept); return bool.
6. Tests gate in the service: split the reference at the first `::` and keep the path part; reject if `Path(ref).is_absolute()`; `resolved = (root / ref).resolve()`; require `resolved.suffix == '.py'`, `resolved.exists()`, and `resolved.is_relative_to((root / 'tests').resolve())`; ignore the `::node` part.
7. Update `_closeout_reference_evidence` (and any caller) as needed to delegate to the moved/tightened gates; confirm `_build_closeout_graph_context` still calls whatever helper wraps the tests gate.
8. Add/extend `tests/test_closeout.py` with rejections for `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py`, `tests/../deskops/x.py`, and acceptances for a real ancestor hash of HEAD and `tests/test_x.py::test_y`.
9. Verify the pre-existing hash-based expectations still pass: `tests/test_closeout.py:335` and `tests/test_lifecycle_end_to_end.py:126`.
10. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
11. Do not commit; hand the diff to the supervisor for the closeout commit (`deskops closeout commit --task <id> --run-dir <dir>`).

**AMBIGUITIES**

1. Service function names/signatures are not specified (keep `_`-prefixed? public names? same params incl. `root`, `run_dir`?).
2. "wrappers" is undefined: whether `operations.py` wrappers must keep the exact old signatures or may re-export, and whether `_closeout_reference_evidence` / `_build_closeout_graph_context` are in `operations.py` at all (only line numbers for two gates are given).
3. No instruction to grep for other callers of the four functions; hidden call sites outside the two test files are unknown.
4. `root` provenance is unstated: which object supplies it (repo root, run dir, task root) and how the service receives it.
5. How `git` is invoked is unspecified (subprocess wrapper, cwd, env, existing helper in `operations.py`, error/timeout handling).
6. Behaviour on git failure other than "not an ancestor" (exit code 2/128, missing repo) is unspecified.
7. `Path.is_relative_to` requires Python ≥3.9; the project's minimum supported version is not stated.
8. Symlink handling inside `tests/` is unspecified (`.resolve()` resolves symlinks; whether that is desired is not stated).
9. Empty/whitespace/`None` reference handling is unspecified.
10. Multiple `::` in a reference is unspecified (`a.py::b::c`).
11. "a real ancestor hash" in the new test: how to obtain it deterministically (fixture, `git rev-parse HEAD~1`, skip if shallow) is unspecified.
12. Test addition has no named test functions or assertion style guidance.
13. `_build_closeout_graph_context` must be moved, but no requirement says behaviour must be bit-identical; acceptance criteria for that move are absent.
14. `runs/planning/deskops-rewrite-inventory.md` (the cited plan) is not verified to exist in the repo.
15. Contradiction: `pills` binds `pill-001-task-closure-commit`, but Resolved Decisions says the executor does not commit and the supervisor makes the closeout commit.
