---
id: atom-cli-surface-and-scriptability-need-explicit-diagnosis
title: CLI surface and scriptability need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:cli-surface
type: atom
description: Summary diagnosis for CLI grammar and machine-readable output gaps.
---

# CLI surface and scriptability need explicit diagnosis

## Answer

The active board already treats command grammar and JSON output as active work, which shows the current CLI surface is not yet fully aligned with spoken workflow language or machine-composable usage. The diagnosis tree should capture this as its own problem family rather than only as a side effect of other architectural concerns.

## Related Tasks

- `desk/tasks/task-design-operational-cli-grammar.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

## Evidence

- `desk/tasks/task-design-operational-cli-grammar.md` — targets a clearer workflow-oriented command language.
- `desk/tasks/task-add-json-output-for-modeled-documents.md` — targets scriptable output for modeled surfaces.
- `docs/faq.md` and `README.md` — already spend significant effort explaining command usage and boundaries.
