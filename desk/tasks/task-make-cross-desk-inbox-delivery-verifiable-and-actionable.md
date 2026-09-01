---
id: task-make-cross-desk-inbox-delivery-verifiable-and-actionable
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-make-cross-desk-inbox-delivery-verifiable-and-actionable
current_node: checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-closeout-ready
history:
- operator-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-activate
- operator-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-ready-for-testing
references:
- ad86203
- tests/test_cli.py
- atom:atom-cross-desk-inbox-delivery-is-verifiable-and-acknowledgeable
depends_on: []
pills:
- desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md
- desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files: []
checklists:
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-execution-ready
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-testing-ready
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-cross-desk-inbox-delivery-is-verifiable-and-acknowledgeable
closeout_evidence_verified: true
pill_graduation_verified: true
---

# Make cross-desk inbox delivery verifiable and actionable

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make cross-desk inbox communication operationally useful by ensuring the sender, target, delivery result, and follow-up path are explicit across project desks.

## Scope

_State what is in scope and what is out of scope._

- define what successful cross-desk inbox delivery must prove
- require clear sender and target identity instead of inferred ambiguity
- decide how recipients discover, acknowledge, or pull pending cross-desk updates
- design a reply or follow-up path so inbox notes do not become write-only dead drops
- identify the minimum implementation slice needed before inbox can be treated as a real horizontal coordination surface

## Implementation Path

_Outline the expected implementation route or affected surface._

- Successful delivery = target desk resolved via canonical identity resolver (deskops/identity.py, from Wave A) AND note written AND note tracked/validated AND a verification result echoed to sender (resolved sender + target + path).
- Sender/target: consume the shared identity resolver; fail loudly on ambiguous/unresolvable identity instead of falling back to cwd().name. Add optional `--sender` override.
- Model: extend InboxNoteDoc with OPTIONAL, defaulted fields `target_project` and `acknowledged_by`/`acknowledged_at` (backward compatible; existing notes still validate). Mirror defaults in cli/model_introspection.py.
- Delivery result: honor `--format {text,json,yaml}`; non-zero exit if delivery cannot be verified.
- Follow-up: implement a single ACK action `deskops inbox --ack <selector>` that flips status open->closed and records ack metadata. Reply-threading / writing back to sender desk is OUT (defer to drawer).
- Route any discovered CLI gaps to desk/drawer/tasks/ per pill-cli-gaps-become-tracked-work.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
