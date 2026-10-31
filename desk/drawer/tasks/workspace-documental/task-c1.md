---
id: C1
status: deferred
depends_on: [B2]
owner: repos dueños
---

# Resolver contrato y clasificación de huecos documentales

## Entregable

matriz resuelta: instancia, vínculo, consulta, contrato o renderer

## Alcance y aceptación

Decidir por caso si bastan Markdown, referencias, consultas y modelos existentes. Puede cerrar sin modelos nuevos. Si se demuestra un hueco de infraestructura, registrarlo en el repo dueño y crear dependencias solo para los nodos afectados; no bloquear entradas Markdown por una migración hipotética. Antes de promover, descomponer cualquier implementación de modelo en tareas atómicas propias con roundtrip y resolución verificables.

## Dependencias y promoción

Depende de B2. Ver [DAG](../../plans/workspace-documental/README.md). No es tarea activa. Si hay código, precisa primero archivos, pills, átomos, validación y contexto fresco; no ejecutar como paquete amplio.
