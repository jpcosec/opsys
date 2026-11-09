---
sldb:
  by: agent
  at: '2026-11-09T20:36:55Z'
  authority: generated
  via: create_document
id: materialization-resolved-by-commands-closeout
title: resolved-by commands closeout
source_atoms:
- atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr
target_kind: code
target_identity: deskops/cli/commands/closeout.py
validation:
- pytest -q tests/test_closeout_resolved_by.py
tags:
- system:deskops
- topic:closeout
---

# resolved-by commands closeout

## Intent

materializa atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr en deskops/cli/commands/closeout.py
