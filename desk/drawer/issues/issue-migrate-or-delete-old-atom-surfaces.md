# Migrate or delete old atom surfaces

## Issue

The repo has shifted from free-form/drawer atoms to curated `AtomDoc` atoms under `desk/atoms`, but old references and surfaces may still mention `desk/drawer/atoms` or old atom fields.

## Core Need

Remove stale atom assumptions and ensure the durable atom surface is only `desk/atoms`.

## Constraints

- No atom drafts in drawers.
- No atom `status` field.
- No `answers` frontmatter field.
- No `related_atoms` or `materializes_into` on atoms.

## Follow-Up Shape

- Search docs/specs/tasks for `desk/drawer/atoms`, `answers:`, `materializes_into`, `related_atoms`, and atom `status` assumptions.
- Convert durable knowledge into `desk/atoms` or delete stale material.
- Leave non-atom drafts as issues/features/conversation processing docs.

## Tags

- system:deskops
- topic:atoms
- topic:migration
