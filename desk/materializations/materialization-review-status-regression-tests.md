---
sldb:
  by: agent
  at: '2026-11-10T15:17:32Z'
  authority: generated
  via: create_document
id: materialization-review-status-regression-tests
title: Review status regression tests
source_atoms:
- atom-review-status-preserves-current-dispositions
target_kind: test
target_identity: tests/test_review_command.py
validation:
- pytest tests/test_review_command.py
tags: []
---

# Review status regression tests

## Intent

Prove exact-input receipt classification and existential verdict priority, immutable receipt/input/manifest evidence, and real plain/pinned CLI accepted status followed by stale after a task input change.
