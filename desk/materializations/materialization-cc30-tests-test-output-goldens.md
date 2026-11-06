---
id: materialization-cc30-tests-test-output-goldens
title: cc30 tests test_output_goldens
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: test
target_identity: tests/test_output_goldens.py
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:architecture
---

# cc30 tests test_output_goldens

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en tests/test_output_goldens.py
