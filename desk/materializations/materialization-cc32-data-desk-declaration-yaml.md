---
sldb:
  by: agent
  at: '2026-11-09T19:12:02Z'
  authority: generated
  via: create_document
id: materialization-cc32-data-desk-declaration-yaml
title: cc32 data desk_declaration.yaml
source_atoms:
- atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla
target_kind: code
target_identity: deskops/data/desk_declaration.yaml
validation:
- pytest -q tests/test_activation_rules.py
tags:
- system:deskops
- topic:lifecycle
---

# cc32 data desk_declaration.yaml

## Intent

materializa atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla en deskops/data/desk_declaration.yaml
