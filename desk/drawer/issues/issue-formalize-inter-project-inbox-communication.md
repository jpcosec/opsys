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

---

## Merged item: `add-upstream-inbox-routing-command`

#### Kind

feature

#### Status

open

#### Problem

The workflow says failed SLDB and spec2viz paths should become sibling repo inbox issues, but agents currently have to hand-write those notes.

#### Desired Outcome

Provide a deskops command or helper that writes a structured inbox note to the owning sibling repo after confirming the target project and issue kind.

#### Questions

- Should this command know sibling repo locations from the registry?
- Should it support `sldb`, `spec2viz`, and arbitrary registered repos?
- Should it create inbox notes only, or also drawer issues when the target repo has no inbox convention?

#### Related Atoms

- atom-failed-sldb-paths-become-sldb-inbox-issues
- atom-upstream-routing-needs-convenient-command

---

## Merged note: `20260621-034342-unclear-clarify-inbox-model-for-inter-project-communication.md`

### Clarify inbox model for inter-project communication

I currently understand the deskops inbox only partially for inter-project communication. From the visible CLI/help, inbox appears to be a structured message intake surface for cross-project requests, clarifications, suggestions, and handoff-like communication, with  likely moving inbox material into more formal workflow artifacts. However, the intended inter-project communication model is still not explicit enough. Please document: (1) when to use Provide a message or use --list/--show. vs ; (2) expected conventions for sender/receiver projects; (3) how inbox items should be phrased for actionability; (4) the lifecycle from inbox -> promote -> task/pill/doc or closure; (5) how to distinguish local notes from true inter-project messages; and (6) examples of good inbox hygiene for cross-project coordination.
