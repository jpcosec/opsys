# Document AtomDoc and namespace workflow

## Status

open

## Issue

`AtomDoc` and atom tag namespaces now have a real implementation, but onboarding/docs do not yet explain how to use them.

## Core Need

Document how to create atoms with `deskops add atom`, how `five_wh_one_plus` works, how tag namespaces are selected, and how to add a namespace when existing ones are insufficient.

## Constraints

- Explain that namespaces are controlled but extensible.
- Explain preference for existing namespaces before adding new ones.
- Explain that `.sldb/core` is versioned and `.sldb/runtime` is ignored.
- Keep docs aligned with actual CLI behavior, not the old noun-verb proposal.

## Follow-Up Shape

- Update README or add a focused atom workflow doc.
- Include examples for `deskops add atom` and `deskops atoms add-namespace`.
- Link to the `sldb` core/runtime follow-up issue.

## Tags

- system:deskops
- topic:atoms
- topic:docs
- topic:namespaces

---

## Merged item: `migrate-or-delete-old-atom-surfaces`

#### Issue

The repo has shifted from free-form/drawer atoms to curated `AtomDoc` atoms under `desk/atoms`, but old references and surfaces may still mention `desk/drawer/atoms` or old atom fields.

#### Core Need

Remove stale atom assumptions and ensure the durable atom surface is only `desk/atoms`.

#### Constraints

- No atom drafts in drawers.
- No atom `status` field.
- No `answers` frontmatter field.
- No `related_atoms` or `materializes_into` on atoms.

#### Follow-Up Shape

- Search docs/specs/tasks for `desk/drawer/atoms`, `answers:`, `materializes_into`, `related_atoms`, and atom `status` assumptions.
- Convert durable knowledge into `desk/atoms` or delete stale material.
- Leave non-atom drafts as issues/features/conversation processing docs.

#### Tags

- system:deskops
- topic:atoms
- topic:migration
