---
# pill-xxx
id: pill-cross-desk-inbox-needs-delivery-verification-and-follow-up
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:inbox
- topic:cross-repo
---

# Guardrail: cross-desk inbox needs delivery verification and follow-up

## What

_Define the context or guardrail this pill carries._

Treat cross-desk inbox as a coordination surface, not just a remote file write.

## Why

_Explain why this context matters for safe execution._

An inbox message between desks is operationally weak if the sender identity is ambiguous, the target path is guessed, delivery is not verifiable, or the receiving repo has no explicit follow-up path.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes `deskops inbox`, repo-targeted desk delivery, inbox synchronization, or horizontal desk coordination flows.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `deskops/cli/commands/inbox.py`, repo registry resolution, future desk update/sync flows, and any design for cross-desk replies or acknowledgements.

## How

_Describe the correct way to apply this guidance._

Require explicit sender and target resolution, define what counts as successful delivery, and make the receiving desk expose a discoverable next step such as sync, acknowledgement, routing, or reply handling.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not call cross-desk inbox done just because a markdown note appeared somewhere on disk. Do not leave remote notes as write-only dead drops with no verification or recipient workflow.
