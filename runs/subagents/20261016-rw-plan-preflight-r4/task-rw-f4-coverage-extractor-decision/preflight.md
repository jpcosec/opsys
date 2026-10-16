RESTATEMENT:

Blocked on the owner decision. Steps below run only after the supervisor records the choice and lifts `blocked`. Two mutually exclusive execution paths; the executor picks exactly one.

Delete path:
1. `git rm deskops/graph/extract_coverage.py`.
2. `git rm tests/test_graph_extract_coverage.py`.
3. Remove the extractor's merge call in `deskops/graph/snapshot.py` (lines ~75-78).
4. Remove its entry from `metadata.source_extractors` in `snapshot.py` (line ~92).
5. Update the asserting test `tests/test_graph_snapshot.py:43`.
6. Regenerate/replace the golden snapshot artifact consumed by `tests/test_graph_snapshot.py`.
7. Verify `grep -rn extract_coverage deskops/` returns nothing.
8. Run `pytest tests` and `deskops graph build --root .`; both must pass.

Keep path:
1. Add registry entry `deskops graph coverage [--root] [--format text|json]` in `deskops/cli/registry.py` (depends on the F5 registry from `task-rw-f5-command-registry`).
2. Implement command behavior: text = one match per line; json = list of objects with `element_id, atom_id, facet, score, basis`; always exit 0.
3. Remove coverage nodes, edges, and the extractor entry from `graph build` (`snapshot.py` ~75-78 and ~92); update `tests/test_graph_snapshot.py:43`.
4. Drop the two sub-cutoff scorers in `extract_coverage.py` (tag-overlap ~line 693, token-overlap ~line 727) and the now-dead 0.70 cutoff at ~line 636.
5. Replace hard-coded `confidence="high"` at lines ~192, 236, 248, 261, 276 (and its write into snapshot edge metadata at `snapshot.py:226`) with score-derived logic: >=0.9 high, else medium.
6. Regenerate the golden snapshot.
7. Verify `deskops graph coverage --help` exits 0 and the built snapshot contains no coverage nodes.
8. Run `pytest tests` and `deskops graph build --root .`.

Supervisor-side (not executor):
9. Supervisor promotes the drawer task, records the choice under Resolved Decisions, commits the promotion, reviews the diff, and closes with `deskops closeout commit` (requiring `pytest tests` green).

AMBIGUITIES:

1. Owner decision is unresolved; the entire task is blocked and no branch can be executed. No information to select delete vs. keep.
2. Keep path: "score" semantics after removing the two sub-cutoff scorers — is the aggregate score recomputed, renormalized, or left to remaining scorers? Unspecified.
3. Keep path: `basis` field meaning, type, and derivation are undefined.
4. Keep path: relationship between the removed 0.70 cutoff and the remaining scorers — are previously excluded matches now emitted? No implicit replacement cutoff given.
5. Keep path: `--root` semantics (repo root vs. desk root vs. `.sldb` store) unspecified.
6. Keep path: `--format json` schema beyond field names (types, ordering, nullability) unspecified.
7. Keep path: fate of `tests/test_graph_extract_coverage.py` (delete, rewrite, keep) not stated.
8. Delete path: location/identity of the "golden snapshot" file is not listed in `files:` nor named.
9. Delete path: whether removing the `source_extractors` entry is a snapshot-schema/version-breaking change needing migration is unstated.
10. Both: effect of `snapshot.py:226` confidence write in the delete path (called out only under keep) — is it removed, retained, or repurposed? Unstated.
11. Both: whether pill-010 graph-runtime output policy constrains the coverage report or the snapshot changes is not stated.
12. Keep path: who removes the F5 dependency vs. keeps it (scope says "supervisor may drop") — decision owner and criteria unspecified.
13. Done When for keep: how "snapshot has no coverage nodes" is verified (which command/assertion/file) is unspecified.
14. Registry change in keep path assumes `task-rw-f5-command-registry` shape; that registry's entry format is not defined here.
