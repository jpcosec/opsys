---
id: task-rw-f0-graph-missing-ignores-archived-records
status: blocked
references: []
depends_on: []
pills:
- desk/contexts/pill-009-source-file-graph-traceability.md
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/extract_edges.py
- deskops/graph/checks.py
- deskops/cli/main.py
- tests/test_graph_declared_edges.py
- desk/drawer/issues/diagnosis-archive.md
- desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:graph
- topic:gates
---

# `graph missing` stops failing on paths quoted in archived drawer records

## Rationale

_Explain why this task exists or the business driver behind it._

`deskops graph missing --root .` exits 1 on the repo desk at HEAD with 99 findings, all `missing_declared_target` from the per-line path scanner (`source-file-reference` provenance) in deskops/graph/extract_edges.py: 96 come from desk/drawer/issues/diagnosis-archive.md (title line says 'archived 2026-09-24'; no frontmatter) and 3 from desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md (a `## Status` section says 'resolved'; no frontmatter). They quote task and test paths that were closed or deleted long ago. Today every finding prints and any finding exits 1 (deskops/cli/main.py:297-309). While this gate is red on the real desk, no task can use it as validation.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops graph missing --root .` exits 0 on the repo desk while a live issue with a dangling path still exits 1. With option A or C every document carrying the record marker is handled by one general rule (no per-file allowlist); with option B the two files no longer contain path-shaped references.

## Scope

_State what is in scope and what is out of scope._

Blocked on the owner's choice (see Open Ambiguities). The record marker is checked on every extracted document, not only under desk/drawer/. With option C the output and exit code of `_graph_missing` in deskops/cli/main.py are in scope. Out of scope: other finding kinds and the sldb-backed graph rewrite (task-rw-f4-graph-on-sldb-edge-index). The 99 HEAD findings are all from the two files named in Rationale (checked 2026-10-16 with `deskops graph missing --root .` and grouping by provenance); if new non-record findings appear before this task runs, list them in the closeout and do not hide them.

## Implementation Path

_Outline the expected implementation route or affected surface._

Option A or C: (1) mark both files with the chosen record marker; (2) the path scanner in extract_edges.py tags each edge from a record document with `record: true` in its metadata (option A instead drops those edges there); `find_missing_graph_references` (deskops/graph/checks.py) copies the flag onto `GraphMissingFinding` as a new `record: bool | None = None` field, set to True only for record findings, so `to_dict` (which drops None) keeps today's dicts for live findings (tests/test_graph_checks.py:25,64); (3) option C only: `_graph_missing` (deskops/cli/main.py:297-309) prints record findings under a separate `Informational (archived records):` heading after the failing ones, does not count them, exits 1 iff at least one non-record finding exists, and ends with `N missing, M informational`. Option B: rewrite each quoted path in the two files as plain text (for example drop the directory part or wrap it so it no longer matches the scanner), with no code change. Tests (all options), in tests/test_graph_declared_edges.py with a `tmp_path` desk: a live issue under desk/drawer/issues/ with a dangling path still yields a finding and exit 1 (the scanner only reads `task` and `issue` documents, extract_edges.py:93); for A or C, a marked record issue with the same path yields no failing finding.

## Validation

_List the checks required before this task can close._

- pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py
- deskops graph missing --root .
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`deskops graph missing --root .` exits 0 on the repo desk (with option C it may print informational record findings), the new tests for the chosen option pass, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

- Owner decision, handling: A) skip record documents in the path scanner; B) edit the two files so the quoted paths stop looking like references (loses verbatim history); C) report record findings as informational with exit 0 (recommended; semantics in Implementation Path).
- Owner decision, marker: a `record: true` frontmatter key (recommended; both files need frontmatter added), the title containing 'archived', or a `## Status` section saying resolved/archived.
