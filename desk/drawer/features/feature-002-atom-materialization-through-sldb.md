# Materialize atoms into specs, docs, features, tasks, and pills through SLDB

ID: feature-002
Status: promoted

## Goal

Use SLDB to turn durable conceptual atoms into phase-appropriate artifacts such as specs, docs, deferred features, executable tasks, and temporary pills without rewriting the same concept by hand each time.

## Why

Atoms capture stabilized conceptual truth, but they still need to materialize into artifacts that belong to later phases of the workflow. Without an explicit materialization system, concepts drift, duplicate themselves, and lose traceability as they move from ontology into design and execution.

## Scope

In scope: defining an AtomDoc model, defining the relationships between atoms and their materializations, deciding which target document types can be derived from an atom, and designing the SLDB commands or routines that create those derived artifacts. Out of scope: implementing every materializer immediately or forcing every document in the repo to derive from atoms from day one.

## Proposed Shape

Introduce a first-class AtomDoc surface that holds the stable conceptual core. Add typed relationships such as derived_from, materializes_into, depends_on_atoms, and stabilized_in. Let SLDB render or create target artifacts from atoms into drawers features, durable docs/specs, active desk tasks, or temporary pills. Use atoms as the semantic source, while downstream artifacts carry phase-specific fields and operational framing.

## Adoption Path

Promoted into active execution and now represented by the resulting models, materializers, proof artifacts, and git history.

## Validation

- An AtomDoc model and its required fields are clearly defined.
- The allowed materialization targets from atoms are explicit.
- Traceability from an atom to its derived docs, specs, features, tasks, and pills is represented as first-class data.
- There is a concrete migration path for proving the workflow on a small example set.

## Tags

- system:sldb
- workspace:drawer
- topic:atoms
- topic:materialization
- topic:workflow
