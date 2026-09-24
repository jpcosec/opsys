# Define atom reference metadata convention

## Kind

feature

## Status

open

## Problem

Artifacts can mention atoms today, but there is no standard machine-readable convention for declaring which atoms an artifact uses or what role each atom plays.

## Desired Outcome

Define a minimal atom reference shape usable by docs, specs, diagrams, tasks, tests, and future indexes.

Candidate shape:

```yaml
atoms:
  - id: atom-sldb-is-read-write-edit-surface
    role: constrains
    target_kind: doc
```

## Questions

- Should the shared field be called `atoms`, `related_atoms`, `source_atoms`, or `atom_refs`?
- Which roles are allowed initially?
- Should this live as a deskops convention first or become an SLDB-level reusable reference type?

## Related Atoms

- atom-materializations-declare-source-atoms
- atom-atom-references-carry-roles
- atom-materialization-metadata-is-not-atom-content

---

## Merged item: `formalize-atom-reference-role-vocabulary`

#### Kind

feature

#### Status

open

#### Problem

`docs/diagrams/codebase/codebase-knowledge-surfaces.md` sketches atom reference metadata with `target_kind` and `role`, and `docs/diagrams/codebase/codebase-document-relation-map.md` uses relation roles on edges, but no validated vocabulary exists yet.

#### Desired Outcome

Promote the draft role and target-kind vocabulary into a small spec or model field definition that can be reused by materialization contracts, document atom references, and trace indexes.

#### Questions

- Which initial roles are canonical: `documents`, `specifies`, `constrains`, `supports`, `validates`, `implements`, `uses`, `composes`, `transcludes`, `renders`, `violates`, or a smaller set?
- Should code relations use different roles from doc/spec/diagram relations?
- Should `target_kind` describe the referencing artifact, the referenced surface, or the intended output of the relation?

#### Related Atoms

- atom-atom-references-carry-roles
- atom-documents-point-to-atoms
- atom-reverse-traceability-is-derived

---

## Merged item: `build-derived-atom-trace-index`

#### Kind

feature

#### Status

open

#### Problem

Atoms should not contain outgoing use-site lists, but users and agents still need to answer which docs, specs, diagrams, tests, tasks, or code surfaces reference each atom.

#### Desired Outcome

Build a derived read-side index or command that scans materializing artifacts and reports reverse traceability without mutating atom documents.

#### Questions

- Should the index live in `.sldb/runtime`, `.sldb/core`, `docs/`, or be generated on demand?
- Should unresolved atom references fail validation?
- Should atom references in prose count, or only structured metadata?

#### Related Atoms

- atom-reverse-traceability-is-derived
- atom-materialization-metadata-is-not-atom-content
- atom-materializations-declare-source-atoms

---

## Merged item: `atom-validation-and-traceability`

#### Issue

Atoms now have a stricter `AtomDoc` contract, but there is no project-level command or test that validates every atom and traces where composed documents use them.

#### Core Need

Provide validation and traceability for `desk/atoms/**/*.md` without reintroducing outgoing relations in atoms.

#### Constraints

- Validation should prove every atom roundtrips through `AtomDoc`.
- Trace should inspect documents/compositions that reference atoms.
- Traceability should not rely on `source-atom:*` tags produced by atom-to-task materializers.

#### Follow-Up Shape

- Add a test that loads all `desk/atoms/**/*.md` as `AtomDoc`.
- Add a read-side trace command once document-to-atom composition is defined.
- Report unresolved atom references as findings.

#### Tags

- system:deskops
- topic:atoms
- topic:validation
- topic:traceability
