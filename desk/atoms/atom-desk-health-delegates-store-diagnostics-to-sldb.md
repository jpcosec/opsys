---
id: atom-desk-health-delegates-store-diagnostics-to-sldb
title: Desk health delegates store diagnostics to SLDB
five_wh_one_plus: why
tags:
- system:deskops
- topic:workspace-health
- topic:boundary
- topic:sldb
---

# Desk health delegates store diagnostics to SLDB

## Answer

Desk health keeps desk workspace repair and SLDB store health separate. deskops doctor delegates document validity and store integrity to sldb stores check; it detects missing deskops model registrations from the store index, and owns workspace checks (desk structure, legacy classification, unmodeled and untracked documents). Desk repair does not initialize or repair the SLDB store itself.

## Boundary Rationale

- **Desk** owns workflow artifacts: tasks, boards, pills, rituals, atoms, and lifecycle documents
- **SLDB** owns document infrastructure: models, templates, fields, store indexes, validation

Mixing these concerns into one health command creates ambiguity about ownership and repair responsibility.

## Delegation Pattern

```
deskops doctor
  ├── desk structure checks  → deskops (own repair)
  ├── untracked docs         → deskops (report only)
  ├── invalid docs           → sldb stores check (report via delegation)
  └── store integrity        → sldb stores check (delegate)
```

## Evidence

`deskops/cli/commands/doctor.py` calls `sldb stores check` for document validity and propagates findings to the operator.

## Tags

- system:deskops
- topic:workspace-health
- topic:boundary
- topic:sldb
