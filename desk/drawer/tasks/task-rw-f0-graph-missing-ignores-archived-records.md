---
id: task-rw-f0-graph-missing-ignores-archived-records
status: deferred
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
- desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md
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

`deskops graph missing --root .` exits 1 on the repo desk (main at 56f49d5) with 102 findings, all `missing_declared_target` from the per-line path scanner (`source-file-reference` provenance) in deskops/graph/extract_edges.py: 98 come from desk/drawer/issues/diagnosis-archive.md (title line says 'archived 2026-09-24'; no frontmatter) and 3 from desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md (a `## Status` section says 'resolved'; no frontmatter). The last one comes from desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md, which quotes deskops/runtime/primitives.py, deleted when afdec7f moved the lifecycle into the sldb graph; that issue is resolved by afdec7f and becomes a record too. They quote task and test paths that were closed or deleted. Today every finding prints and any finding exits 1 (`_graph_missing`, deskops/cli/main.py:280). While this gate is red on the real desk, no task can use it as validation.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops graph missing --root .` exits 0 on the repo desk while a live issue with a dangling path still exits 1. With option A or C every document carrying the record marker is handled by one general rule (no per-file allowlist); with option B the three files no longer contain path-shaped references.

## Scope

_State what is in scope and what is out of scope._

The record marker is checked on every extracted document, not only under desk/drawer/. With option C the output and exit code of `_graph_missing` in deskops/cli/main.py are in scope. Out of scope: other finding kinds and the sldb-backed graph rewrite (task-rw-f4-graph-on-sldb-edge-index). The 102 findings are all from the three files named in Rationale (checked 2026-10-16 with `deskops graph missing --root .` and grouping by provenance); if new non-record findings appear before this task runs, list them in the closeout and do not hide them.

## Implementation Path

_Outline the expected implementation route or affected surface._

Option A or C: (1) mark all three files with the chosen record marker; (2) the path scanner in extract_edges.py tags each edge from a record document with `record: true` in its metadata (option A instead drops those edges there); `find_missing_graph_references` (deskops/graph/checks.py) copies the flag onto `GraphMissingFinding` as a new `record: bool | None = None` field, set to True only for record findings, so `to_dict` (which drops None) keeps today's dicts for live findings (tests/test_graph_checks.py:25,64); (3) option C only: `_graph_missing` (`_graph_missing`, deskops/cli/main.py:280) prints record findings under a separate `Informational (archived records):` heading after the failing ones, does not count them, exits 1 iff at least one non-record finding exists, and ends with `N missing, M informational`. Option B: rewrite each quoted path in the three files as plain text (for example drop the directory part or wrap it so it no longer matches the scanner), with no code change. Tests (all options), in tests/test_graph_declared_edges.py with a `tmp_path` desk: a live issue under desk/drawer/issues/ with a dangling path still yields a finding and exit 1 (the scanner only reads `task` and `issue` documents, extract_edges.py:93); for A or C, a marked record issue with the same path yields no failing finding.

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
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): option C with the `record: true` frontmatter marker. Record findings print under `Informational (archived records):`, are not counted, and do not fail the command; it exits 1 iff a non-record finding exists. Add `record: true` frontmatter to the three files. Implement only the option C path of Implementation Path.

## Open Ambiguities

None.
