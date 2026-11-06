---
id: materialization-cc30-deskops-doc-access
title: cc30 deskops doc_access
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: code
target_identity: deskops/doc_access.py
validation:
- pytest -q tests/test_output_goldens.py tests/test_specs.py
tags:
- system:deskops
- topic:architecture
---

# cc30 deskops doc_access

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en deskops/doc_access.py
