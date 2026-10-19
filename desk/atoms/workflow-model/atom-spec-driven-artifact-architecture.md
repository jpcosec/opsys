---
id: atom-spec-driven-artifact-architecture
title: Spec-driven artifact architecture
five_wh_one_plus: what
tags:
- system:deskops
- topic:specs
- topic:artifacts
---

# Spec-driven artifact architecture

## Answer

Deskops artifact YAML specs supply artifact-level config such as id patterns, status defaults, tag defaults, and field lists for structure diagrams. The Pydantic model owns the fields of each artifact, and the task lifecycle is declared in its own workflow spec, `deskops/spec/workflows/task_lifecycle.yaml`, not in artifact specs.
