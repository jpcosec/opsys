---
id: task-closed-issues-count-as-records-in-graph-missing
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/graph/extract_edges.py
- tests/test_graph_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# A closed issue counts as an archived record in `graph missing`

## Rationale

_Explain why this task exists or the business driver behind it._

After the desk was brought to zero on 2026-10-18, `deskops graph missing` reported 10 missing targets. All of them came from closed drawer issues whose Resolution refs name task files: `deskops issue close --ref desk/tasks/task-x.md`. Those files were deleted when their tasks closed through closeout. A closed issue is history, just like a `record: true` document, so its stale refs should count as informational and not fail the check.

## Goal

_Describe the concrete result this task must produce._

An issue whose status is closed (frontmatter `status:`, `## Status` section, or `Status:` line) is treated as an archived record by the graph extractor, so `graph missing` lists its unresolved targets as informational. This repository goes back to 0 missing.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/graph/extract_edges.py (where `record` is derived for a source document and for store-unresolved findings), reusing `issue_status` from deskops/services/issues.py, and a test. Out of scope: the issue close verb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Where extract_edges sets `record` for a document, also set it when the source node kind is issue and `issue_status(text) == "closed"`. 2. Do the same in the store-unresolved path. 3. Test: a closed issue with a ref to a missing task file makes `graph missing` exit 0 and lists that finding as informational; an open issue with the same ref still fails.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_graph_checks.py tests/test_graph_cli.py -q
- python -m deskops graph missing --root .
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

`deskops graph missing --root .` reports 0 missing, the new test passes, and `pytest tests` is green.
