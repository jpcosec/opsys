## REFORMULACION
Propósito: precisar el catálogo de vistas/renderizaciones del workspace. Resultado: `borradores/vistas.md` con cada fila provista de origen, contrato, renderer, acción/dueño, error y estado, más ficha completa y distinción authored/derivado/preferencia local. Repo dueño: `deskops`. Límites: nodo de planificación; no implementa UI ni ejecuta; ViewDoc se trata como grafo, no como contrato universal de UI; depende de WS07/WS10 y del gate G_PRODUCT.

## AMBIGUEDADES
1. «error = fallo visible esperado para esa fila» (`dag.yaml#node:WS09`): no hay fuente que enumere fallos esperados por fila; WS04 aporta disponibilidad y WS10 etiquetas, no errores. El ejecutor tendría que inventar el fallo esperado de cada fila.
2. «aceptación mediante user-flow» (`vistas.md`, ficha por vista) junto a «completa la ficha por fila» (`dag.yaml#node:WS09`): WS09 no depende de WS08, que refina el guion de user-flows, y `cobertura.md` asigna flujos a nodos, no a filas del catálogo. Se inventaría el vínculo fila→UF o faltaría una dependencia.

## DRY-RUN
Lecturas previstas: `dag.yaml` (WS09 y vecinos), `vistas.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y, cuando existan, `auditoria/ui.md` (WS04) y la salida de WS10. Cambios previstos: solo `desk/drawer/plans/workspace-documental/borradores/vistas.md`. Dependencias: WS07 (G_PRODUCT, P01/P04) y WS10 (definiciones de estado); WS04 llega transitivamente. Validaciones futuras: que cada fila de ambas tablas y la ficha tengan los campos pedidos, estados trazables a WS10/WS04, y que no se atribuya a ViewDoc un contrato universal de UI; preflight de promoción en TaskDoc.

## FUTURO
WS10 entrega las definiciones de disponible/propuesto/bloqueado; WS04, la disponibilidad observada; WS07 registra G_PRODUCT y `source_mode`; el TaskDoc de promoción fija archivos y evidencia; WS11, WS18, WS22 y WS23 consumen el catálogo. La aprobación de Pxx y del gate es decisión humana.
