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

Desk health is measured through deskops doctor, which classifies the workspace as absent, empty, legacy or current and reports missing desk structure (desk/, tasks/Board.md, drawer/, rituals/phase.md), untracked modeled documents, documents the model cannot read, invalid documents, an unreadable store index, and unregistered deskops models. --repair scaffolds missing structure and registers missing models; document tracking and content repairs are reported for manual follow-up.

## Diagnostic Surface

`deskops doctor` reports:
1. **Missing desk structure** — `desk/`, `desk/tasks/Board.md`, `desk/drawer/`, `desk/rituals/phase.md`
2. **Untracked desk documents** — Markdown files in `desk/` not registered in `.sldb`
3. **Unreadable desk documents** — Modeled documents whose current text does not extract their fields
4. **Invalid desk documents** — Documents with malformed YAML, missing required fields, or validation errors
5. **Unreadable store index** — Local store index records doctor cannot load
6. **Unregistered deskops models** — Deskops models missing from the local store

## Repairability

| Finding | Auto-repair | Manual required |
|---------|-------------|-----------------|
| Missing structure | Scaffold with `deskops doctor --repair` | — |
| Unregistered models | Register with `deskops doctor --repair` | — |
| Untracked docs | Report only | Use `sldb docs track` |
| Unreadable or invalid docs | Report only | Fix the text or run `sldb stores update` |

## Evidence

`deskops/cli/commands/doctor.py` — `DoctorCLI.run()` method implements these checks.

## Tags

- system:deskops
- topic:workspace-health
- topic:diagnosis
- topic:cli
