---
id: materialization-forced-advance-never-closes-regressions
title: Forced advance never closes regressions
source_atoms:
- atom-closing-commits-are-tool-made-and-run-linked
target_kind: test_file
target_identity: tests/test_inbox_promote_cli_gaps.py
validation:
- pytest -q tests/test_inbox_promote_cli_gaps.py
tags:
- system:deskops
- topic:closeout
- topic:materialization
---

# Forced advance never closes regressions

## Intent

Regression tests that a forced advance to complete or closed is refused and leaves the task untouched.
