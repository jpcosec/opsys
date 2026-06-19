---
id: pill-list-surfaces-must-expose-malformed-docs
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:list
- topic:data-integrity
---

# Guardrail: list surfaces must expose malformed docs

## What

Treat malformed modeled documents as visible findings, not as items to skip silently during list operations.

## Why

A list command that hides bad documents creates false confidence about the health of the desk and makes recovery harder.

## When

Apply this pill whenever a task changes `deskops list`, document loading, directory scans, or first-use behavior for partially broken desks.

## Where

Applies to list surfaces for tasks, routines, artifacts, and primitives, plus malformed frontmatter and invalid model payload handling.

## How

Keep empty and first-use states friendly, but surface malformed entries with clear location and failure information so repair work can start immediately.

## How Not

Do not let invalid docs disappear from the operator's field of view. Do not confuse "empty" with "failed to parse".
