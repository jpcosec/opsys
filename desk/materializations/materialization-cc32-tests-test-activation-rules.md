---
sldb:
  by: agent
  at: '2026-11-09T19:12:04Z'
  authority: generated
  via: create_document
id: materialization-cc32-tests-test-activation-rules
title: cc32 tests test_activation_rules
source_atoms:
- atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla
target_kind: test
target_identity: tests/test_activation_rules.py
validation:
- pytest -q tests/test_activation_rules.py
tags:
- system:deskops
- topic:lifecycle
---

# cc32 tests test_activation_rules

## Intent

materializa atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla en tests/test_activation_rules.py
