# Make extensibility first class

## Kind

feature

## Status

open

## Problem

Extensibility currently appears as scattered capabilities: tag namespaces, spec artifacts, generated CLI surfaces, diagram extension rules, and sibling tool routing. It is not yet a named contract with explicit extension points and tests.

## Desired Outcome

Define the first-class extension points for models, fields, artifacts, primitives, materializers, CLI commands, diagrams, atom roles, and tag namespaces.

## Questions

- Which extension points are stable public contracts?
- Which extension points are internal and allowed to change?
- What validation proves an extension does not break existing workflows?

## Related Atoms

- atom-extensibility-is-a-contract
- atom-spec-driven-artifact-architecture
- atom-self-generating-spec-derived-cli
