---
sldb:
  by: agent
  at: '2026-11-09T20:36:14Z'
  authority: generated
  via: create_document
id: materialization-cc35b-deskops-doc-access
title: cc35b deskops doc_access
source_atoms:
- atom-deskops-resuelve-documentos-por-los-selectores-de-sldb
target_kind: code
target_identity: deskops/doc_access.py
validation:
- pytest -q tests/test_tracked_selector_resolution.py
tags:
- system:deskops
- topic:selectors
---

# cc35b deskops doc_access

## Intent

materializa atom-deskops-resuelve-documentos-por-los-selectores-de-sldb en deskops/doc_access.py
