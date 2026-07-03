---
id: atom-frontmatter-becomes-reading-noise-when-sldb-is-underused
title: Frontmatter becomes reading noise when SLDB is underused
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:symptoms
type: atom
description: Symptom explaining why the current reading path feels heavy.
---

# Frontmatter becomes reading noise when SLDB is underused

## Answer

Frontmatter is valuable as structured metadata for indexing, validation, and field access, but it becomes reading noise when the operational path repeatedly consumes whole Markdown files instead of retrieving only the needed fields or a composed view. This symptom indicates the structured layer is not acting as the primary interface.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `spec/artifacts/atom.yaml` — atom docs carry structured fields like title, five_wh_one_plus, and answer in a modeled document format.
- `.skills/sldb/SKILL.md` — suggests those fields should be queried or composed structurally instead of always reading whole Markdown files.
- Current atom materializations under `desk/atoms/` expose frontmatter plus rendered body, which is useful for humans but heavy as the default operational read path.
