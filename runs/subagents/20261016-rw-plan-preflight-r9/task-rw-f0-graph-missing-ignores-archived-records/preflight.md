RESTATEMENT:
1. Assume option C + `record: true` frontmatter: add `record: true` to the frontmatter of `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` (both currently have no frontmatter, so frontmatter blocks must be created).
2. In `deskops/graph/extract_edges.py`, locate the per-line path scanner that emits `source-file-reference` edges; read the extracted document's `record` marker and set `record: true` in those edges' metadata.
3. In `deskops/graph/checks.py`, add `record: bool = False` to `GraphMissingFinding` and have `find_missing_graph_references` copy the edge's `record` flag onto each finding.
4. In `deskops/cli/main.py` `_graph_missing` (lines 297-309), partition findings into non-record (failing) and record (informational); print failing findings first, then a `Informational (archived records):` heading with record findings; print summary `N missing, M informational`; exit 1 iff at least one non-record finding exists, else 0.
5. Add tests to `tests/test_graph_declared_edges.py`: (a) document marked `record: true` with a dangling path yields informational output and exit 0; (b) unmarked live drawer task with the same dangling path yields exit 1.
6. Run: `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`, `deskops graph missing --root .`, `pytest tests`.
7. Confirm `deskops graph missing --root .` exits 0 on the repo desk and record each new non-record finding (if any) in the closeout rather than hiding it.

AMBIGUITIES:
1. Task is `status: blocked` on two unresolved owner decisions (handling A/B/C; marker choice). No option or marker is selected, so the implementation cannot be started.
2. Marker choice is undecided among three options whose detection semantics are unspecified: `record: true` frontmatter, title containing `archived` (case? substring? which line?), or a `## Status` section saying resolved/archived (which values, exact spelling, case).
3. If the title/`## Status` marker is chosen, precedence when both a frontmatter key and a title/status match (or conflict) is undefined.
4. Neither target file has frontmatter; it is unspecified whether adding frontmatter is compatible with SLDB parsing/rendering and whether a new SLDB field contract is required first (AGENTS.md forbids desk-local field documents).
5. `extract_edges.py` is not described beyond "the per-line path scanner"; the exact function/name that must set `record: true` is not given.
6. Scope says the record marker is "checked on every extracted document, not only under desk/drawer/", but only drawer files are marked and the drawer wording elsewhere suggests drawer-only; which documents outside drawer are in scope is unclear.
7. Whether the new `record` field is serialized in JSON/other output formats (and whether existing output-snapshot tests in `tests/test_graph_cli.py` must change) is unspecified; `tests/test_graph_cli.py` appears in Validation but not in `files`.
8. Exact output format is under-specified: column layout, whether informational findings repeat the full finding text, ordering, and how the summary line renders when N=0 or M=0.
9. Whether informational findings keep kind `missing_declared_target` and provenance `source-file-reference` (potentially confusing) is not stated.
10. For option A ("skip record documents in the path scanner") it is unspecified whether the edges are skipped entirely or only omitted from missing-reporting; affects graph output.
11. For option B (edit the two files) the resulting acceptance behavior conflicts with Done When (which assumes records stay and are reported as informational), and no exit-code rule is defined.
12. The "live drawer task with a dangling path" test fixture is not identified (which file, created or existing).
13. The premise "the 99 HEAD findings are all from the two files named" is a checked-at-HEAD claim; if it fails at execution time the task says to list findings in closeout but no criterion states whether the task still passes.
14. `Done When` requires `pytest tests` green, while `Resolved Decisions` says the executor does not commit and the supervisor makes the closeout commit; task-local acceptance for the executor versus supervisor is only partially aligned.
