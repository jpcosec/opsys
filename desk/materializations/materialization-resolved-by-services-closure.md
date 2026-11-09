---
sldb:
  by: agent
  at: '2026-11-09T20:36:53Z'
  authority: generated
  via: create_document
id: materialization-resolved-by-services-closure
title: resolved-by services closure
source_atoms:
- atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr
target_kind: code
target_identity: deskops/services/closure.py
validation:
- pytest -q tests/test_closeout_resolved_by.py
tags:
- system:deskops
- topic:closeout
---

# resolved-by services closure

## Intent

materializa atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr en deskops/services/closure.py
