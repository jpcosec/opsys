# Separate opsys as the workflow domain instance above sldb and specyaml

ID: feature-008
Status: promoted

## Goal

Split the current workflow work into an explicit opsys domain instance so sldb remains infra, specyaml remains the semantic contract, and workflow-specific models plus routines live in their own layer.

## Why

Right now the workflow domain is bleeding into sldb itself. Without a separate opsys layer, it is hard to tell which parts are reusable infrastructure, which parts are canonical semantics, and which parts are just this repo's operating system.

## Scope

In scope: defining opsys as the workflow-domain instance, deciding what moves out of sldb into opsys, and clarifying the boundaries between sldb infra, specyaml semantics, and opsys-specific models and routines. Out of scope: fully migrating every file immediately.

## Proposed Shape

Introduce opsys as the domain layer above sldb and specyaml. Keep sldb responsible for structured document infrastructure, keep specyaml responsible for canonical semantic contracts, and move workflow-specific models such as desk, drawer, tasks, pills, rituals, atoms, edges, and materializers into opsys.

## Adoption Path

Promoted into active execution and now represented by the standalone `opsys` repo separation from `sldb`.

## Validation

- The responsibilities of sldb, specyaml, and opsys are explicitly separated.
- The workflow-specific models that should move into opsys are enumerated.
- The new split is concrete enough to drive follow-up implementation tasks.

## Tags

- system:sldb
- workspace:drawer
- topic:opsys
- topic:architecture
- topic:separation
