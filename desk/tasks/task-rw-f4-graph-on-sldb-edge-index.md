---
id: task-rw-f4-graph-on-sldb-edge-index
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f4-request-sldb-unresolved-references
- task-rw-f3-atoms-service
- task-rw-f3-closeout-gates-service
- task-rw-f0-graph-missing-ignores-archived-records
- task-rw-f1-output-golden-files
pills:
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- desk/contexts/pill-009-source-file-graph-traceability.md
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/extract_edges.py
- deskops/graph/extract_docs.py
- deskops/graph/snapshot.py
- deskops/services/closeout_gates.py
- tests/test_graph_cli.py
- tests/test_graph_declared_edges.py
- tests/test_graph_extract_edges.py
- runs/planning/graph-missing-baseline.txt
- tests/fixtures/golden/graph_snapshot.kg.json
- runs/planning/graph-id-mapping.md
- deskops/graph/self_reflection.py
- deskops/cli/parser.py
- tests/fixtures/knowledge_graph/static_desk_source_graph.json
- tests/test_graph_extract_docs.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f4-graph-on-sldb-edge-index.md
---

# Declared graph edges come from the sldb edge index

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S4: deskops/graph/extract_edges.py re-implements with regex the declared edges sldb indexes, and deskops uses several node-id schemes (`task:`, `atom:`, `pill:`, `doc:`, `board:`, `drawer_task:<path>`, ... from deskops/graph/extract_docs.py:59-115, plus `source_file:`/`test_file:` from extract_sources.py:108-112), so promoting a drawer task changes its node id.

Plan: phase F4 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Edges declared by model fields come from sldb's public edge index (per the API agreed in task-rw-f4-request-sldb-unresolved-references); document nodes use one id scheme `<kind>:<id>` with `drawer_task` folded into `task`; file nodes keep `source_file:<path>`/`test_file:<path>`; `graph missing` uses sldb's unresolved-reference report. Id mapping: kinds keyed by frontmatter `id` today (atom, task, pill, board, and the rest in deskops/graph/extract_docs.py:183-193) keep `<kind>:<frontmatter id>`; `drawer_task:<path>` becomes `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) keep `<kind>:<path>`. Old ids get no alias.

## Scope

_State what is in scope and what is out of scope._

In scope: extract_edges.py, extract_docs.py, snapshot.py, the closeout graph context in deskops/services/closeout_gates.py, and the graph tests listed below, which may be updated for the id change. Edges sldb cannot provide stay local: diagram `source:` edges (`_diagram_source_declarations`), section-declared atom refs (`_section_declarations`), YAML-fenced atom declarations in bodies (`_atom_declarations`, extract_edges.py:244), the per-line path scanner, and frontmatter fields of models that declare no `__references__`/`__containment__` (today MaterializationContractDoc's `source_atoms` and `target_identity`, read by `_declarations_from_mapping`, pinned by tests/test_materialization_contract.py:163), and the frontmatter edges of documents the store does not track (drawer tasks and any other untracked desk document; .sldb/core/documents/ holds only tracked ones), which keep the local extraction. Out of scope: the coverage extractor. Other code and fixtures that hard-code old ids are updated in this task: deskops/graph/self_reflection.py:164,173,450, deskops/operations.py:1304,1863 (or their moved copies), deskops/cli/parser.py:323, tests/fixtures/knowledge_graph/static_desk_source_graph.json and tests/test_graph_extract_docs.py:48-53.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Before changing anything, save `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt` (a committed artifact).
2. Switch declared-field edges to sldb; keep the local edges named in Scope.
3. Keep today's edge roles: the local extractor uses the declaring field name as the role (for example `depends_on`, `pills`, tests/test_graph_declared_edges.py:78-92), while sldb emits `references`/`contains` with the field in its metadata; map each sldb edge back to role = its `field`, so roles do not change. Rename node ids; update tests/fixtures/golden/graph_snapshot.kg.json and the graph tests for the id change only (anything else that changes is a regression to fix), and write the old->new id table to runs/planning/graph-id-mapping.md.
4. `graph missing` must report the same set of dangling references as the baseline: compare the sets of (kind, mapped source id, mapped target id) tuples, ignoring order.

## Validation

_List the checks required before this task can close._

- pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py
- deskops graph missing --root .
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

extract_edges.py no longer parses the declared reference fields of store-tracked documents (the local cases listed in Scope remain), the dangling-reference set matches the baseline modulo the id mapping, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
