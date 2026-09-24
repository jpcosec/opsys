---
# pill-xxx
id: pill-real-cli-surfaces-prove-operator-contracts
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:pattern
- topic:cli
- topic:validation
---

# Pattern: real CLI surfaces prove operator contracts

## What

_Define the context or guardrail this pill carries._

Validate CLI-facing workflow changes through the real `deskops` commands that operators and sibling tools will use, not only through reconstructed Python objects or assumed internal behavior.

## Why

_Explain why this context matters for safe execution._

The executable command path is part of the user contract. A feature that works only in isolated internals but fails through parser, normalization, rendering, or exit-code behavior is not actually proven.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes CLI grammar, command output, list/show behavior, promotion flows, closeout flows, doctor/status flows, or other user-facing deskops commands.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `deskops/cli/`, `deskops/operations.py`, `tests/test_cli.py`, command help, and any docs that describe operator-facing command behavior.

## How

_Describe the correct way to apply this guidance._

Run the real command path, assert user-visible output and exit behavior, and keep at least one CLI-level validation in the task's evidence when the task changes a user-facing workflow surface.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat direct Python helper coverage as sufficient proof of a CLI contract. Do not assume parser or command wiring correctness just because lower-level objects behaved as expected.
