RESTATEMENT:

1. Stop: task status is `blocked`; do not begin branch work until the owner decision (delete vs keep) is recorded under Resolved Decisions.
2. If delete: remove `deskops/graph/extract_coverage.py`; delete `tests/test_graph_extract_coverage.py`; remove the extractor merge at `deskops/graph/snapshot.py:75-78`; remove its `metadata.source_extractors` entry at `snapshot.py:92` and the assertion at `tests/test_graph_snapshot.py:43`; regenerate the golden snapshot.
3. If keep: add `deskops graph coverage [--root] [--format text|json]` as an entry in `deskops/cli/registry.py` (per task-rw-f5-command-registry) printing matches, exit 0; strip coverage nodes/edges and the extractor entry out of `graph build`; delete the tag-overlap (line 693) and token-overlap (line 727) scorers and the dead cutoff at line 636; derive `confidence` from score (>=0.9 high, else medium) instead of the hard-coded `"high"` at lines 192/236/248/261/276.
4. Run `pytest tests` and `deskops graph build --root .`; confirm Done When (`grep -rn extract_coverage deskops/` empty for delete, or `deskops graph coverage --help` exit 0 plus no coverage nodes in snapshot for keep).
5. Do not commit; hand diff to supervisor for closeout.

AMBIGUITIES:

1. The single blocking decision (delete vs keep) is unresolved; neither branch can start.
2. Scope says the keep option runs after the F5 chain, but `depends_on` lists only task-rw-f5-deprecated-aliases, not task-rw-f5-command-registry which the keep path requires; and it says the delete option can drop the F5 dependency — unknown whether to wait at all.
3. No acceptance criteria define what `deskops graph coverage` "prints matches" against: no input source, query, root semantics, argument behavior, or exit-code rules beyond exit 0.
4. Keep-path `confidence` thresholds (>=0.9 high, else medium) have no defined score source once the tag-overlap and token-overlap scorers and the line 636 cutoff are removed; the surviving score range is unspecified.
5. "Update/regenerate the golden snapshot" gives no path, fixture name, or regeneration command.
6. Unclear whether the executor edits the task document to record the choice under Resolved Decisions, or the supervisor does.
7. Implementation Path cites exact line numbers (636, 693, 727, 192/236/248/261/276, snapshot.py:75-78/92/226, tests:43) that may not survive prior F5 edits; no verification method given for drift.
8. No stated behavior for `metadata.source_extractors` in the keep path (remove entry only, or retain under another name).
