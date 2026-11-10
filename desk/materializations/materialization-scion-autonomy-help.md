---
sldb:
  by: agent
  at: '2026-11-10T18:01:33Z'
  authority: generated
  via: save_document_payload
id: materialization-scion-autonomy-help
title: Scion autonomy help
source_atoms:
- atom-scion-coordinator-progresses-authorized-work
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_runtime_template.txt
validation:
- pytest tests/test_scion_runtime.py tests/test_command_registry.py
- Inspect runs/subagents/20261110-autonomy-coordinator-contract/live-integration-acceptance.md
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
---

# Scion autonomy help

## Intent

Record public CLI help including tester mode and explicit context-file input.
