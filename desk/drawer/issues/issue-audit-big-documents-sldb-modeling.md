# Audit big documents SLDB modeling

## Kind

feature

## Status

open

## Problem

Large documents such as README, FAQ, knowledge materialization docs, and diagram explanations are not clearly classified as shallow SLDB documents, composed atom materializations, strict typed documents, or unmodeled prose.

## Desired Outcome

Inventory the big documents and decide their model strategy: shallow body, composed materialization, typed sections, generated projection, or intentionally unmodeled.

## Questions

- Which large docs must be tracked by SLDB now?
- Which big docs should declare source atoms and materialization metadata?
- When does a large document need typed sections instead of a shallow body?

## Related Atoms

- atom-big-documents-need-explicit-modeling-strategy
- atom-main-docs-are-composed-materializations
- atom-materialization-contracts-bind-source-output-validation

---

## Merged item: `atom-composition-documents-through-sldb`

#### Issue

Large documents should be materializations/compositions of atoms through `sldb`, but the concrete composition contract is not defined yet.

#### Core Need

Define how a larger document declares and renders the atoms it composes without pushing outgoing references into the atom itself.

#### Constraints

- Atoms do not point outward.
- Large documents declare their own composition.
- Composition should use `sldb` mechanisms such as model fields, `__compositions__`, links, or a sidecar composition document.
- The result must be roundtrippable and testable.

#### Follow-Up Shape

- Create or identify a document model for composed atom documents.
- Add a composition test that renders a document from multiple `AtomDoc` files.
- Decide whether atom references live in frontmatter fields, body links, or a dedicated composition spec.

#### Tags

- system:deskops
- system:sldb
- topic:atoms
- topic:composition
