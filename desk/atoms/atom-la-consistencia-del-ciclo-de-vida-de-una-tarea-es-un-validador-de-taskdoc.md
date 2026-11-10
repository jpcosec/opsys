---
sldb:
  by: agent
  at: '2026-11-10T10:31:27Z'
  authority: generated
  via: create_document
id: atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
title: La consistencia del ciclo de vida de una tarea es un validador de TaskDoc
five_wh_one_plus: what
tags:
- system:deskops
- topic:lifecycle
---

# La consistencia del ciclo de vida de una tarea es un validador de TaskDoc

## Answer

status, current_node, history y task_type de un TaskDoc se validan contra la tabla de RelationDoc del paquete en el modelo, así que sldb los rechaza en toda vía de escritura (fields update, docs update, /save, transacción); advance aplica el estado completo y desk update no escribe tareas inconsistentes (DA6; D2 y D3 revisables).
