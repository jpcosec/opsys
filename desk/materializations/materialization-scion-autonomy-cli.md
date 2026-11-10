---
sldb:
  by: agent
  at: '2026-11-10T17:56:32Z'
  authority: generated
  via: create_document
id: materialization-scion-autonomy-cli
title: Scion autonomy cli
source_atoms:
- atom-scion-coordinator-progresses-authorized-work
target_kind: code
target_identity: deskops/cli/commands/runtime.py
validation:
- pytest tests/test_scion_runtime.py tests/test_command_registry.py
- Inspect runs/subagents/20261110-autonomy-coordinator-contract/live-integration-acceptance.md
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
---

# Scion autonomy cli

## Intent

Pass validated explicit runtime context to the Scion template renderer.
