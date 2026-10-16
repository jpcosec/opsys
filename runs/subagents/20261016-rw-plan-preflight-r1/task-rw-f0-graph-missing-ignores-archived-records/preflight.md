RESTATEMENT:
1. Read pills `desk/contexts/pill-009-source-file-graph-traceability.md` and `pill-010-graph-runtime-output-policy.md` for graph traceability and output-policy constraints.
2. Read `deskops/graph/extract_edges.py`; locate the per-line path scanner that emits `source-file-reference` edges and `missing_declared_target` findings.
3. Read `tests/test_graph_declared_edges.py` for existing fixtures/assertions; check whether `tests/test_graph_cli.py` exists.
4. Reproduce baseline: `deskops graph missing --root .` → expect exit 1, 99 findings (96 from `desk/drawer/issues/diagnosis-archive.md`, 3 from `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`).
5. Implement owner-chosen option in `extract_edges.py`:
   - C: detect record docs (status line/title says archived|resolved, or `record: true` frontmatter); emit their dangling paths as informational and not failure-counted.
   - A: skip record docs entirely in the scanner.
   - B: edit the two drawer files so quoted paths stop being path-shaped.
6. Add test: archived/resolved record with a dangling path does not fail the gate.
7. Add test: live drawer task with a dangling path still fails the gate.
8. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`.
9. Run `deskops graph missing --root .`; confirm exit 0.
10. Run `pytest`.

AMBIGUITIES:
1. Owner decision (A/B/C) is unresolved; task is `status: blocked`, so no option can be implemented.
2. Record marker mechanism undefined: status line vs title vs new `record: true` frontmatter flag; no schema/format given for any of the three.
3. No definition of "informational" for option C: whether the finding still prints, whether it appears in the count, and how exit code is derived from mixed informational/failing findings.
4. Exit-code rule unspecified: exit 0 requires zero findings total, or zero non-informational findings?
5. "Live doc" / "live drawer task" (positive test) has no definition or discriminator vs archived/resolved.
6. `tests/test_graph_cli.py` appears in Validation but not in `files`; unclear whether it exists, is in scope, or must be created.
7. No acceptance criteria for the informational output format or the reported count after the change.
8. Whether option C's threshold is limited to the two named files or must generalize to all archived/resolved drawer records.
9. Option B is described as losing verbatim history and contradicts the archived-record intent; no stated tie-break if owner picks B.
10. Whether `record: true` frontmatter requires an SLDB model/schema change (SLDB ownership not addressed in scope).
11. Owner identity and how the decision is recorded/communicated are unspecified.
12. Whether `runs/planning/deskops-rewrite-inventory.md` (phase F0 plan) must be read is unspecified.
13. `depends_on: []` and `references: []` contradict `status: blocked` on a pending owner decision.
