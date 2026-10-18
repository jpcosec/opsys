---
id: task-rw-f4-request-sldb-unresolved-references
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f1-model-contract-snapshot
- task-rw-f1-cli-contract-tests
- task-rw-f1-output-golden-files
pills:
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md
files:
- runs/planning/sldb-request-unresolved-references.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f4-request-sldb-unresolved-references.md
---

# Write the sldb request for resolving bare ids and reporting unresolved references

## Rationale

_Explain why this task exists or the business driver behind it._

deskops wants its declared graph edges from sldb's edge index instead of its own regex extractor. Two sldb behaviors block that: `_ids_in` (../sldb/src/sldb/store/edge_index/declared_references.py:66-74) keeps only values written `Model:name`, and deskops stores bare ids (`depends_on: [task-x]`, pill paths), so sldb emits no edge for any deskops reference; and `resolve_edges` (../sldb/src/sldb/store/edge_index/resolve.py:20-30) drops schema edges whose target is not tracked without reporting them, so `graph missing` cannot be computed from sldb.

Plan: phase F4 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

runs/planning/sldb-request-unresolved-references.md contains a reproduction and a proposed public API for both gaps, and the coordinator's written reply is pasted into its `## Response` section.

## Scope

_State what is in scope and what is out of scope._

In scope: the request document. The reproduction runs only in a throwaway repo under /tmp: git init, `deskops init .` (creates the store, registers the deskops models and scaffolds desk/), then `deskops add task` twice, one task with `depends_on: [task-nope]` and one with `depends_on: [TaskDoc:task-nope]`, then inspect sldb's edge index for both; never in ../sldb or its desk. Delivery: the supervisor of this deskops session pastes the file to the coordinator; the executor stops after writing the reproduction and proposal, and the supervisor pastes the reply. Out of scope: writing into the sldb repo or its inbox; the coordinator (the session that supervises deskops and owns sldb) routes it.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce and paste commands and output under `## Reproduction`.
2. Under `## Proposed API`: (a) how a declared reference field can resolve bare ids (for example a per-field allowed-model list, as `__containment__` already has); (b) a function such as `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
3. Under `## deskops caller`: which deskops function will call it (`deskops graph missing`).
4. Hand the file to the coordinator and paste the reply under `## Response`.

## Validation

_List the checks required before this task can close._

- test -f runs/planning/sldb-request-unresolved-references.md
- grep -q '^## Reproduction' runs/planning/sldb-request-unresolved-references.md
- grep -q '^## Proposed API' runs/planning/sldb-request-unresolved-references.md
- grep -q '^## deskops caller' runs/planning/sldb-request-unresolved-references.md
- grep -q '^## Response' runs/planning/sldb-request-unresolved-references.md

## Done When

_Name the observable condition that makes the task complete._

All validation checks pass and `## Response` holds the coordinator's reply, stating for each of the two gaps whether the proposed API is accepted, changed (with the agreed signature), or rejected.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
