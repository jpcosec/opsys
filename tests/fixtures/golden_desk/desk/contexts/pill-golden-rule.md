---
id: pill-golden-rule
tags:
- system:deskops
- pill-type:guardrail
- topic:golden
---

# Guardrail: golden outputs stay stable

## What

Golden files pin output contracts.

## Why

Stable outputs keep sibling tools working.

## When

Apply when serialized output changes.

## Where

Applies to tests/fixtures/golden/.

## How

Compare normalized output against committed files.

## How Not

Do not edit a golden to match a regression.
