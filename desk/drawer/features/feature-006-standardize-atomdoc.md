# Standardize AtomDoc as the durable conceptual source model

ID: feature-006
Status: promoted

## Goal

Define a first-class AtomDoc model so atoms become typed SLDB documents instead of only a folder convention.

## Why

Atom materialization will stay fuzzy until atoms themselves are formalized as a document type with stable fields, relationships, and query semantics.

## Scope

In scope: AtomDoc fields, atom taxonomy, related-concept edges, and the distinction between durable atoms and temporary pills. Out of scope: implementing all materializers immediately.

## Proposed Shape

Model atoms with stable sections parallel to the current methodology: what, why, how, when, where, and for whom, plus category, related atoms, and downstream materialization edges. Keep atoms durable and conceptual, clearly distinct from execution-time pills.

## Adoption Path

Promoted into active execution and now represented by `AtomDoc`, the example atom slice, and supporting tests.

## Validation

- AtomDoc required fields are explicit.
- Atom relationships and downstream edges are typed.
- The difference between atoms and pills is preserved in the model.
- Atoms can be queried as stable conceptual sources.

## Tags

- system:sldb
- workspace:drawer
- topic:atoms
- topic:modeling
- topic:knowledge
