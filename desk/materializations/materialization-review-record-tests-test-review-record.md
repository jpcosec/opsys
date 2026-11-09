---
sldb:
  by: agent
  at: '2026-11-09T18:21:17Z'
  authority: generated
  via: create_document
id: materialization-review-record-tests-test-review-record
title: review-record tests test_review_record
source_atoms:
- atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo
target_kind: test
target_identity: tests/test_review_record.py
validation:
- pytest -q tests/test_review_record.py
tags:
- system:deskops
- topic:review
---

# review-record tests test_review_record

## Intent

materializa atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo en tests/test_review_record.py
