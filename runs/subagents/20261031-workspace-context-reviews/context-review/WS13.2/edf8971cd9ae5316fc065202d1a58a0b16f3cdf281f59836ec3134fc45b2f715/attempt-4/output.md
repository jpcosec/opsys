## REFORMULACION

- **Propósito**: implementar en `graph_ui` un explorador que reúna documentos modelados del store y Markdown no modelado del desk, permitiendo abrirlos sin conocer su ID ni introducir índices nuevos.
- **Resultado**: explorador en `frontends/mindmap/views/workspace/explorer/` y `tests/`, alimentado por la API del store y el sistema de archivos del desk según el contrato WS11.
- **Repo dueño**: `graph_ui`. Depende de WS11 (contrato de navegación/identidad) y WS13.1 (lector); requiere `G_UI_READ`, pendiente y producido por WS11. Es entrega, no agregado; integración como delta o ticket existente, sin duplicar workspace.
- **Límites**: lectura; no crear workspace independiente ni índices nuevos; no mutar el store; promoción no autorizada. Aceptación: abrir un documento modelado y uno no modelado sin ID ni índices nuevos, y ver aparecer en el explorador un documento añadido al store temporal sin cambiar código.

## AMBIGUEDADES

ninguna.

## DRY-RUN

- **Lecturas**: nodo WS13.2, guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y bloques vecinos del DAG. Sin herramientas.
- **Cambios previstos**: componente de explorador y pruebas en `graph_ui`; consumo del contrato WS11 y de rutas del store/filesystem; sin edición ni mutación.
- **Dependencias**: contrato WS11, lector WS13.1, gate `G_UI_READ`; corpus WS40 cuando exista; regla de contrato ausente en `alcance.md`.
- **Validaciones futuras**: prueba con store temporal y alta de documento sin cambio de código; apertura de documento modelado/no modelado sin ID; ausencia de índices nuevos; acta de aceptación del gate. No ejecutado.

## FUTURO

WS11 produce el contrato de navegación/identidad y el acta de `G_UI_READ`; WS07 designa al responsable de `graph_ui`; WS13.1 entrega el lector; WS40 aporta corpus; WS13 cierra cuando cumplen sus hijos. La promoción y el TaskDoc fijarán archivos, pills y escenarios de prueba; la autorización y validación humana quedan fuera de este nodo.
