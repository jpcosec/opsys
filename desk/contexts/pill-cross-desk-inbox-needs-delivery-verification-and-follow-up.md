---
id: pill-cross-desk-inbox-needs-delivery-verification-and-follow-up
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:inbox
- topic:cross-repo
---

# Guardrail: cross-desk inbox needs delivery verification and follow-up

## What

Treat cross-desk inbox as a coordination surface, not just a remote file write.

## Why

An inbox message between desks is operationally weak if the sender identity is ambiguous, the target path is guessed, delivery is not verifiable, or the receiving repo has no explicit follow-up path.

## When

Apply this pill whenever a task changes `deskops inbox`, repo-targeted desk delivery, inbox synchronization, or horizontal desk coordination flows.

## Where

Applies to `deskops/cli/commands/inbox.py`, repo registry resolution, future desk update/sync flows, and any design for cross-desk replies or acknowledgements.

## How

Require explicit sender and target resolution, define what counts as successful delivery, and make the receiving desk expose a discoverable next step such as sync, acknowledgement, routing, or reply handling.

## How Not

Do not call cross-desk inbox done just because a markdown note appeared somewhere on disk. Do not leave remote notes as write-only dead drops with no verification or recipient workflow.
