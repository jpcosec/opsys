RESTATEMENT:

1. Read the surfaces named: `deskops/graph/extract_edges.py` (path scanner; doc selection around line 93), `deskops/graph/checks.py` (`find_missing_graph_references`, `GraphMissingFinding`, `to_dict`), `deskops/cli/main.py` (`_graph_missing`, ~line 280), `tests/test_graph_declared_edges.py`, `tests/test_graph_checks.py` (dict expectations at lines 25 and 64).
2. Read the three drawer files to confirm each quoted path: `desk/drawer/issues/diagnosis-archive.md`, `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`, `desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md`.
3. Reproduce baseline: `deskops graph missing --root .` → expect exit 1; group findings by provenance to confirm the stated per-file counts.
4. Obtain the two owner decisions (option A/B/C; marker form). Task is `status: blocked`; STOP and route back to supervisor if neither is fixed.
5. Assume the recommended pair (option C + `record: true` frontmatter) unless told otherwise:
   - a. Add `record: true` frontmatter to each targeted drawer file (both, per Implementation Path; three, per Rationale/Scope).
   - b. In `extract_edges.py`, detect the marker per extracted document and set `record: true` in each edge's metadata from that document.
   - c. In `checks.py`, add `record: bool | None = None` to `GraphMissingFinding`; set `True` only for record-sourced findings; keep `to_dict` dropping `None` so live-finding dicts are unchanged at `tests/test_graph_checks.py:25,64`.
   - d. In `main.py::_graph_missing`, print record findings under a new `Informational (archived records):` heading after failing ones, exclude them from the failure count, exit 1 iff ≥1 non-record finding exists, and end output with `N missing, M informational`.
6. Option A variant: drop record documents' edges inside the scanner instead of tagging; no CLI change; decide whether the `record` field is still added (Implement Path writes the field clause jointly for A and C).
7. Option B variant: rewrite each quoted path in the files as non-matching plain text; no code change.
8. Add tests in `tests/test_graph_declared_edges.py` using a `tmp_path` desk:
   - live `issue` under `desk/drawer/issues/` with a dangling path → finding present, exit 1;
   - for A/C, a marked record `issue` with the same path → no failing finding.
9. Run: `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py`; `deskops graph missing --root .`; `pytest tests`.
10. Report the diff; do not commit (supervisor commits via `deskops closeout commit`).

AMBIGUITIES:

1. Task is `status: blocked` with no chosen option (A/B/C) and no chosen marker — cannot execute step 5–9; the "Open Ambiguities" entries are unresolved options, not decisions, contradicting the statement that Open Ambiguities are known owner decisions.
2. File count contradiction: Implementation Path says "mark both files"; Rationale/Scope name three files (diagnosis-archive.md, issue-session-20260910…md, issue-refactor-primitives….md).
3. Finding-count contradiction: Rationale gives 96 + 3 = 99, then "98 come from the first file and 3 from the second" = 101, then "the last one" = 102; totals do not reconcile.
4. Marker mechanism unspecified in detail: if `record: true` frontmatter is added, what doc type/frontmatter fields are required for a drawer issue to remain parseable as an `issue` document; no schema/model change is stated.
5. Scope says "the record marker is checked on every extracted document", but extract_edges.py:93 only reads `task` and `issue` documents — behavior for record-marked documents of other types is undefined.
6. Matching rule for the non-frontmatter marker options ('archived' in title; `## Status` saying resolved/archived) is unspecified: exact strings, case sensitivity, body vs title, multiple markers.
7. Implementation Path describes tagging edges and copying to `GraphMissingFinding` for "A or C" jointly, but option A drops the edges — whether the new `record` field is still added under A is unclear.
8. Option C informational semantics underspecified: whether `M` counts findings or documents; whether informational findings appear in `to_dict`/JSON output or only text; exact heading/format compatibility with existing CLI tests.
9. Test assertion for record case ("yields no failing finding") does not state whether an informational finding must be present/asserted under option C.
10. Done When requires `deskops graph missing --root .` exit 0, while Scope says new non-record findings must be "listed in the closeout and do not hide them" — no rule for when a new live dangling path would keep the gate red.
11. Validation lists `tests/test_graph_cli.py` and `tests/test_graph_checks.py` but they are not in `files`; whether they may be modified (e.g. `test_graph_checks.py:25,64`) is unclear.
12. `task-rw-f4-graph-on-sldb-edge-index` is referenced but absent from `depends_on`/`references`; no stated ordering constraint.
13. `runs/planning/deskops-rewrite-inventory.md` is cited but not listed as a file or verified to exist.
14. No acceptance criterion for the "live issue with a dangling path" — whether one exists in the repo now or only in the new test is unspecified.
15. Handling of "record" findings in the sldb-backed graph path is out of scope but no rule is given for preventing the same false positives after f4.
