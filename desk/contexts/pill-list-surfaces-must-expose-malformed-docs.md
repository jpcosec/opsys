---
# pill-xxx
id: pill-list-surfaces-must-expose-malformed-docs
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:list
- topic:data-integrity
---

# Guardrail: list surfaces must expose malformed docs

## What

_Define the context or guardrail this pill carries._

Treat malformed modeled documents as visible findings, not as items to skip silently during list operations.

## Why

_Explain why this context matters for safe execution._

A list command that hides bad documents creates false confidence about the health of the desk and makes recovery harder.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes `deskops list`, document loading, directory scans, or first-use behavior for partially broken desks.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to list surfaces for tasks, routines, artifacts, and primitives, plus malformed frontmatter and invalid model payload handling.

## How

_Describe the correct way to apply this guidance._

Keep empty and first-use states friendly, but surface malformed entries with clear location and failure information so repair work can start immediately.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not let invalid docs disappear from the operator's field of view. Do not confuse "empty" with "failed to parse".
