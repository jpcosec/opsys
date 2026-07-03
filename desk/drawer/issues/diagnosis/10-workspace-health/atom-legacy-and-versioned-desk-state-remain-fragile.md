---
id: atom-legacy-and-versioned-desk-state-remain-fragile
title: Legacy and versioned desk state remain fragile
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
type: atom
description: Diagnosis of why desk recovery and migration work keeps appearing.
---

# Legacy and versioned desk state remain fragile

## Answer

Desk state remains fragile because the project still depends on conventions that can drift across modeled docs, runtime files, legacy layouts, and version expectations. Without a stronger workspace contract and explicit recovery surface, deskops cannot reliably distinguish healthy desks, fresh desks, stale desks, and incompatible desks.

## Related Tasks

- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md`
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md`
- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`

## Evidence

- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md` — scope includes malformed current surfaces and migration/adoption paths.
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md` — scope includes explicit desk format and workflow expectation versions.
- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md` — scope includes stale runtime state and invalid desk documents.
