---
id: atom-workline-introduce-deskops-compose-operations
title: Introduce deskops compose operations
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:worklines
type: atom
description: Workline for making deskops consume SLDB compositions directly.
---

# Introduce deskops compose operations

## Answer

Deskops should expose first-class compose operations for structured workflow artifacts such as atoms, tasks, and materializations. These operations should resolve documents through SLDB and return fit-for-purpose views such as minimal field bundles, execution bundles, review bundles, or human-facing composed summaries.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

## Evidence

- `.skills/sldb/SKILL.md` — provides the underlying query/compose/document operations that deskops can build on.
- `README.md` — says deskops should not duplicate document infrastructure behavior owned by SLDB.
- Existing `deskops next` behavior in `deskops/operations.py` already hints at higher-level composed views and can serve as a stepping stone.
