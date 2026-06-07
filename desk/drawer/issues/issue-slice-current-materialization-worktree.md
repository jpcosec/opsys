# Slice current materialization worktree

## Kind

chore

## Status

open

## Problem

The current workspace contains many related additions, deletions, and migrations across atoms, docs, diagrams, SLDB core files, tests, and generated/stale field surfaces. Git can explain this work only if the final changes are grouped intentionally.

## Desired Outcome

Before closeout, classify the current worktree into explanatory slices such as field model cleanup, atom migration, knowledge materialization model, diagram cleanup, SLDB/spec2viz inbox routing, and validation changes.

## Questions

- Which changes are user-owned and should not be staged by the agent?
- Should the current work land as one conceptual commit or several commits?
- Which generated files should remain tracked versus ignored?

## Related Atoms

- atom-large-worktree-changes-need-explanatory-slices
- atom-git-is-explanatory-surface-for-changes
- atom-closeout-validates-knowledge-surfaces
