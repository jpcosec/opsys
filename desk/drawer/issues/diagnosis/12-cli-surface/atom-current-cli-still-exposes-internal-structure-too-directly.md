---
id: atom-current-cli-still-exposes-internal-structure-too-directly
title: Current CLI still exposes internal structure too directly
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:cli-surface
type: atom
description: Diagnosis of why CLI simplification and output shaping remain active work.
---

# Current CLI still exposes internal structure too directly

## Answer

The current CLI still reflects internal artifact and implementation structure more directly than an operator-facing workflow language should. That makes both human use and machine composition harder than necessary, and it increases the amount of explanatory documentation needed around command behavior.

## Related Tasks

- `desk/tasks/task-design-operational-cli-grammar.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `desk/tasks/task-design-operational-cli-grammar.md` — explicitly aims to align commands with spoken workflow nouns and user intent.
- `desk/tasks/task-add-json-output-for-modeled-documents.md` — explicitly aims to make list/show surfaces scriptable.
- `desk/drawer/issues/issue-make-deskops-easy-to-use.md` — notes that the model is powerful but concept-heavy for first use.
