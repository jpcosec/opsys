---
sldb:
  by: agent
  at: '2026-11-09T20:36:51Z'
  authority: generated
  via: create_document
id: atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr
title: closeout resolved-by cierra una tarea cuyo trabajo ya entró por PR
five_wh_one_plus: what
tags:
- system:deskops
- topic:closeout
---

# closeout resolved-by cierra una tarea cuyo trabajo ya entró por PR

## Answer

deskops closeout resolved-by --task <id> --ref <commit> [--ref <URL de PR>] --test <ref> --reason <texto> cierra una tarea cuyo trabajo ya está en la historia: exige un commit ancestro de HEAD y que cada --test pase el gate de tests, no exige átomo por archivo, deja status resolved y el commit de cierre con Closeout-Mode: resolved-by (r1-r6, revisables).
