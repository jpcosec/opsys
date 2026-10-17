RESTATEMENT:

0. Cannot start: task status is `blocked` pending the owner decision. First step is the supervisor recording the choice in Resolved Decisions and lifting `blocked`; executor waits for that (and for `depends_on` tasks to be resolved).
1. Delete path — remove `deskops/graph/extract_coverage.py` (907 lines).
2. Delete path — remove `tests/test_graph_extract_coverage.py`.
3. Delete path — remove the extractor's merge into the snapshot at `deskops/graph/snapshot.py:75-78`.
4. Delete path — remove its entry in `metadata.source_extractors` at `snapshot.py:92`.
5. Delete path — update the assertion at `tests/test_graph_snapshot.py:43`.
6. Delete path — regenerate/update the golden snapshot fixture.
7. Delete path — confirm `grep -rn extract_coverage deskops/` is empty.
8. Keep path — add registry entry in `deskops/cli/registry.py` for `deskops graph coverage [--root] [--format text|json]`.
9. Keep path — implement command output: text = one match per line; json = list with fields `element_id, atom_id, facet, score, basis`; always exit 0.
10. Keep path — remove coverage nodes, edges, and the extractor entry from `graph build`.
11. Keep path — drop the tag-overlap scorer (line 693) and token-overlap scorer (line 727) and the now-dead cutoff at line 636.
12. Keep path — compute `confidence` from score (`>=0.9` high, else medium), replacing hardcoded `confidence="high"` at lines 192, 236, 248, 261, 276 and the write at `snapshot.py:226`.
13. Verify per chosen path: delete → grep empty and `pytest tests` green; keep → `deskops graph coverage --help` exits 0, snapshot has no coverage nodes, `pytest tests` green.
14. Run `pytest tests` and `deskops graph build --root .`.
15. Executor does not commit; hand diff to supervisor for closeout commit.

AMBIGUITIES:

1. Owner decision unresolved (delete vs keep) — task is `blocked`; no work can be executed or verified without it.
2. Delete path: unclear whether `metadata.source_extractors` key is deleted entirely or only the coverage entry removed.
3. Both paths: golden snapshot file path and regeneration command are not named ("update the golden snapshot").
4. Keep path: `basis` field values and `score` scale/type are unspecified, so exact output cannot be reproduced or tested.
5. Keep path: exact text format (column order, separators, header or not) is unspecified.
6. Keep path: "always exits 0" is unclear for invalid `--format`, invalid `--root`, or internal errors.
7. Keep path: unclear whether `graph coverage` reuses the existing extractor logic or is an independent implementation.
8. Keep path: dropping the two sub-cutoff scorers/cutoff may change scores of surviving matches; no before/after expected values or test updates given.
9. Contradiction risk: keeping `snapshot.py:226` confidence write while "remove coverage nodes, edges and the extractor entry from `graph build`" is stated — unclear whether that snapshot code path remains reachable or should also change.
10. `depends_on` on `task-rw-f4-single-snapshot-reader` and `task-rw-f5-deprecated-aliases`: unclear who decides to "drop that dependency" for the delete option, and whether executor may proceed if it isn't dropped.
11. Validation/Done When command `deskops graph build --root .` writes to the real repo graph; no sandbox root or `--root` path is specified (AGENTS.md prefers a sandbox for mutating CLI runs).
12. No test requirements stated for the keep path's new `graph coverage` command (existing test file list does not include new tests).
13. Delete path line/anchor references (`snapshot.py:75-78`, `:92`, `:226`) may shift after partial edits; no stated verification method beyond `grep` and tests.
14. "snapshot has no coverage nodes" — the exact command/artifact used to verify this is not specified.
