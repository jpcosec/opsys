---
id: task-derive-declared-graph-edges-from-model-containment-and-references
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-derive-declared-graph-edges-from-model-containment-and-references
current_node: checklist-task-derive-declared-graph-edges-from-model-containment-and-references-closeout-ready
history:
- operator-task-derive-declared-graph-edges-from-model-containment-and-references-activate
- operator-task-derive-declared-graph-edges-from-model-containment-and-references-ready-for-testing
references:
- tests/test_graph_declared_edges.py
- tests/test_graph_extract_docs.py
- 47a5816
- desk/atoms/knowledge-model/atom-sldb-semantics-are-graph-inputs.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-execution-ready
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-testing-ready
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: true
pill_graduation_verified: true
---

# Derive declared graph edges from model containment and references

## Rationale

_Explain why this task exists or the business driver behind it._

deskops graph build emits only the 282 coverage edges; the containment/references that TaskDoc, BoardDoc and RitualDoc declare reach the snapshot only as prose. The mindmap lost Task to Routine and Task to checklist edges when those models started declaring containment instead of relying on the legacy global field list.

## Goal

_Describe the concrete result this task must produce._

extract_declared_edges consumes each model's __containment__ and __references__ to emit edges for the declared fields, so a task's routine, checklists, pills and atoms and a board's tasks appear as edges in the snapshot.

## Scope

_State what is in scope and what is out of scope._

deskops/graph/extract_edges.py and the models that declare containment; tests for the snapshot. Does not change graph_ui or the KGDB contract.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/graph/extract_edges.py _declarations_from_mapping: read __containment__ and __references__ from the registered model for the document's kind, resolve each declared field value (path or id) against nodes_by_path/existing_ids, and emit declarations with the field name as role. Missing targets keep going to missing_targets.

## Validation

_List the checks required before this task can close._

- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

deskops graph build emits edges for a task's routine and checklists and for a board's tasks, and deskops graph missing does not report them as missing.
