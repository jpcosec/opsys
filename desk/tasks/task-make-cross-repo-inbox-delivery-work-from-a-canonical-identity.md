---
id: task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity
current_node: checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-testing-ready
history:
- operator-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-activate
references:
- tests/test_repo_identity.py
- 9899f8f
- desk/atoms/atom-cross-desk-inbox-delivery-is-verifiable-and-acknowledgeable.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-execution-ready
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-testing-ready
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-closeout-ready
task_type: feature
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Make cross-repo inbox delivery work from a canonical identity

## Rationale

_Explain why this task exists or the business driver behind it._

Two drawer issues with one answer. issue-establish-canonical-repository-identity-through-sldb: cross-repo routing needs one path that answers 'what repo am I in' and 'how do I find another'. issue-formalize-inter-project-inbox-communication: the inbox is a first-class cross-repo API but delivery is unverifiable. This session hit both: delivering a note to sldb needed the ecosystem registry, which did not list the sender, so the note landed in the sender's own inbox instead of the target's.

## Goal

_Describe the concrete result this task must produce._

One identity path usable for both questions, and cross-repo delivery that either reaches the target or fails with the reason, with the sender able to see that the target acknowledged or closed the note.

## Scope

_State what is in scope and what is out of scope._

Identity resolution, the repo registry surface and the inbox command. Does not build an outbox or a synchronization daemon.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/identity.py holds resolve_canonical_project_identity, resolve_registered_desk and infer_sender_project_identity; deskops/cli/commands/inbox.py holds _sender_project. A desk without a registry is now its own authority (fixed this session, tests/test_repo_identity.py). Extend that to targeting: --repo must resolve through the ecosystem registry and, when it cannot, say which registry it consulted and which repos are registered, never silently deliver to the sender. Add a way for the sender to see the note's status in the target.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_repo_identity.py tests/test_inbox_promote_cli_gaps.py tests/test_cli.py -q

## Done When

_Name the observable condition that makes the task complete._

Delivering to a registered sibling repo puts the note in that repo's inbox with the right sender and target, delivering to an unregistered one fails with the registry path and the known ids, and the sender can read back the note's open/closed status.
