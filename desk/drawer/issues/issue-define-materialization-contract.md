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

---

## Merged item: `slice-current-materialization-worktree`

#### Kind

chore

#### Status

open

#### Problem

The current workspace contains many related additions, deletions, and migrations across atoms, docs, diagrams, SLDB core files, tests, and generated/stale field surfaces. Git can explain this work only if the final changes are grouped intentionally.

#### Desired Outcome

Before closeout, classify the current worktree into explanatory slices such as field model cleanup, atom migration, knowledge materialization model, diagram cleanup, SLDB/spec2viz inbox routing, and validation changes.

#### Questions

- Which changes are user-owned and should not be staged by the agent?
- Should the current work land as one conceptual commit or several commits?
- Which generated files should remain tracked versus ignored?

#### Related Atoms

- atom-large-worktree-changes-need-explanatory-slices
- atom-git-is-explanatory-surface-for-changes
- atom-closeout-validates-knowledge-surfaces
