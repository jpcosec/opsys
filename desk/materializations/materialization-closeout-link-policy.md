---
id: materialization-closeout-link-policy
title: Closeout link policy
source_atoms:
- atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
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
