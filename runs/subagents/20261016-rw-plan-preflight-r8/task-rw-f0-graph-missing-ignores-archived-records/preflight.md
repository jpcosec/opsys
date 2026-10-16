RESTATEMENT:

1. Treat status `blocked` as gate: confirm owner picked option C (`Informational (archived records)` + `record: true` frontmatter marker). Without that selection, only steps 3–10 are fixed; steps 1–2 vary by option A/B/C.
2. Add `record: true` frontmatter to `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` (both currently have no frontmatter).
3. In `deskops/graph/extract_edges.py`, in the per-line path scanner that produces `source-file-reference` provenance edges, detect the record marker on every extracted document (location-independent, not just `desk/drawer/`). Option C: set `record: true` in each affected edge's metadata. Option A: skip emitting those edges.
4. In `deskops/graph/checks.py`, extend `GraphMissingFinding` with `record: bool = False` and have `find_missing_graph_references` copy the edge flag onto the finding.
5. In `deskops/cli/main.py` `_graph_missing` (lines ~297–309), split findings by `record`; print record findings under a `Informational (archived records):` heading after the failing ones; summary line `N missing, M informational`; exit 1 iff at least one non-record finding exists.
6. In `tests/test_graph_declared_edges.py` add two cases sharing one dangling path: a marked record doc (expect informational, no failure) and an unmarked live drawer task (expect failure/exit 1).
7. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`, then `deskops graph missing --root .`, then `pytest tests`.
8. Verify `deskops graph missing --root .` exits 0 on the repo desk and the 99 HEAD findings still group into the two named files; if new non-record findings appear, record them in closeout without hiding.
9. Do not commit; hand diff to supervisor, who promotes/commits and runs `deskops closeout commit --task <id> --run-dir <dir>` with `pytest tests` green.

AMBIGUITIES:

1. No option (A/B/C) is selected and status is `blocked`; steps 3–5 differ per option, so the task is not executable as written.
2. No marker is selected; `record: true` frontmatter, title containing `archived`, and `## Status: resolved/archived` have unspecified detection semantics (substring? case sensitivity? precedence when both present?).
3. Task says the marker is "checked on every extracted document" but only two files are given markers; unclear what "every ... document" means for other drawer docs (all drawer docs marked, or only explicitly marked ones?).
4. Unspecified how to detect the marker for documents without frontmatter (both target files lack it), and whether that detection lives in `extract_edges.py`, a shared helper, or SLDB.
5. Adding a `record: true` frontmatter key may conflict with the AGENTS rule against desk-local field docs duplicating SLDB field behavior; no instruction on SLDB involvement.
6. Adding a `record` field to `GraphMissingFinding` may change CLI JSON/human output consumed by `tests/test_graph_cli.py` and pill-010 output policy; no spec for serialization or whether `record` appears in output payloads.
7. Exact format of the summary line and heading is only partially fixed (`N missing, M informational`, `Informational (archived records):`); placement, blank lines, and whether `M` counts only record findings are unspecified.
8. "one general rule (no per-file allowlist)" vs. requiring explicit frontmatter on exactly two files is not reconciled: is frontmatter on the two files itself a per-file edit that violates the rule?
9. Contradiction: Done When requires exit 0, but Scope says new non-record findings must be surfaced; if any appear, exit will be 1 and Done When cannot pass.
10. No definition of "live drawer task" for the test: path, fixture vs. real `desk/`, and whether the sandbox desk root (`.tmp/deskops-cli-test`) is used.
11. No acceptance criterion stating which option A/B behavior the tests should assert beyond option C's described semantics.
12. Validation lists `pytest tests/test_graph_cli.py` but Scope/Implementation Path never mention editing it; unclear if CLI tests must change or must stay untouched.
