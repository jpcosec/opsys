---
id: feature-atom-model-kinds-and-question-facets
status: proposed
tags:
- system:deskops
- topic:atoms
- topic:knowledge-model
---

# Atom model kinds and question facets

## Goal

Improve the atom model so 5WH1+ questions remain useful for retrieval without forcing every atom to be authored as a direct answer to a single question.

## Why

Questions are useful indexing facets, but they are not always the best primary shape for knowledge. Some atoms are definitions, boundaries, decisions, constraints, patterns, failure modes, procedures, or observations.

## Proposed Shape

- Add an explicit atom `kind`, such as `definition`, `principle`, `boundary`, `decision`, `constraint`, `pattern`, `failure_mode`, `procedure`, or `observation`.
- Replace the single `five_wh_one_plus` field with question facets such as `questions: [what, where]`.
- Keep the atom body focused on the natural knowledge shape, for example `## Claim` and `## Consequence`, or a single concise content section.
- Preserve simple retrieval through tags and graph relations.

## Validation

- Existing atoms can be migrated without losing meaning.
- KGDB can query by atom kind and question facets.
- New atom authoring feels less forced than single-question answering.
