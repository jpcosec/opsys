---
# pill-xxx
id: pill-operational-cli-grammar-follows-spoken-workflow
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:pattern
- topic:cli
- topic:workflow-language
---

# Pattern: operational CLI grammar follows spoken workflow

## What

_Define the context or guardrail this pill carries._

Shape command names, nesting, and help text around the workflow nouns and questions a user naturally asks.

## Why

_Explain why this context matters for safe execution._

A workflow CLI becomes harder to adopt when users must already understand internal implementation structure before they can discover the right command.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task designs command grammar, adds major subcommands, or reorganizes help text around status, doctor, graph, materialization, closeout, or repo context.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `deskops/cli/parser.py`, command help, examples, docs, and any migration from internal terms to user-facing workflow language.

## How

_Describe the correct way to apply this guidance._

Prefer verbs and nouns that match operator intent, keep related actions grouped predictably, and validate the grammar by walking real CLI discovery paths.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not expose internal module boundaries as the primary user grammar. Do not assume a command name is good just because it mirrors implementation structure.
