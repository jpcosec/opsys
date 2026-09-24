---
# pill-xxx
id: pill-canonical-desk-identity-enables-horizontal-routing
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:repo-identity
- topic:cross-repo
---

# Guardrail: canonical desk identity enables horizontal routing

## What

_Define the context or guardrail this pill carries._

Treat cross-desk routing as an identity problem first: each desk needs one canonical project identity and one reliable way to resolve sibling desks from that identity.

## Why

_Explain why this context matters for safe execution._

Without canonical identity, horizontal workflow features such as inbox targeting, sender inference, repo routing, and future cross-desk promotion degrade into ambiguous path matching and first-hit heuristics.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes repo registration, sender inference, desk targeting, cross-repo task discovery, or per-project desk configuration.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `deskops/cli/commands/inbox.py`, repo registration flows, per-project config design, and any command that resolves another repo's desk.

## How

_Describe the correct way to apply this guidance._

Define one canonical identity for the current repo, fail clearly on duplicate or ambiguous matches, and make every cross-desk lookup consume that contract instead of scanning arbitrary local repository artifacts.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not let cross-desk routing depend on whichever repository document happens to be loaded first. Do not treat aliases, examples, or fixture registrations as canonical identity by default.
