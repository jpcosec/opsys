---
id: materialization-every-command-help-page-states-what-it-does
title: Every command help page states what it does
source_atoms:
- atom-cli-should-match-spoken-workflow-language
target_kind: source_file
target_identity: deskops/cli/parser.py
validation:
- pytest -q tests/test_cli_help_examples.py tests/test_output_goldens.py
tags:
- system:deskops
- topic:cli
- topic:materialization
---

# Every command help page states what it does

## Intent

A command page without its own description reuses its one-line help, deprecated aliases say what replaces them, and argument help wraps while hand-laid examples keep their layout.
