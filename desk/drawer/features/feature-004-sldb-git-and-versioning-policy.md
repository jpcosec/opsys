# Define git and versioning policy for .sldb core, runtime, and local config

ID: feature-004
Status: promoted

## Goal

Make the versioning boundary of .sldb explicit so it is always clear what belongs in git, what stays local, and what is promoted through validation.

## Why

The store will remain confusing until the repo has a stable policy for durable versus runtime artifacts. Without that policy, contributors will keep guessing whether to commit, ignore, or regenerate store content.

## Scope

In scope: git policy for .sldb/core, .sldb/runtime, and .sldb/.config; promotion rules for drafts; and interaction between store versioning and git commits. Out of scope: implementing every migration command.

## Proposed Shape

Document and enforce a policy where .sldb/core is durable and versionable, .sldb/runtime is ephemeral and regenerated, and .sldb/.config is local override state by default. Define how model versions, temp drafts, locks, and runtime indexes should behave under git and validation workflows.

## Adoption Path

Promoted into active execution and now represented by `.gitignore`, `.sldb/README.md`, store routing, and git history.

## Validation

- The commit policy for each .sldb area is explicit.
- Draft and promotion behavior is tied to git semantics.
- Runtime-only files have a clear ignore or regeneration policy.
- Model versioning and durable contract changes have a documented lifecycle.

## Tags

- system:sldb
- workspace:drawer
- topic:store
- topic:git
- topic:versioning
