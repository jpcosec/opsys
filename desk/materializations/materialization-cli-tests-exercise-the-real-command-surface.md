---
id: materialization-cli-tests-exercise-the-real-command-surface
title: CLI tests exercise the real command surface
source_atoms:
- atom-real-cli-surfaces-prove-workflow-behavior
- atom-cli-should-match-spoken-workflow-language
target_kind: test_file
target_identity: tests/test_cli.py
validation:
- pytest -q tests/test_cli.py
tags:
- system:deskops
- topic:cli
- topic:materialization
---

# CLI tests exercise the real command surface

## Intent

Tests drive deskops through main() and its printed help, including the root page's Typical flow and its pointers to deskops faq and the quickstart.
