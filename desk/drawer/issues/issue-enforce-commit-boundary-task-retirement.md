# Enforce commit boundary task retirement rule

## Kind

feature

## Status

open

## Problem

A task is currently often considered "done" and retired simply because the code works and tests pass. Without a strong completion boundary, a subagent or worker might make a bad change that is difficult to untangle or audit later. This weakens the safe supervised workflow model.

## Desired Outcome

Implement and enforce a strict "commit boundary" rule for task retirement. A task is not ready for retirement until:
1. The scoped implementation exists.
2. The relevant tests pass.
3. Closeout evidence is written to disk.
4. The change is ready to commit.
5. The result is secured by a git commit boundary.

Only after this boundary is secured should the task be removed from active planning surfaces (e.g., deleting the task file and removing it from the board).

## Questions

- How can the `deskops` CLI or closeout rituals programmatically verify that a commit boundary has been created for the task?
- Should the `deskops closeout` command automatically stage or commit the changes if evidence passes?
- How do we handle tasks that result in exploratory artifacts rather than codebase changes?

## Follow-Up Shape

- Update `desk/rituals/closeout.md` to require a commit boundary.
- Implement checks in `deskops` routines to ensure git status is clean or commits are mapped to tasks before retirement.
- Document the retirement order in the task lifecycle atoms.

## Related Atoms

- atom-every-change-needs-descriptive-commit
- atom-code-changes-close-with-tests-and-commit
