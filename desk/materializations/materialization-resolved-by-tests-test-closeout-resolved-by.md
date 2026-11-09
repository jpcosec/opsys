---
sldb:
  by: agent
  at: '2026-11-09T20:36:57Z'
  authority: generated
  via: create_document
id: materialization-resolved-by-tests-test-closeout-resolved-by
title: resolved-by tests test_closeout_resolved_by
source_atoms:
- atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr
target_kind: test
target_identity: tests/test_closeout_resolved_by.py
validation:
- pytest -q tests/test_closeout_resolved_by.py
tags:
- system:deskops
- topic:closeout
---

# resolved-by tests test_closeout_resolved_by

## Intent

materializa atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr en tests/test_closeout_resolved_by.py
