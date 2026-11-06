---
id: materialization-cc30-services-atoms
title: cc30 services atoms
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: code
target_identity: deskops/services/atoms.py
validation:
- pytest -q tests/test_output_goldens.py tests/test_specs.py
tags:
- system:deskops
- topic:architecture
---

# cc30 services atoms

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en deskops/services/atoms.py
