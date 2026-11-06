---
id: materialization-cc30-tests-test-extension-points
title: cc30 tests test_extension_points
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: test
target_identity: tests/test_extension_points.py
validation:
- pytest -q tests/test_extension_points.py
tags:
- system:deskops
- topic:architecture
---

# cc30 tests test_extension_points

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en tests/test_extension_points.py
