---
# pill-xxx
id: pill-project-local-config-carries-version-and-sandbox-policy
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:config
- topic:versioning
---

# Guardrail: project-local config carries version and sandbox policy

## What

_Define the context or guardrail this pill carries._

Treat per-project desk configuration as a first-class contract: it should declare the desk's canonical identity inputs, version expectations, and default testing/sandbox policy for that repo.

## Why

_Explain why this context matters for safe execution._

Global environment variables and implicit local heuristics do not explain which desk format a repo expects, how a legacy desk should be upgraded, or whether mutating CLI work should land in the real desk or a sandbox for that project.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes desk root resolution, testing sandbox behavior, desk migration/version handling, or repo-local workflow defaults.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to CLI root/config resolution, per-project desk metadata, upgrade planning, and cross-desk identity or targeting flows.

## How

_Describe the correct way to apply this guidance._

Use one tracked project config for shared behavior and one optional local override for machine-specific settings. Put durable desk/version expectations in the tracked file and keep disposable local testing choices out of shared history unless the repo wants them as policy.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not rely only on shell-global environment variables for repo-specific behavior. Do not hide shared migration expectations in ignored local config.
