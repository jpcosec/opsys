---
id: task-canonical-atom-reference-metadata
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
- deskops/atom_references.py
- deskops/graph/extract_edges.py
- deskops/graph/checks.py
- deskops/graph/self_reflection.py
- docs/knowledge-graph/desk-source-graph-vocabulary.md
- tests/test_atom_reference_convention.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Canonical atom reference field and role vocabulary

## Rationale

_Explain why this task exists or the business driver behind it._

The extractor accepts `atoms`, `source_atoms`, and `related_atoms`, and silently rewrites an
unknown role to `references`. The docs role catalog and the code vocabulary also disagree, so
artifacts cannot rely on one validated atom-reference convention.

## Goal

_Describe the concrete result this task must produce._

Make `atoms` the only structured artifact field for atom references, validate the five allowed
roles, and report legacy aliases and invalid roles through `deskops drift check` without adding
a hard closeout gate.

## Scope

_State what is in scope and what is out of scope._

In scope: a shared constants/parser module, extractor reuse of those constants, a drift validator,
tests, and the vocabulary doc. Out of scope: changing `MaterializationContractDoc.source_atoms`,
changing any Pydantic model contract, changing closeout gates, and building a reverse trace index.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `deskops/atom_references.py` with `CANONICAL_FIELD = "atoms"`,
   `LEGACY_FIELDS = ("related_atoms",)`, `MATERIALIZATION_FIELD = "source_atoms"`,
   `ALLOWED_ROLES = ("references", "documents", "specifies", "constrains", "validates")`, and
   `DEFAULT_ROLE = "references"`.
2. Add one parser that accepts a string or `{id, role}` mapping and returns `(atom_id, role, field_name)`.
   Return an explicit violation for an unknown role; do not fall back silently in the validator.
3. Replace the local constants in `deskops/graph/extract_edges.py` with imports from the new module.
   Keep its current graph behavior stable (an invalid role may still map to `references` while
   extraction continues), because the drift validator is the reporting surface.
4. Add `find_atom_reference_violations(root)` to `deskops/graph/checks.py`. It reads Markdown
   frontmatter only under `desk/` and `docs/`, and emits findings for
   `invalid_atom_reference_role` and `legacy_atom_reference_field`. Do not scan fenced YAML:
   issue and doc examples contain candidate shapes that are not declarations.
5. Append those findings in `drift_check_knowledge_surfaces` in
   `deskops/graph/self_reflection.py`, formatted as `atom-reference: <path>#<locator> ...`.
6. Update `docs/knowledge-graph/desk-source-graph-vocabulary.md` so the atom-reference role row
   points at the five-role vocabulary and states that `atoms` is the canonical field.
7. Add `tests/test_atom_reference_convention.py`: valid roles pass; an unknown role produces one
   finding; `related_atoms` produces one legacy finding; a bare string maps to `references`.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_atom_reference_convention.py -q
- python -m pytest tests/test_graph_extract_edges.py tests/test_graph_self_reflection.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

`atoms` is the documented canonical field, the five roles are defined once, invalid roles and
`related_atoms` appear as `deskops drift check` findings, and all listed tests pass.
