---
id: atom-git-ignored-skill-trees-need-tracked-drift-guards
title: Git-ignored skill trees need tracked drift guards
five_wh_one_plus: how
tags: []
---

# Git-ignored skill trees need tracked drift guards

## Answer

Agent-facing skills may live in git-ignored trees such as .pi/, so git history cannot see their drift from the CLI they document. When a skill surface is untracked, the durable drift surface is a tracked guard test that reads the on-disk SKILL.md files and asserts the documented commands match the real CLI; the guard asserts and routes findings, it never rewrites the skills.
