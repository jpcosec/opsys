---
id: task-derived-atom-trace-index
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
- deskops/graph/atom_trace.py
- docs/knowledge-graph/desk-source-graph-vocabulary.md
- tests/test_graph_atom_trace.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Add a derived atom use-site index

## Rationale

_Explain why this task exists or the business driver behind it._

Atoms must not carry outgoing use-site lists, but users still need to answer which docs, tasks,
tests, and diagrams reference a given atom. The graph already extracts declared atom edges.

## Goal

_Describe the concrete result this task must produce._

Provide a read-only `atom_use_sites(root, atom_id)` helper that derives reverse traceability from
`extract_declared_edges`, plus a test proving that no atom document is mutated.

## Scope

_State what is in scope and what is out of scope._

In scope: one graph helper module and one test. Out of scope: a new CLI command, a persisted index,
prose-only scan support, and any atom or document rewrite.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `deskops/graph/atom_trace.py` with an immutable `AtomUseSite` dataclass
   (`source_id`, `role`, `path`, `locator`) and
   `atom_use_sites(root: Path, atom_id: str) -> list[AtomUseSite]`.
2. Implement it by calling `extract_declared_edges(root)` and filtering edges whose
   `target_id == f"atom:{atom_id.removeprefix('atom:')}"`; sort by `(path, locator)`.
3. Do not read or write `desk/atoms/**`; the helper is a projection over extracted edges.
4. Add `tests/test_graph_atom_trace.py` with a temporary root containing one AtomDoc and one
   Markdown doc with `atoms: [{id: atom-..., role: documents}]`. Assert the use site reports the
   doc path and `documents` role, and assert the atom file bytes are unchanged.
5. Add a second test with a task that has `atoms: [atom-...]` and assert the task source is found.
6. Add a short paragraph to `docs/knowledge-graph/desk-source-graph-vocabulary.md` stating that
   reverse atom traceability is derived from declared edges and is not stored in atoms.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_graph_atom_trace.py -q
- python -m pytest tests/test_graph_extract_edges.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

`atom_use_sites` returns doc and task use sites from declared edges, the atom file is byte-identical
after the call, and the new tests pass.
