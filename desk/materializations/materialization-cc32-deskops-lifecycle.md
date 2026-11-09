---
sldb:
  by: agent
  at: '2026-11-09T19:11:58Z'
  authority: generated
  via: create_document
id: materialization-cc32-deskops-lifecycle
title: cc32 deskops lifecycle
source_atoms:
- atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla
target_kind: code
target_identity: deskops/lifecycle.py
validation:
- pytest -q tests/test_activation_rules.py
tags:
- system:deskops
- topic:lifecycle
---

# cc32 deskops lifecycle

## Intent

materializa atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla en deskops/lifecycle.py
