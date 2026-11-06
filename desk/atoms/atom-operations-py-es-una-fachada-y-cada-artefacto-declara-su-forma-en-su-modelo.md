---
id: atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo
title: operations.py es una fachada y cada artefacto declara su forma en su modelo
five_wh_one_plus: where
tags:
- system:deskops
- topic:architecture
- topic:models
---

# operations.py es una fachada y cada artefacto declara su forma en su modelo

## Answer

En deskops, deskops/operations.py es solo una fachada que delega: no guarda lógica propia. Los helpers privados que piden los servicios viven en deskops/doc_access.py o en el servicio dueño, y ningún servicio construye DeskopsOperations (lo reciben). Lo que antes vivía en los spec YAML duplicados (deskops/spec/artifacts y deskops/spec/fields, SpecRegistry) es un atributo de clase de cada modelo: id_pattern, status_default y tags por artefacto. La normalización del payload de una tarea y la compilación de su spec son una sola función, y task_lifecycle.yaml se carga solo por lifecycle.load_lifecycle_spec. Este paso no cambia el comportamiento: los goldens de ayuda y salida quedan idénticos. Implementado en CC30 (plan deskops-como-config); es la base de CC38 (invariantes de un documento al modelo).
