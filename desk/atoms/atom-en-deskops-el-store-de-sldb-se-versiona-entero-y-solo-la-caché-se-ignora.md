---
id: atom-en-deskops-el-store-de-sldb-se-versiona-entero-y-solo-la-caché-se-ignora
title: En deskops el store de sldb se versiona entero y solo la caché se ignora
five_wh_one_plus: what
tags:
- system:deskops
- topic:store-layout
---

# En deskops el store de sldb se versiona entero y solo la caché se ignora

## Answer

La regla del dueño vigente para el layout de sldb en deskops: .sldb/store.yaml y todo .sldb/core/ se versionan en git (el pasado del store se lee del historial), .sldb_cache/ es regenerable y se ignora, y nada de .sldb/runtime/ se trackea. tests/test_gitignore_policy.py hace cumplir esa política leyendo .gitignore y el índice de git. Un test que espere .sldb/core ignorado quedó viejo frente a la migración de layout y se ajusta el test, no la política.
