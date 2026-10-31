# Executor comparison — WS27.2

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION

**Propósito:** definir un nodo de implementación en graph_ui que muestre, junto a la TaskDoc, la evidencia declarada, encontrada y verificada, sin introducir un modelo de comentarios.

**Resultado:** vista de evidencia en `frontends/mindmap/views/workspace/evidence/` con tests, capaz de abrir el soporte Markdown del workspace y, fuera de ese caso, mostrar ruta y "no soportado".

**Repo dueño:** graph_ui. **Dependencias:** WS13 (lector con historia/foco, agregado) y WS12 (contrato de operaciones/escritura). **Gate:** G_UI_READ, pendiente y evaluado por delta; su ausencia de recibo es intencional, no defecto.

**Límites:** solo lectura; sin comentarios nuevos; rutas de lectura según contrato WS11; no promete apertura de artefactos no Markdown (alcance.md).

##

## Comparación con intención / hallazgos

1/2 correspondencia por tipo evidencia y reporte público closeout verify se fija en WS12; no inferir por renderer ni afirmar que un gate ejecuta pruebas. Sin reporte/fallo = no verificable/error, no aprobado.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
