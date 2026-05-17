# Make .sldb/README.md a first-class SLDB document

ID: feature-003
Status: promoted

## Goal

Define .sldb/README.md as a modeled SLDB document that explains the store from inside the store itself.

## Why

If .sldb is going to become a self-described workspace, its README cannot remain ad-hoc prose. It should be typed, queryable, and versioned through the same machinery the repo uses everywhere else.

## Scope

In scope: the model for the .sldb README, its required sections, its role as the entrypoint into the store, and the way it links to core, runtime, and .config. Out of scope: full runtime migration by itself.

## Proposed Shape

Introduce a dedicated SLDB model for .sldb/README.md with sections such as purpose, layout, git policy, runtime lifecycle, draft promotion rules, and command map. Treat it as the canonical entrypoint for understanding the store and as the first durable document inside .sldb/core.

## Adoption Path

Promoted into active execution and now represented by the tracked `.sldb/README.md` model plus its supporting code and tests.

## Validation

- The README has an explicit SLDB model.
- The README covers core, runtime, and .config boundaries.
- The README explains promotion, runtime cleanup, and git policy.
- The README can be tracked as part of the durable store layer.

## Tags

- system:sldb
- workspace:drawer
- topic:store
- topic:readme
- topic:self-hosting
