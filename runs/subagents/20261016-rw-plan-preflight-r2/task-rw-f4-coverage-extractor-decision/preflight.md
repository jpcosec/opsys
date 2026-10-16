RESTATEMENT:

Cannot execute as written: task is `status: blocked` on an owner decision not supplied. Steps 2–6 apply if owner says "delete"; steps 7–12 apply if owner says "keep".

1. Obtain the owner decision (delete vs keep-as-opt-in-report); without it the Goal/Scope are undefined.
2. [delete] Grep repo for imports/calls of `extract_coverage` (notably the call in `deskops/graph/snapshot.py`).
3. [delete] Remove `deskops/graph/extract_coverage.py` and `tests/test_graph_extract_coverage.py`.
4. [delete] Remove the extractor call and the coverage-edge metadata write in `deskops/graph/snapshot.py` (snapshot.py:226).
5. [delete] Update the golden snapshot fixture(s) to drop coverage edges.
6. [delete] Run `pytest` and `deskops graph build --root .`.
7. [keep] Register a `coverage` subcommand on the graph CLI: `deskops graph coverage [--root] [--format text|json]`, printing matches, exit 0.
8. [keep] Remove coverage-edge emission from the `graph build` path.
9. [keep] Delete the tag-overlap scorer (0.65, extract_coverage.py:693) and semantics scorer (0.60, :725), both below the 0.70 cutoff at :636.
10. [keep] Replace hard-coded `confidence="high"` (lines 192, 236, 248, 261, 276) with score-derived confidence: score >=0.9 → `high`, else `medium`; confirm it reaches snapshot edge metadata (snapshot.py:226).
11. [keep] Update `tests/test_graph_extract_coverage.py` and any snapshot/golden tests; run `deskops graph coverage` directly.
12. [keep] Run `pytest` and `deskops graph build --root .`.
13. Record the applied decision in this task document (resolve the Open Ambiguity, update status).
14. Do not commit; leave the diff for the supervisor closeout commit.

AMBIGUITIES:

1. The owner decision is absent; the task is blocked and cannot start.
2. "The decision is recorded in this task" has no target field/edit specified, and "code matches it" is not machine-checkable.
3. Keep-branch: the graph CLI registration module is not in `files:`.
4. Both branches: the golden snapshot file(s) to update are not named.
5. Keep-branch: which surviving scorer supplies the score used for `confidence` is unspecified.
6. Keep-branch: fate of the 0.70 cutoff (line 636) after dropping only the two sub-cutoff scorers is unspecified.
7. Keep-branch: whether `graph build`/snapshot should still record coverage at all (edges removed) or only via the new command is ambiguous.
8. Keep-branch: no `low` confidence value defined for scores below 0.70.
9. Delete-branch: callers/readers of coverage edges/keywords beyond snapshot.py:226 are not enumerated.
10. `deskops graph build --root .` has no expected output or exit criterion; validation has no pass condition.
11. Contradiction: Goal/Scope depend on a decision that is withheld, yet Done When requires the code to match it.
12. Pill `desk/contexts/pill-010-graph-runtime-output-policy.md` content is not included; output-format obligations for the new command are unknown.
13. `depends_on: task-rw-f4-single-snapshot-reader` is not provided; the snapshot builder's current shape is unknown.
