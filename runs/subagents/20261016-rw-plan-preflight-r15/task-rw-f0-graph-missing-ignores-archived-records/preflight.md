RESTATEMENT:

1. Wait for owner decisions (handling option A/B/C; marker form) — task is `status: blocked` until resolved.
2. If option B: edit the three files (`desk/drawer/issues/diagnosis-archive.md`, `.../issue-session-20260910-handoff-uncommitted-work-and-open-items.md`, `.../issue-refactor-primitives-to-ast-driven-task-nodes.md`) to rewrite each quoted path as plain text so the scanner no longer matches it; no code change.
3. If option A or C: add the chosen record marker to all three files (frontmatter `record: true` requires adding frontmatter to files that lack it).
4. In `deskops/graph/extract_edges.py` path scanner (~line 93; reads only `task` and `issue` documents): for a record document, option A drops its edges; option C sets `record: true` on each edge's metadata.
5. In `deskops/graph/checks.py` `find_missing_graph_references`: add `record: bool | None = None` to `GraphMissingFinding`, copy the flag from the edge, set True only for record findings; keep `to_dict` dropping `None` so live-finding dicts are unchanged (tests/test_graph_checks.py:25,64).
6. Option C only: in `_graph_missing` (`deskops/cli/main.py:280`) print record findings under `Informational (archived records):` after failing findings, exclude them from the count and exit logic, exit 1 iff ≥1 non-record finding, and end output with `N missing, M informational`.
7. Add tests to `tests/test_graph_declared_edges.py` using a `tmp_path` desk: (a) live issue under `desk/drawer/issues/` with a dangling path yields a finding and exit 1; (b) for A/C, a marked record issue with the same path yields no failing finding.
8. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py`, then `deskops graph missing --root .`, then `pytest tests`.
9. Hand the diff to the supervisor; executor does not commit. Supervisor promotes the drawer task, reviews, and closes with `deskops closeout commit --task <id> --run-dir <dir>` (or `--no-run --reason <why>`), requiring `pytest tests` green.

AMBIGUITIES:

1. Owner decision on handling (A/B/C) is unmade; task cannot start or finish.
2. Owner decision on marker form (`record: true` frontmatter / title containing 'archived' / `## Status` resolved-archived) is unmade.
3. Open Ambiguities says "both files need frontmatter added" but three files are named; which files need frontmatter is unspecified.
4. The third file (`issue-refactor-primitives-to-ast-driven-task-nodes.md`) is asserted to already be resolved (afdec7f) and to "become a record," but no statement that it carries any of the three marker forms (title has no 'archived'; `## Status` presence unknown).
5. Scope says the record marker "is checked on every extracted document, not only under desk/drawer/", but the scanner only reads `task` and `issue` documents (extract_edges.py:93); which document types/marker fields the check reads is unspecified.
6. Option A drops record edges in the scanner, yet step (2) of Implementation Path describes adding a `record: bool | None` field for A or C; whether the field is added under A is unclear.
7. Option C exit semantics ("exits 1 iff at least one non-record finding") conflict with Done When ("exits 0") whenever a non-record finding survives; whether new non-record findings block closure is unspecified.
8. `N` and `M` in `N missing, M informational` are not defined (whether N excludes record findings).
9. Whether the summary line is printed in all options or only option C is unspecified.
10. `tests/test_graph_cli.py` appears in Validation but not in `files`; whether CLI output changes require updating it is unstated.
11. Expected new test names/counts, and how a "live issue" and "marked record issue" fixtures are constructed, are unspecified.
12. No acceptance criterion for option B beyond "no longer contain path-shaped references"; verification method undefined.
13. Closeout requires a run dir (`--run-dir <dir>`) that no path is given for.
14. Whether pill bindings (`pill-009`, `pill-010`) or the run plan `runs/planning/deskops-rewrite-inventory.md` require edits is not stated.
