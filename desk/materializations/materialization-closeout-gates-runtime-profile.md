---
id: materialization-closeout-gates-runtime-profile
title: closeout gates runtime profile
source_atoms:
- atom-review-attestations-state-only-what-was-actually-read
target_kind: code
target_identity: deskops/models/runtime_profile.py
validation:
- pytest -q tests/test_review_command.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates runtime profile

## Intent

RuntimeProfileDoc names the reviewer runtime a review runs on.
