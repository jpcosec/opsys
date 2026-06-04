# Derive deskops CLI grammar from workflow nouns

## Issue

The old `046-052` task set proposed a fixed noun-verb CLI over many document models, but the model has shifted: CLI nouns should come from actual workflow operations, not from every available model.

## Core Need

Define a `deskops` CLI grammar where nouns are user-facing operational surfaces and verbs are meaningful actions over those surfaces.

## Constraints

- Do not expose every model just because it exists.
- Preserve existing working commands until replacements are real.
- Prefer workflow-derived nouns such as task, atom, board, routine, hook, namespace, and inbox when they have clear user value.
- Avoid deprecated assumptions from the old task set: `materializes_into`, atom lifecycle `status`, atoms in drawer, and atom-to-task/pill/feature generation.

## Follow-Up Shape

- Review current CLI commands and classify them as operational, model CRUD, or transitional.
- Define priority nouns from current workflow diagrams and atoms.
- Add parser tests for only the nouns/verbs that are intentionally exposed.

## Tags

- system:deskops
- topic:cli
- topic:workflow-model
