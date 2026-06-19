---
id: pill-drift-checks-are-review-surfaces-not-mutators
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:drift
- topic:review
---

# Guardrail: drift checks are review surfaces, not mutators

## What

Treat drift detection as a review surface that emits findings, evidence, and promotion paths, not as a command that rewrites durable knowledge automatically.

## Why

Drift signals are often partial, heuristic, or confidence-weighted. They are useful for routing work, but dangerous as silent mutation triggers.

## When

Apply this pill whenever a task designs drift checks, graph reflection outputs, or review records that compare atoms, docs, tests, diagrams, and implementation surfaces.

## Where

Applies to drift CLI design, finding storage, review workflows, and any future automation that proposes follow-up tasks, questions, or atom updates.

## How

Emit provenance-backed findings, include confidence and dedupe keys, and route accepted work through explicit human-reviewed promotions.

## How Not

Do not let drift tooling rewrite docs, atoms, or graph links just because a heuristic matched. Do not collapse review, decision, and mutation into one implicit step.
