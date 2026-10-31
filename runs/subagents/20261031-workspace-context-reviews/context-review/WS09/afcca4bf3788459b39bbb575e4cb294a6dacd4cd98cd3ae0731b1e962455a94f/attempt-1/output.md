REFORMULACION
Propósito: precisar el catálogo de renderizaciones del workspace documental, separando fuente, selección, representación, contrato, renderer, acciones/dueño, errores y estado. Resultado: `desk/drawer/plans/workspace-documental/borradores/vistas.md` con las filas de sus tablas y la ficha por fila completadas según la aceptación de WS09. Repo dueño: deskops. Límites: nodo de planificación; no implementa UI ni ejecuta; ViewDoc es grafo, no contrato universal de UI; solo modifica `borradores/vistas.md`; no resuelve Pxx ni toca otros repos; depende de WS07, WS10 y G_PRODUCT.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, `vistas.md`, nodo WS09 y contratos de sus dependencias; en ejecución futura, `auditoria/ui.md` (WS04) y salida de WS10. Cambios previstos: completar tablas y fichas en `vistas.md`; sin código ni otros archivos. Dependencias: G_PRODUCT/WS07; definiciones de estado de WS10; auditoría de disponibilidad WS04, transitiva. Validaciones futuras: cada fila con origen, contrato, renderer, acción/dueño, error y estado; distinguir authored/derivado/preferencia local; estado conforme WS10; disponibilidad conforme auditoría; ficha completa; sin capacidades inventadas. Sin ejecutar.

FUTURO
WS07 y el humano registran P01–P09 y G_PRODUCT. WS10 fija las definiciones de disponible/propuesto/bloqueado. WS04 aporta la disponibilidad actual. WS11 y los nodos de implementación consumen el catálogo; el humano decide P04/source_mode y las autorizaciones de promoción.
