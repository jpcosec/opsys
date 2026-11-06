---
id: materialization-closeout-gates-review-service
title: closeout gates review service
source_atoms:
- atom-review-attestations-state-only-what-was-actually-read
target_kind: code
target_identity: deskops/services/review.py
validation:
- pytest -q tests/test_review_command.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates review service

## Intent

Review service: bundle, attempts, receipts, stale detection and disposition.
