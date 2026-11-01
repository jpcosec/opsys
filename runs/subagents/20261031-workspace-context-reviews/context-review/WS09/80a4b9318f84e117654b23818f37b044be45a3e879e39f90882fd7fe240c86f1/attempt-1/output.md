## REFORMULACION
Propósito: precisar el catálogo de renderizaciones del workspace documental. Resultado: `borradores/vistas.md` con cada fila inventariada y su ficha completa: origen, contrato o «sin contrato», renderer, acción/dueño, error, estado y aceptación, distinguiendo authored/derivado/preferencia local. Repo dueño: `deskops`. Límites: no implementar UI ni APIs, no inventar actores/renderers disponibles, ViewDoc no es contrato universal de UI, promoción no autorizada.

## AMBIGUEDADES
1. Fuente normativa del estado. Cita: «estado desde auditorías WS02–04/decisiones y UFs WS08» y «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)». Obliga a inventar la precedencia entre WS10, las auditorías/decisiones, las UFs de WS08 y WS04. Además, WS10 define estados para capítulos de `borradores/manual.md`, no para filas de render; el ejecutor tendría que decidir si esos criterios se trasladan literalmente o si solo aportan el vocabulario.
2. Cobertura de la ficha sin UF aplicable. Cita: «completa la ficha por fila», donde la ficha incluye «aceptación mediante user-flow», frente a la regla «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación». Si una fila no tiene UF identificable, obliga a inventar una UF, un productor distinto de WS08/WS30 o a forzar un productor que no genera aceptación de user-flow.

## DRY-RUN
Lecturas previstas: `dag.yaml` (WS09 y gates), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vistas.md`, auditorías WS02–04, `borradores/user-flows.md` (WS08) y `borradores/manual.md` (WS10). Cambios previstos: completar filas y fichas de `borradores/vistas.md`; no tocar otros outputs. Dependencias: WS07/WS10/WS08 y, transitivamente, WS02–04; G_PRODUCT satisfecho. Validaciones futuras: revisión de contexto, contraste con WS11/WS12 para huecos y promoción posterior con TaskDoc; nada se ejecuta aquí.

## FUTURO
WS11 y WS12 producirán contrato de navegación y operaciones; WS18 consumirá la selección mínima del catálogo; WS22/23/24 implementarán renderers; WS10 entregará el manual; WS08 mantendrá las UFs. La promoción, archivos exactos y preflight quedan para otro nodo o decisión humana.
