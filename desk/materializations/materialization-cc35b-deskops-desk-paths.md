---
sldb:
  by: agent
  at: '2026-11-09T20:36:12Z'
  authority: generated
  via: create_document
id: materialization-cc35b-deskops-desk-paths
title: cc35b deskops desk_paths
source_atoms:
- atom-deskops-resuelve-documentos-por-los-selectores-de-sldb
target_kind: code
target_identity: deskops/desk_paths.py
validation:
- pytest -q tests/test_tracked_selector_resolution.py
tags:
- system:deskops
- topic:selectors
---

# cc35b deskops desk_paths

## Intent

materializa atom-deskops-resuelve-documentos-por-los-selectores-de-sldb en deskops/desk_paths.py
