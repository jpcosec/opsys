---
id: materialization-forced-advance-never-closes
title: Forced advance never closes
source_atoms:
- atom-closing-commits-are-tool-made-and-run-linked
target_kind: source_file
target_identity: deskops/services/tasks.py
validation:
- pytest -q tests/test_inbox_promote_cli_gaps.py
tags:
- system:deskops
- topic:closeout
- topic:materialization
---

# Forced advance never closes

## Intent

A forced advance (--to) skips lifecycle gates but refuses both complete and closed, pointing at deskops closeout commit, so only the tool-made closing commit closes a task.
