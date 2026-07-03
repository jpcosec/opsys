---
id: atom-horizontal-operations-need-canonical-identity-and-verifiable-transport
title: Horizontal operations need canonical identity and verifiable transport
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:cross-desk
type: atom
description: Diagnosis of why cross-desk workflow remains unreliable.
---

# Horizontal operations need canonical identity and verifiable transport

## Answer

Cross-desk workflow remains unreliable when desk identity can be inferred ambiguously and inbox delivery behaves like a write-only drop rather than a verifiable transport. Canonical identity and explicit delivery semantics are prerequisites for treating multi-repo workflow as an operational surface instead of a best-effort convention.

## Related Tasks

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md`
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md`

## Evidence

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md` — requires reliable answers to “who am I?” and “where is that repo's desk?”.
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md` — requires sender/target identity and recipient follow-up semantics.
- `desk/drawer/issues/issue-fix-inbox-sender-project-resolution.md` — captures a concrete sender-identity failure mode.
