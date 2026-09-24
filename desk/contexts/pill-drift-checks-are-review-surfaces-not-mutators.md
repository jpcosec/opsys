---
# pill-xxx
id: pill-drift-checks-are-review-surfaces-not-mutators
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:drift
- topic:review
---

# Guardrail: drift checks are review surfaces, not mutators

## What

_Define the context or guardrail this pill carries._

Treat drift detection as a review surface that emits findings, evidence, and promotion paths, not as a command that rewrites durable knowledge automatically.

## Why

_Explain why this context matters for safe execution._

Drift signals are often partial, heuristic, or confidence-weighted. They are useful for routing work, but dangerous as silent mutation triggers.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task designs drift checks, graph reflection outputs, or review records that compare atoms, docs, tests, diagrams, and implementation surfaces.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to drift CLI design, finding storage, review workflows, and any future automation that proposes follow-up tasks, questions, or atom updates.

## How

_Describe the correct way to apply this guidance._

Emit provenance-backed findings, include confidence and dedupe keys, and route accepted work through explicit human-reviewed promotions.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not let drift tooling rewrite docs, atoms, or graph links just because a heuristic matched. Do not collapse review, decision, and mutation into one implicit step.
