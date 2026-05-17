# Standardize .sldb as a self-described core/runtime workspace

ID: feature-001
Status: promoted

## Goal

Restructure .sldb into a self-described workspace where durable shared knowledge lives under core, local machine overrides live under .config, and execution-time state lives under runtime.

## Why

The current store boundary mixes durable knowledge with runtime state, which makes it unclear what belongs in git and what should remain local. A self-described .sldb layout would let the repo version the durable contract while keeping runtime noise isolated.

## Scope

In scope: defining .sldb/core, .sldb/runtime, and .sldb/.config; deciding which artifacts belong in each area; and making .sldb/README.md a first-class SLDB document that explains how the store works. Out of scope: migrating every existing store artifact immediately or collapsing all runtime state into durable config.

## Proposed Shape

Use one .sldb root. Put versionable durable artifacts in .sldb/core (models, plugins, routines, policy packs, ontology layers). Put local overrides in .sldb/.config. Put ephemeral indexes, locks, temp drafts, active runtime store files, and model draft files under .sldb/runtime. Treat .sldb/README.md as a StructuredNLDoc that documents the store layout, promotion rules, and git policy from inside the store itself.

## Adoption Path

Promoted into active execution and now represented by the resulting store docs, code, tests, and git history.

## Validation

- The .sldb layout is defined with durable versus runtime boundaries.
- The README inside .sldb is specified as an SLDB document rather than plain prose.
- Git policy for .sldb/core, .sldb/runtime, and .sldb/.config is explicit.
- The migration path from the current flat store layout is concrete enough to become desk tasks.

## Tags

- system:sldb
- source-atom:atom-001
- workspace:drawer
- topic:store
- topic:runtime
- topic:core-layout
