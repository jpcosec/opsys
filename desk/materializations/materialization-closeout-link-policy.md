---
sldb:
  by: agent
  at: '2026-10-21T06:39:50Z'
  authority: generated
  via: create_document
id: materialization-closeout-link-policy
title: Closeout link policy
source_atoms:
- atom-closeout-verify-requires-tests-links-and-commit
target_kind: source_file
target_identity: deskops/operations.py
validation:
- pytest -q tests/test_closeout_atomless.py tests/test_closeout.py tests/test_closeout_skill_links.py
tags:
- system:deskops
- topic:closeout
- topic:materialization
---

# Closeout link policy

## Intent

Implement closeout knowledge-link coverage only when local atom documents exist, preserving test, ancestor commit, path and generated-source gates.
