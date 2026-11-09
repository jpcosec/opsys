---
sldb:
  by: agent
  at: '2026-11-09T18:21:15Z'
  authority: generated
  via: create_document
id: materialization-review-record-commands-review
title: review-record commands review
source_atoms:
- atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo
target_kind: code
target_identity: deskops/cli/commands/review.py
validation:
- pytest -q tests/test_review_record.py
tags:
- system:deskops
- topic:review
---

# review-record commands review

## Intent

materializa atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo en deskops/cli/commands/review.py
