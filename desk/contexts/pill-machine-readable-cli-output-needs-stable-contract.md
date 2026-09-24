---
# pill-xxx
id: pill-machine-readable-cli-output-needs-stable-contract
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:cli
- topic:serialization
---

# Guardrail: machine-readable CLI output needs a stable contract

## What

_Define the context or guardrail this pill carries._

Treat JSON or YAML CLI output as a compatibility surface with its own explicit contract.

## Why

_Explain why this context matters for safe execution._

Once users or sibling tools parse `deskops list` or `deskops show`, small presentation changes become behavioral breaks even if human-readable text still looks acceptable.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task adds `--format json|yaml`, changes modeled document output, or exposes workflow data to scripts.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to parser flags, serialization helpers, list/show commands, and regression tests for structured CLI output.

## How

_Describe the correct way to apply this guidance._

Define stable field names, preserve explicit document identity, and test parseability with real CLI output rather than reconstructed Python objects.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat JSON output as a thin debug dump. Do not let human-formatting shortcuts silently redefine the machine contract.
