# Add per-project desk config and version contract

ID: task-add-per-project-desk-config-and-version-contract
Status: deferred
Priority: high

## Goal

Give each project desk one explicit local configuration contract that declares desk identity, desk/version expectations, and per-project testing defaults such as sandbox behavior.

## Scope

- tracked project config for shared desk behavior
- optional local override file for machine-specific settings
- explicit desk format or migration version
- explicit model/workflow expectation version fields
- per-project testing sandbox policy instead of shell-global heuristics
- interaction with environment overrides and explicit CLI flags

## Done When

- A project can declare its own desk/version expectations and testing defaults without relying on global shell state.
- The config makes it possible to reason about legacy desk upgrades explicitly.
- Cross-desk routing work can consume per-project identity/config instead of ad hoc path guessing.

## Suggested Pills

- `desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md`
- `desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md`
- `desk/contexts/pill-006-self-described-store-layout.md`
