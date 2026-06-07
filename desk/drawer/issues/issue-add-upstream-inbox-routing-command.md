# Add upstream inbox routing command

## Kind

feature

## Status

open

## Problem

The workflow says failed SLDB and spec2viz paths should become sibling repo inbox issues, but agents currently have to hand-write those notes.

## Desired Outcome

Provide a deskops command or helper that writes a structured inbox note to the owning sibling repo after confirming the target project and issue kind.

## Questions

- Should this command know sibling repo locations from the registry?
- Should it support `sldb`, `spec2viz`, and arbitrary registered repos?
- Should it create inbox notes only, or also drawer issues when the target repo has no inbox convention?

## Related Atoms

- atom-failed-sldb-paths-become-sldb-inbox-issues
- atom-upstream-routing-needs-convenient-command
