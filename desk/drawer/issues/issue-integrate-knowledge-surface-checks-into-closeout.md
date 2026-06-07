# Integrate knowledge surface checks into closeout

## Kind

feature

## Status

open

## Problem

The closeout ritual checks tests, pills, board cleanup, store cleanup, and commit discipline, but it does not yet explicitly check atom references, materializations, diagram source rules, upstream gaps, source artifact deletion, or git tracking intent.

## Desired Outcome

Update closeout once the atom reference and materialization conventions exist so every task closes with knowledge surfaces consistent or follow-up work captured.

## Questions

- Which checks are mandatory gates versus advisory prompts?
- Should closeout require all new atoms to be referenced by at least one materialization or follow-up issue?
- How should untracked files be classified without trampling user work?

## Related Atoms

- atom-closeout-validates-knowledge-surfaces
- atom-git-is-explanatory-surface-for-changes
- atom-used-source-artifacts-are-deleted
