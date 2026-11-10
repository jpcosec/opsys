---
sldb:
  by: agent
  at: '2026-11-10T20:13:15Z'
  authority: generated
  via: create_document
id: materialization-materializa-recibos-de-evidencia-cc33a-en-tests-test-closeout-evidence-receipts
title: materializa recibos de evidencia CC33a en tests test_closeout_evidence_receipts
source_atoms:
- atom-closeout-verify-escribe-recibos-de-evidencia-como-reviewdoc-kind-evidence
target_kind: test
target_identity: tests/test_closeout_evidence_receipts.py
validation:
- pytest -q tests/test_closeout_evidence_receipts.py
tags:
- system:deskops
- topic:closeout
---

# materializa recibos de evidencia CC33a en tests test_closeout_evidence_receipts

## Intent

materializa atom-closeout-verify-escribe-recibos-de-evidencia-como-reviewdoc-kind-evidence en tests/test_closeout_evidence_receipts.py
