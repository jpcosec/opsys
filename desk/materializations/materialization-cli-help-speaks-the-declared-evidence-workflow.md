---
id: materialization-cli-help-speaks-the-declared-evidence-workflow
title: CLI help speaks the declared-evidence workflow
source_atoms:
- atom-cli-should-match-spoken-workflow-language
- atom-task-lifecycle-is-cli-runnable-end-to-end
target_kind: source_file
target_identity: deskops/cli/registry.py
validation:
- pytest -q tests/test_cli_help_examples.py tests/test_output_goldens.py
tags:
- system:deskops
- topic:cli
- topic:materialization
---

# CLI help speaks the declared-evidence workflow

## Intent

Help texts, epilogs and examples describe the workflow as it runs today: tasks declare closeout evidence at creation, forced advance never closes, and every printed example runs on a fresh desk.
