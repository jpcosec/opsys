---
id: atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb
title: La estructura inicial de un desk se declara en el paquete de deskops y la aplica
  sldb
five_wh_one_plus: what
tags:
- system:deskops
- topic:scaffold
---

# La estructura inicial de un desk se declara en el paquete de deskops y la aplica sldb

## Answer

La estructura de un desk nuevo (carpetas, archivos semilla y plantillas) ya no se crea a mano en el código de deskops: se declara en el paquete, en deskops/data/templates/ y desk_declaration.yaml (folders, seeds e include {model, glob}), y la aplica sldb.api.scaffold_store (GD26) con declaration= y template_root. seed_desk reemplaza a scaffold_desk. Los include glob cubren las semillas trackeadas, así que el store.yaml del desk no cambia por sembrar. Un golden del scaffold (tests/test_scaffold_golden.py) fija la salida. Implementado en CC36 (plan deskops-como-config).
