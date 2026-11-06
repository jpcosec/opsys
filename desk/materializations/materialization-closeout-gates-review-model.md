---
id: materialization-closeout-gates-review-model
title: closeout gates review model
source_atoms:
- atom-review-attestations-state-only-what-was-actually-read
target_kind: code
target_identity: deskops/models/review.py
validation:
- pytest -q tests/test_review_doc.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates review model

## Intent

ReviewDoc as the receipt of a review anchored to the task contract by subject.
