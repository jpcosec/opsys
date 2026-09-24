---
# pill-xxx
id: pill-011
# e.g., language:python, library:pydantic
tags:
- system:deskops
- pill-type:guardrail
- topic:self-reflection
- topic:knowledge-graph
- topic:drift-control
---

# Guardrail: self reflection must avoid noisy generation

## What

_Define the context or guardrail this pill carries._

Self-reflection should produce high-signal atoms, issues, or routed questions from graph findings, not bulk-generated guesses.

## Why

_Explain why this context matters for safe execution._

If every weak graph inference becomes an atom or issue, the knowledge base becomes noisy and harder to trust. Self-reflection must distinguish missing evidence from durable knowledge.

## When

_Describe when an agent should apply this pill._

Apply this pill to self-reflection routines, graph missing checks, stale relation checks, and automatic issue/atom creation.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/tasks/*self-reflection*.md`, future graph/reflection commands, and any generated inbox or drawer output.

## How

_Describe the correct way to apply this guidance._

Require confidence, provenance, and dedupe before writing new atoms or issues. Prefer reviewable findings when uncertainty is high. Route unclear cross-tool questions to the owning repo inbox.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not create atoms from low-confidence graph gaps. Do not open duplicate issues for the same missing relation. Do not silently mutate source artifacts during a reflection-only task.
