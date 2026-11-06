---
id: materialization-cc30-tests-test-packaging
title: cc30 tests test_packaging
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: test
target_identity: tests/test_packaging.py
validation:
- pytest -q tests/test_packaging.py
tags:
- system:deskops
- topic:architecture
---

# cc30 tests test_packaging

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en tests/test_packaging.py
