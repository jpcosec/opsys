RESTATEMENT:
1. Resolve the open decision: delete `deskops/graph/extract_coverage.py` or keep it as an opt-in report. Record the chosen option in this task document.
2. Read `desk/contexts/pill-010-graph-runtime-output-policy.md` and `runs/planning/deskops-rewrite-inventory.md` (F4 section, finding S13) to confirm the constraint the chosen option must satisfy.
3. Branch A (delete): remove `deskops/graph/extract_coverage.py`; remove `tests/test_graph_extract_coverage.py`; delete the coverage section/keys from `deskops/graph/snapshot.py` and any golden fixture it writes; update the golden file to match; grep for remaining imports of `extract_coverage` and remove them.
4. Branch B (keep): add a `coverage` subcommand under `deskops graph` (e.g. `deskops graph coverage`); move the extractor call out of `graph build`; delete branches unreachable under the 0.70 cutoff; remove the hard-coded `confidence="high"` stamp; keep/adjust `tests/test_graph_extract_coverage.py` for the new entry point.
5. Run `pytest` and confirm pass.
6. Run `deskops graph build --root .` and confirm success.
7. Confirm the recorded decision and the code match; commit.

AMBIGUITIES:
1. The owner decision itself is unmade — the task is `status: blocked` with no recorded choice. Both branches are unexecutable as written.
2. "The golden file" is unnamed; no path, format, or regeneration command given.
3. "Snapshot keys" / "snapshot section" are unspecified; exact keys and location in `deskops/graph/snapshot.py` unknown.
4. "Unreachable branches under the 0.70 cutoff" is not enumerated; no list, line ranges, or selection method.
5. `confidence="high"` removal: no stated replacement (drop field, compute value, nullable, constant?) or downstream effect.
6. Branch B entry point is only sketched ("move it behind `deskops graph coverage`"); no CLI signature, flags, output format, or exit-code contract.
7. `depends_on: task-rw-f4-single-snapshot-reader` is not confirmed complete; no read of its output/contract, which may define snapshot keys.
8. Pill `pill-010-graph-runtime-output-policy.md` content is not included; its constraints on the keep/delete option are unknown.
9. `Rationale`, `Goal`, `Scope` placeholders are unfilled — scope bounds and success intent missing.
10. Validation lists commands only; no expected output, coverage threshold, or pass criteria.
11. "Docs are atom-backed" per repo rules: no atom identified for the decision record, so it is unclear whether the decision must be captured in an atom before this task closes.
12. No acceptance criteria distinguishing an acceptable opt-in report from an unacceptable one (e.g., must not be public API, must not run in CI).
