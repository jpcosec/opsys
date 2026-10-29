---
sldb:
  by: agent
  at: '2026-10-21T06:39:51Z'
  authority: generated
  via: create_document
id: materialization-closeout-atomless-regressions
title: Closeout atomless regressions
source_atoms:
- atom-closeout-verify-requires-tests-links-and-commit
target_kind: test_file
target_identity: tests/test_closeout_atomless.py
validation:
- pytest -q tests/test_closeout_atomless.py tests/test_closeout.py tests/test_closeout_skill_links.py
tags:
- system:deskops
- topic:closeout
- topic:materialization
---

# Closeout atomless regressions

## Intent

Prove atomless closeout behavior with real Git repositories and CLI calls, including strict nested-atom coverage and mandatory evidence/provenance checks.
