# Define desk source graph vocabulary

## Kind

feature

## Status

open

## Problem

The graph needs a typed vocabulary for desk artifacts and source files before KGDB can be used safely. Without a small controlled vocabulary, graph edges become inconsistent prose labels.

## Desired Outcome

Define the first node kinds, edge roles, identifier formats, and provenance metadata for the desk/source knowledge graph.

## Candidate Node Kinds

- atom
- task
- issue
- doc
- diagram
- spec
- primitive
- sldb_model
- cli_command
- source_file
- test_file
- config_file

## Candidate Edge Roles

- materializes
- references
- validates
- implements
- invokes
- defines
- routes
- configures
- tests
- generated_from
- source_for
- violates

## Questions

- Which names must match KGDB contracts exactly?
- Which relation roles overlap with existing atom reference roles?
- Should ontology/OWL mapping be stored now as metadata, or deferred until after the property graph is useful?

## Related Atoms

- atom-knowledge-graph-connects-desk-and-source-files
- atom-atom-references-carry-roles
- atom-extensibility-is-a-contract
