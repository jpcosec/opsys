---
id: materialization-help-examples-run-as-printed
title: Help examples run as printed
source_atoms:
- atom-real-cli-surfaces-prove-workflow-behavior
- atom-task-lifecycle-is-cli-runnable-end-to-end
target_kind: test_file
target_identity: tests/test_cli_help_examples.py
validation:
- pytest -q tests/test_cli_help_examples.py
tags:
- system:deskops
- topic:cli
- topic:materialization
---

# Help examples run as printed

## Intent

Runs the Typical flow and the add examples printed by --help in a temporary git-backed desk, so help cannot drift from the CLI.
