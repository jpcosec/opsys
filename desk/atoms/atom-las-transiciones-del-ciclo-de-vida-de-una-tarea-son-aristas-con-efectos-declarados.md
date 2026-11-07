---
id: atom-las-transiciones-del-ciclo-de-vida-de-una-tarea-son-aristas-con-efectos-declarados
title: Las transiciones del ciclo de vida de una tarea son aristas con efectos declarados
five_wh_one_plus: what
tags:
- system:deskops
- topic:lifecycle
---

# Las transiciones del ciclo de vida de una tarea son aristas con efectos declarados

## Answer

El ciclo de vida de una tarea en deskops ya no está escrito en código ni en task_lifecycle.yaml: cada transición es un RelationDoc semilla, managed, en desk/lifecycle/ (sembrado por el scaffold de CC36), cuyos attributes declaran sus efectos {sets, terminal} (GO09 de sldb) y cuya condition es una regla del lenguaje de sldb. deskops advance pide a sldb edges_holding las aristas que se cumplen desde current_node, elige la que corresponde y aplica sus efectos con apply_effects, que valida contra el modelo de la tarea. Implementado en CC31 (plan deskops-como-config).
