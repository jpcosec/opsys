---
sldb:
  by: agent
  at: '2026-11-10T20:13:09Z'
  authority: generated
  via: create_document
id: materialization-materializa-recibos-de-evidencia-cc33a-en-commands-closeout
title: materializa recibos de evidencia CC33a en commands closeout
source_atoms:
- atom-closeout-verify-escribe-recibos-de-evidencia-como-reviewdoc-kind-evidence
target_kind: code
target_identity: deskops/cli/commands/closeout.py
validation:
- pytest -q tests/test_closeout_evidence_receipts.py
tags:
- system:deskops
- topic:closeout
---

# materializa recibos de evidencia CC33a en commands closeout

## Intent

materializa atom-closeout-verify-escribe-recibos-de-evidencia-como-reviewdoc-kind-evidence en deskops/cli/commands/closeout.py
