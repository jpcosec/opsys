# Formalize inter-project inbox communication API

## Kind

feature

## Status

open

## Problem

The current `desk/inbox/` is used primarily as a local scratchpad. However, in multi-repository ecosystems, projects need a formal way to drop actionable suggestions, cross-repo bug reports, or hand-offs into each other's workspaces without relying on external issue trackers. The existing model for this is partially present but lacks formal contracts for sender routing and status tracking.

## Desired Outcome

Treat the `inbox` as a first-class API for cross-repository orchestration.
- Define a structured YAML frontmatter for inbox notes (e.g., `sender_project`, `kind: suggestion | error | clarification`, `status: open | closed`).
- Standardize the lifecycle from `inbox -> promote -> task/pill/doc` or closure.
- Establish guidelines on how to phrase cross-project inbox items for immediate actionability.

## Questions

- How do we automate delivery of an inbox note from Repo A to Repo B using `deskops`?
- Do we need an outbox/inbox synchronization mechanism?
- How do we verify delivery and notify the sender project when an item is promoted or closed?

## Follow-Up Shape

- Document the inter-project inbox communication model.
- Add `sender_project`, `kind`, and `status` fields to the `sldb` schema for inbox items.
- Update `deskops inbox` commands to filter by sender and status.

## Related Atoms

- atom-inbox-routes-external-needs-toward-work
- atom-inbox-is-coordination-intake
