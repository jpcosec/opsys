---
id: materialization-skill-drift-guard-tests
title: Skill drift guard tests
source_atoms:
- atom-git-ignored-skill-trees-need-tracked-drift-guards
- atom-tasks-enable-zero-context-subagents
target_kind: test_file
target_identity: tests/test_skill_cli_drift.py
validation:
- python -m pytest tests/test_skill_cli_drift.py -q
tags:
- system:deskops
- topic:materialization
---

# Skill drift guard tests

## Intent

Keep the git-ignored agent skill trees covered by a tracked test that reads the on-disk SKILL.md files and asserts they match the real CLI, so a changed skill surface resolves to durable validation instead of git history.
