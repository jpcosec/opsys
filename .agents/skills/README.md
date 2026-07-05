# Repo-local agent skills

This directory is now intentionally narrow.

Repo-local skills should only cover workflow helpers that are specific to this repository and that make sense as on-demand skills.

## Current repo-local skill

- `subagent-execution` — bounded helper for launching one deskops execution lane with run evidence.

## Not skills anymore

The following were previously modeled as repo-local skills, but they are better treated as global guidance or system-prompt concerns:

- `use-deskops` is the comprehensive global deskops surface skill at `.opencode/skills/use-deskops/SKILL.md`
- `use-sldb` is the comprehensive global SLDB surface skill at `.opencode/skills/use-sldb/SKILL.md`
- workflow roles such as supervisor, executor, and tester live under `docs/agent-system-prompts/` as role-prompt references, not auto-discovered skills or project agents

This keeps project skill discovery focused on surfaces and tools instead of role identity.
