---
sldb:
  by: agent
  at: '2026-11-10T17:56:36Z'
  authority: generated
  via: create_document
id: materialization-scion-autonomy-tests
title: Scion autonomy tests
source_atoms:
- atom-scion-coordinator-progresses-authorized-work
target_kind: test
target_identity: tests/test_scion_runtime.py
validation:
- pytest tests/test_scion_runtime.py tests/test_command_registry.py
- Inspect runs/subagents/20261110-autonomy-coordinator-contract/live-integration-acceptance.md
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
---

# Scion autonomy tests

## Intent

Verify deterministic child identities, native label limits and explicit context/template contracts.
