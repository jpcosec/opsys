---
id: atom-use-case-read-atom-without-reading-full-markdown
title: Read an atom without reading full Markdown
five_wh_one_plus: when
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:use-cases
type: atom
description: Priority use case for the compose/query path.
---

# Read an atom without reading full Markdown

## Answer

A common workflow should allow deskops to retrieve just the relevant structured answer or a composed view of an atom without forcing the operator to read raw frontmatter and the whole materialized file. This use case is a direct test of whether deskops is really mounted over SLDB rather than merely coexisting beside it.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

## Evidence

- `spec/artifacts/atom.yaml` models atoms with structured fields that should support partial retrieval.
- `.skills/sldb/SKILL.md` provides commands for field-level and document-level structured access.
- Current atom files under `desk/atoms/` remain the human-facing materialization that this use case tries to avoid reading by default.
