---
id: atom-desk-health-is-measured-by-cli-diagnostics
title: Desk health is measured by CLI diagnostics
five_wh_one_plus: how
tags:
- system:deskops
- topic:workspace-health
- topic:diagnosis
- topic:cli
---

# Desk health is measured by CLI diagnostics

## Answer

Desk health is measured through deskops doctor, which separates **errors** from **alerts**. An error is something broken: the desk cannot be worked as it is, and doctor exits 1. An alert is the store having moved under an expected change (a document edited, moved or added by hand, a model contract that changed): nothing is broken, the change only has to be registered with `deskops desk update --apply`. Alerts alone exit 0 and are always printed. --repair acts on errors only.

## Diagnostic Surface

Errors (exit 1):
1. **Missing desk structure** — `desk/tasks/Board.md`, `desk/drawer/`, `desk/rituals/phase.md`
2. **Legacy desk** — no `desk/config.json`, an old `desk_format`, or a surface sldb reports in a state deskops does not know
3. **Tracked document is gone** — a tracked file deleted with no file of the same name left untracked (that pair is a move)
4. **Document its model cannot read** — any edit through the model would erase the fields it cannot extract
5. **Invalid desk document**, an unreadable store or store index, a store check that crashed, and any error sldb reports (`errors` in `stores check --format json`)
6. **Unregistered deskops models**

Alerts (exit 0, always printed):
1. **Edited** — `data_mutation` or `contract_mutation`
2. **Moved** — a tracked document gone plus an untracked one with the same file name
3. **Not tracked yet** — a modeled desk document added by hand
4. Store-wide moves — contracts changed, document lists not reindexed, and any alert sldb reports (`alerts`)

An edited or moved document never makes the desk legacy.

## Repairability

| Finding | Kind | Handled by |
|---------|------|------------|
| Missing structure | error | `deskops doctor --repair` scaffolds it |
| Unregistered models | error | `deskops doctor --repair` registers them |
| Document gone, unreadable or invalid | error | manual: restore or fix the text |
| Edited, moved, not tracked yet, store moves | alert | `deskops desk update --apply` registers them |

## Evidence

`deskops/cli/commands/doctor.py` (`DoctorCLI`) runs the checks; `deskops/doctor_findings.py` holds the error/alert rule; `tests/test_doctor_alerts.py` pins it.

## Tags

- system:deskops
- topic:workspace-health
- topic:diagnosis
- topic:cli
