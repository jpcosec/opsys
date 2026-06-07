# Define materialization contract

## Kind

feature

## Status

open

## Problem

The knowledge materialization model says atoms become docs, specs, diagrams, tests, and tasks, but there is no contract that names source atoms, target artifact, transformation intent, and validation.

## Desired Outcome

Define a minimal materialization contract for one proof slice, then apply it to `docs/knowledge-materialization-model.md` and its diagram.

Candidate shape:

```yaml
materialization:
  source_atoms:
    - atom-atoms-distill-project-knowledge
    - atom-docs-materialize-atoms-for-humans
  output_kind: main_doc
  output: docs/knowledge-materialization-model.md
  validates_with:
    - pytest tests/test_atom_tags.py
```

## Questions

- Is the contract embedded in the artifact, stored beside it, or generated into an index?
- Should materialization contracts be SLDB documents?
- How should stale materializations be detected cheaply?

## Related Atoms

- atom-materialization-contracts-bind-source-output-validation
- atom-main-docs-are-composed-materializations
- atom-drift-checks-compare-atoms-materializations-implementation
