## REFORMULACION

**Propósito:** WS27 es un agregado de revisión, no una tarea ejecutable: reúne la integración de diff Git y de evidencia junto a la TaskDoc en el workspace.

**Resultado:** se considera cumplido cuando WS27.1 (diff/historial read-only) y WS27.2 (evidencia declarada/encontrada/verificada) cumplen su aceptación. No produce entregable propio fuera de las salidas de sus hijos.

**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/`; las salidas concretas viven en `frontends/mindmap/views/workspace/diff/` y `.../evidence/` según cada hijo.

**Límites:** alcance agregado limitado a diff y evidencia; no ejecuta cambios ni escribe/revierte; no muestra hallazgos de integridad del store (WS29); no crea modelo de comentarios nuevo. Depende de WS13 y WS12 y de sus hijos. Requiere `G_UI_READ` (evaluación `per_delta`). Promoción no autorizada; requiere preflight y TaskDoc.

## AMBIGUEDADES

Ninguna.

El agregado no obliga al ejecutor a inventar: repo, dependencias, resultado y aceptación comprobable están definidos; la aceptación remite a las aceptaciones de WS27.1/WS27.2, y el gate pendiente es intencional con productor humano designado (P01).

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS27, hijos WS27.1/WS27.2, vecinos WS13/WS12), `task-ws27.md`, `reconciliacion.md`, guía de revisión. Sin herramientas ni ejecución.
- **Cambios previstos:** ninguno en este nodo agregado; no hay mutaciones ni escritura de código. Una promoción futura fijaría archivos/pills/evidencia en el TaskDoc, sin ejecutar aquí.
- **Dependencias:** WS13 (lector con historia/foco), WS12 (contrato de operaciones/escritura), WS27.1 y WS27.2. Transitivas: WS11 y WS02–WS10 según DAG.
- **Validaciones futuras:** aceptación de ambos hijos; recepción `G_UI_READ` por delta con acta del receptor P01 en `graph_ui`; no se exige aceptación conjunta de otros deltas ni de WS29/Changes/Scion.

## FUTURO

- WS13 entrega el lector integrado; WS12 publica el contrato de operaciones y correspondencia de evidencia.
- WS27.1 y WS27.2 producen diff/historial y estados de evidencia respectivamente.
- El receptor P01 en `graph_ui` emite el acta de recepción del delta concreto.
- La promoción decide archivos exactos, escenarios y textos mediante TaskDoc; no corresponde a este revisor.
