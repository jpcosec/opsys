---
id: atom-un-pass-focal-no-prueba-el-resto-del-artefacto
title: Un PASS focal no prueba el resto del artefacto
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:workflow
provenance: runs/subagents/20261101-ws11-correccion/review-source.md
---

# Un PASS focal no prueba el resto del artefacto

## Answer

Un Tester focal o por muestra solo prueba lo que abrió, sobre los bytes que leyó. No se declara probado el resto del artefacto, y la cobertura se informa por bytes. En WS09 y WS11 un PASS por muestra dejó pasar negaciones falsas que una lectura completa encontró.
