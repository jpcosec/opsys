## REFORMULACION

**Propósito:** definir un nodo de implementación en graph_ui que muestre, junto a la TaskDoc, la evidencia declarada, encontrada y verificada, sin introducir un modelo de comentarios.

**Resultado:** vista de evidencia en `frontends/mindmap/views/workspace/evidence/` con tests, capaz de abrir el soporte Markdown del workspace y, fuera de ese caso, mostrar ruta y "no soportado".

**Repo dueño:** graph_ui. **Dependencias:** WS13 (lector con historia/foco, agregado) y WS12 (contrato de operaciones/escritura). **Gate:** G_UI_READ, pendiente y evaluado por delta; su ausencia de recibo es intencional, no defecto.

**Límites:** solo lectura; sin comentarios nuevos; rutas de lectura según contrato WS11; no promete apertura de artefactos no Markdown (alcance.md).

## AMBIGUEDADES

1. «Declarada = closeout_evidence de la TaskDoc; encontrada = artefactos resolubles en las references/files de la TaskDoc». No se fija cómo emparejar una entrada declarada con un artefacto encontrado (normalización de rutas, identidad, granularidad por ítem o por TaskDoc). El ejecutor tendría que inventar la regla de correspondencia para distinguir «declarada sin artefacto» de «artefacto no declarado».

2. «verificada = resultado de `deskops closeout verify`». No se define qué salida o código de esa orden constituye "verificada", "fallida" o "no ejecutable", ni si su alcance es por artefacto o por TaskDoc. Obligaría a inventar el mapeo entre resultado del comando y estados visibles, y el comportamiento si el comando no está disponible.

## DRY-RUN

- **Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS27.2 y aristas WS12/WS13/WS27/gates (sin revisarlas).
- **Cambios previstos:** crear la vista de evidencia y sus tests en graph_ui, consumiendo rutas de lectura del contrato WS11 y la salida de `deskops closeout verify`.
- **Dependencias:** WS13 completo (WS13.1–13.3), contrato WS12, G_UI_READ con recibo por delta para este nodo.
- **Validaciones futuras:** preflight task-only al promover, pruebas con store temporal o corpus WS40, acta de recepción humana en graph_ui.

## FUTURO

El TaskDoc de promoción fijará archivos exactos, textos de pantalla y escenarios de prueba. El receptor humano emitirá el recibo G_UI_READ por este delta. WS12 publicará el contrato de operaciones y WS11 las rutas de lectura. La conciliación con a1b2b22/f16fcd1/134a665 queda pendiente de aceptación, sin inferir cierre por commit.
