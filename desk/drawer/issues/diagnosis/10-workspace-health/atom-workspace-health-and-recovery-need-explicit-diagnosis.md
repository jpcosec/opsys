---
id: atom-workspace-health-and-recovery-need-explicit-diagnosis
title: Workspace health and recovery need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
type: atom
description: Summary diagnosis for workspace health, recovery, and migration concerns.
---

# Workspace health and recovery need explicit diagnosis

## Answer

The active board already treats desk health, recovery, legacy migration, and per-project version/config contracts as important work, but the diagnosis tree does not yet capture them as a first-class architectural problem family. That leaves a gap between implementation pressure and explicit understanding of why workspace state remains fragile.

## Related Tasks

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`
- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md`
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md`

## Evidence

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md` — targets broken desk states, invalid modeled documents, and stale runtime files.
- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md` — targets incompatible and hand-rolled desk layouts.
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md` — targets explicit version/config contracts for safe per-project behavior.
