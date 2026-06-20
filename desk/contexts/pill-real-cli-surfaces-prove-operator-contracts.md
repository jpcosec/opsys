---
id: pill-real-cli-surfaces-prove-operator-contracts
tags:
- system:deskops
- workspace:desk
- pill-type:pattern
- topic:cli
- topic:validation
---

# Pattern: real CLI surfaces prove operator contracts

## What

Validate CLI-facing workflow changes through the real `deskops` commands that operators and sibling tools will use, not only through reconstructed Python objects or assumed internal behavior.

## Why

The executable command path is part of the user contract. A feature that works only in isolated internals but fails through parser, normalization, rendering, or exit-code behavior is not actually proven.

## When

Apply this pill whenever a task changes CLI grammar, command output, list/show behavior, promotion flows, closeout flows, doctor/status flows, or other user-facing deskops commands.

## Where

Applies to `deskops/cli/`, `deskops/operations.py`, `tests/test_cli.py`, command help, and any docs that describe operator-facing command behavior.

## How

Run the real command path, assert user-visible output and exit behavior, and keep at least one CLI-level validation in the task's evidence when the task changes a user-facing workflow surface.

## How Not

Do not treat direct Python helper coverage as sufficient proof of a CLI contract. Do not assume parser or command wiring correctness just because lower-level objects behaved as expected.
