# Guardrail: self reflection must avoid noisy generation

ID: pill-011

## What

Self-reflection should produce high-signal atoms, issues, or routed questions from graph findings, not bulk-generated guesses.

## Why

If every weak graph inference becomes an atom or issue, the knowledge base becomes noisy and harder to trust. Self-reflection must distinguish missing evidence from durable knowledge.

## When

Apply this pill to self-reflection routines, graph missing checks, stale relation checks, and automatic issue/atom creation.

## Where

Applies to `desk/tasks/*self-reflection*.md`, future graph/reflection commands, and any generated inbox or drawer output.

## How

Require confidence, provenance, and dedupe before writing new atoms or issues. Prefer reviewable findings when uncertainty is high. Route unclear cross-tool questions to the owning repo inbox.

## How Not

Do not create atoms from low-confidence graph gaps. Do not open duplicate issues for the same missing relation. Do not silently mutate source artifacts during a reflection-only task.

## Tags

- system:deskops
- topic:self-reflection
- topic:knowledge-graph
- topic:drift-control
