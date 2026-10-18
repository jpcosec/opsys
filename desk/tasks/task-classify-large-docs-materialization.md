---
id: task-classify-large-docs-materialization
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
- README.md
- docs/atoms.md
- docs/faq.md
- docs/how-to-report.md
- docs/how-to-test-ux-cli.md
- docs/knowledge-materialization-model.md
- docs/quickstart.md
- docs/sldb-templates.md
- docs/workflow-policy-reference.md
- deskops/graph/extract_docs.py
- deskops/data/faq.md
- tests/test_large_doc_materialization.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Declare composed materialization metadata for large docs

## Rationale

_Explain why this task exists or the business driver behind it._

README, the top-level docs, and the packaged FAQ are currently unclassified prose. They already
name source atoms in hand-written bullet lists, but the graph cannot read that as structured
provenance, and `deskops/data/faq.md` is an unguarded copy of `docs/faq.md`.

## Goal

_Describe the concrete result this task must produce._

Encode the audited inventory: every composed document declares `atoms:` frontmatter with role
`documents`, and `deskops/data/faq.md` is enforced as a byte-identical projection of
`docs/faq.md`.

## Scope

_State what is in scope and what is out of scope._

In scope: the ten audited files and one test. Out of scope: SLDB tracking of root/docs prose,
typed section models, materialization contracts, and changing the FAQ parser.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. For each composed document, add YAML frontmatter with an `atoms:` list. Use
   `role: documents` for every entry. Preserve the existing atom ids.
   Files: `README.md`, `docs/atoms.md`, `docs/faq.md`, `docs/how-to-report.md`,
   `docs/how-to-test-ux-cli.md`, `docs/knowledge-materialization-model.md`,
   `docs/quickstart.md`, `docs/sldb-templates.md`, `docs/workflow-policy-reference.md`.
2. Remove the now-duplicated "This ... is a human-facing materialization of these atoms" bullet
   list from each body and replace it with one sentence: `Source atoms are declared in the
   YAML frontmatter.` Keep all other prose unchanged.
3. Copy `docs/faq.md` to `deskops/data/faq.md` after its frontmatter is added. Treat
   `deskops/data/faq.md` as a projection and do not edit it independently afterward.
4. Add root `README.md` and `deskops/data/*.md` as `doc` nodes in
   `deskops/graph/extract_docs.py` when they exist, so their copied frontmatter produces declared
   edges and closeout can link both the canonical FAQ and its packaged projection.
5. Add `tests/test_large_doc_materialization.py`:
   - assert each of the nine composed paths has `atoms:` frontmatter with at least one entry;
   - assert every role is in `{"references", "documents", "specifies", "constrains", "validates"}`;
   - assert `docs/faq.md` and `deskops/data/faq.md` are byte-identical;
   - assert `extract_declared_edges` emits a `doc:<path> -> atom:<id>` edge for one doc.
6. Do not add these files to `.sldb`; the composed decision is frontmatter plus graph extraction.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_large_doc_materialization.py -q
- python -m deskops graph missing --root .
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

All nine composed documents carry structured `atoms:` frontmatter, the FAQ projection is identical
and guarded by a test, graph missing reports no new dangling atom target, and `pytest` is green.
