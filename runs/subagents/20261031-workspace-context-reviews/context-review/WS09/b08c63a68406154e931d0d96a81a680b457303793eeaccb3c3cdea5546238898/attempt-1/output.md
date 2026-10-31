## REFORMULACION
- **Propósito:** precisar el catálogo de renderizaciones para que cada fila de `vistas.md` tenga origen, contrato, renderer, acción/dueño, error y estado, distinguiendo authored/derivado/preferencia local.
- **Resultado:** `borradores/vistas.md` actualizado con las filas y fichas completas; ViewDoc se trata como grafo, no como contrato universal de UI.
- **Repo:** `deskops`.
- **Límites:** nodo de planificación; no implementa UI ni ejecuta nada; depende de WS07/WS10/WS08 y de `G_PRODUCT`; no amplía alcance.

## AMBIGUEDADES
1. «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)».  
   Obliga a decidir si «estado» mide madurez de implementación en la UI o publicación/verificación en el manual. WS10 define las etiquetas para el manual y WS04 aporta disponibilidad actual; sin una regla de precedencia, el ejecutor debe inventar la correspondencia entre ambos ejes y podría producir una aceptación no comprobable.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml` (WS09 y aristas WS07/WS08/WS10), `borradores/vistas.md`, `brief.md`, `alcance.md`, `cobertura.md`, `decisiones.md`, `auditoria/ui.md` (WS04, transitiva), `borradores/user-flows.md` (WS08) y `borradores/manual.md` (WS10).
- **Cambios previstos:** solo `borradores/vistas.md`: completar filas de ambas tablas y la ficha por fila.
- **Dependencias:** WS07/WS08/WS10 y `G_PRODUCT`; WS04 llega por dependencia transitiva.
- **Validaciones futuras:** cada fila con los campos exigidos, estado según la regla acordada, distinción authored/derivado/preferencia local y ficha completa; preflight de promoción posterior, no ejecutado aquí.

## FUTURO
WS07 debe registrar `G_PRODUCT`; WS10 aporta definiciones de estado; WS04 aporta disponibilidad actual; WS11/WS18/WS22/WS23 consumen el catálogo. La promoción sigue `not_authorized` y requiere decisión humana y preflight específico.
