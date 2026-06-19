---
id: pill-operational-cli-grammar-follows-spoken-workflow
tags:
- system:deskops
- workspace:desk
- pill-type:pattern
- topic:cli
- topic:workflow-language
---

# Pattern: operational CLI grammar follows spoken workflow

## What

Shape command names, nesting, and help text around the workflow nouns and questions a user naturally asks.

## Why

A workflow CLI becomes harder to adopt when users must already understand internal implementation structure before they can discover the right command.

## When

Apply this pill whenever a task designs command grammar, adds major subcommands, or reorganizes help text around status, doctor, graph, materialization, closeout, or repo context.

## Where

Applies to `deskops/cli/parser.py`, command help, examples, docs, and any migration from internal terms to user-facing workflow language.

## How

Prefer verbs and nouns that match operator intent, keep related actions grouped predictably, and validate the grammar by walking real CLI discovery paths.

## How Not

Do not expose internal module boundaries as the primary user grammar. Do not assume a command name is good just because it mirrors implementation structure.
