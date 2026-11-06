---
id: materialization-cc30-cli-model-introspection
title: cc30 cli model_introspection
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: code
target_identity: deskops/cli/model_introspection.py
validation:
- pytest -q tests/test_output_goldens.py tests/test_specs.py
tags:
- system:deskops
- topic:architecture
---

# cc30 cli model_introspection

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en deskops/cli/model_introspection.py
