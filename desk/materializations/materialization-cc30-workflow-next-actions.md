---
id: materialization-cc30-workflow-next-actions
title: cc30 workflow next_actions
source_atoms:
- atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
target_kind: code
target_identity: deskops/workflow/next_actions.py
validation:
- pytest -q tests/test_output_goldens.py tests/test_specs.py
tags:
- system:deskops
- topic:architecture
---

# cc30 workflow next_actions

## Intent

materializa la fachada de operations.py y la forma de artefacto en el modelo (CC30) en deskops/workflow/next_actions.py
