---
id: materialization-cc36-data-desk-declaration-yaml
title: cc36 data desk_declaration.yaml
source_atoms:
- atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb
target_kind: code
target_identity: deskops/data/desk_declaration.yaml
validation:
- pytest -q tests/test_scaffold_golden.py tests/test_desk_sync.py
tags:
- system:deskops
- topic:scaffold
---

# cc36 data desk_declaration.yaml

## Intent

materializa atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb en deskops/data/desk_declaration.yaml
