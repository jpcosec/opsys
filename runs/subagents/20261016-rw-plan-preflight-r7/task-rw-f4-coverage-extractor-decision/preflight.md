RESTATEMENT:

0. Owner choice is not recorded in this document; read Resolved Decisions for the recorded option before any step. If absent, stop (task is `status: blocked`).

Branch DELETE:
1. Delete `deskops/graph/extract_coverage.py`.
2. Delete `tests/test_graph_extract_coverage.py`.
3. In `deskops/graph/snapshot.py`, remove the extractor merge at lines 75-78.
4. In `deskops/graph/snapshot.py`, remove the `metadata.source_extractors` entry at line 92.
5. Update `tests/test_graph_snapshot.py:43` to drop the extractor assertion.
6. Update the golden snapshot fixture.
7. Verify `grep -rn extract_coverage deskops/` returns nothing.
8. Run `pytest tests` and `deskops graph build --root .`.

Branch KEEP:
1. In `deskops/cli/registry.py` (created by task-rw-f5-command-registry), register `deskops graph coverage [--root] [--format text|json]`.
2. Implement output: text = one match per line; json = list of objects with `element_id, atom_id, facet, score, basis`; always exit 0.
3. In `deskops/graph/snapshot.py`, remove coverage nodes/edges and the extractor entry from `graph build` (lines 75-78, 92).
4. In `extract_coverage.py`, drop the tag-overlap scorer (line 693) and token-overlap scorer (line 727) and the now-dead cutoff at line 636.
5. Replace hard-coded `confidence="high"` (lines 192, 236, 248, 261, 276) with score-derived value (`>=0.9` high, else medium); do the same at `snapshot.py:226`.
6. Update `tests/test_graph_extract_coverage.py` and `tests/test_graph_snapshot.py`.
7. Verify `deskops graph coverage --help` exits 0 and snapshot has no coverage nodes.
8. Run `pytest tests` and `deskops graph build --root .`.

AMBIGUITIES:

1. Owner decision (delete vs keep) is unresolved and not recorded under Resolved Decisions; task is delivered `status: blocked`, so neither branch can be executed as written.
2. Scope says delete may let the supervisor drop the F5 registry dependency; which dependency set applies is a supervisor choice not reflected in `depends_on`.
3. "Update the golden snapshot" gives no path/filename for the golden fixture.
4. Keep branch: default value of `--format` (text vs json) unspecified.
5. Keep branch: text line delimiter and field order unspecified.
6. Keep branch: `score` output type/precision (raw float vs rounded) unspecified.
7. Keep branch: semantics of `facet` and `basis` fields not defined.
8. Keep branch: "signals --root" default root unspecified.
9. Keep branch: "always exits 0" — behavior on missing root, parse failure, or zero matches unspecified.
10. Keep branch: removing the cutoff at line 636 may change which matches are emitted; whether remaining filtering is intended is unclear.
11. `desk/contexts/pill-010-graph-runtime-output-policy.md` is bound but its constraints are not included; it may fix output format details.
12. Done When keep option says "the snapshot has no coverage nodes" but names no command to verify node absence.
13. "Resolved Decisions" says the supervisor records the choice when promoting, while "Open Ambiguities" leaves it open; no acceptance criteria specify who resolves it or how the executor learns it.
14. Closeout requires `pytest tests` green, but no baseline of currently-passing tests is given, so "green" cannot be distinguished from pre-existing failures.
