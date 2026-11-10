---
sldb:
  by: agent
  at: '2026-11-10T17:56:34Z'
  authority: generated
  via: create_document
id: materialization-scion-autonomy-supervisor
title: Scion autonomy supervisor
source_atoms:
- atom-scion-coordinator-progresses-authorized-work
target_kind: document
target_identity: desk/roles/deskops-supervisor.md
validation:
- pytest tests/test_scion_runtime.py tests/test_command_registry.py
- Inspect runs/subagents/20261110-autonomy-coordinator-contract/live-integration-acceptance.md
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
---

# Scion autonomy supervisor

## Intent

Authorize routine workflow progress and preserve separate executor/tester/closeout responsibilities.
