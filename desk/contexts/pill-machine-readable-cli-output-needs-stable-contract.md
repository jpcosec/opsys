---
id: pill-machine-readable-cli-output-needs-stable-contract
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:cli
- topic:serialization
---

# Guardrail: machine-readable CLI output needs a stable contract

## What

Treat JSON or YAML CLI output as a compatibility surface with its own explicit contract.

## Why

Once users or sibling tools parse `deskops list` or `deskops show`, small presentation changes become behavioral breaks even if human-readable text still looks acceptable.

## When

Apply this pill whenever a task adds `--format json|yaml`, changes modeled document output, or exposes workflow data to scripts.

## Where

Applies to parser flags, serialization helpers, list/show commands, and regression tests for structured CLI output.

## How

Define stable field names, preserve explicit document identity, and test parseability with real CLI output rather than reconstructed Python objects.

## How Not

Do not treat JSON output as a thin debug dump. Do not let human-formatting shortcuts silently redefine the machine contract.
