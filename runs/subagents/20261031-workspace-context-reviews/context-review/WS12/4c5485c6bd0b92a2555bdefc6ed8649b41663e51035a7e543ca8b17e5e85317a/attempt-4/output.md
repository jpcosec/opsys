## REFORMULACION
Propósito: cerrar el contrato de operaciones y escritura del workspace documental. Resultado: `contratos/operaciones.md` con whitelist por campo/modelo, capability exacta (operación, canal, efectos), política de coordinador/Git/campos protegidos/CAS/fallos/permisos/closeout. Repo dueño: deskops. Límites: nodo de planificación; no implementa adapters ni UI, no ejecuta; registra huecos con dueño; no asume lock UI; no diseña canales inexistentes.

## AMBIGUEDADES
1. «si no existe, se registra hueco y dueño, no se diseña uno aquí» frente a «la capacidad raw-source faltante se diseña y queda gated por G_SOURCE». Obliga a inventar si WS12 debe producir un diseño de la capacidad faltante o solo el registro de hueco/dueño, y si G_SOURCE corresponde únicamente a WS20.
2. La aceptación enumera «WS19, WS20, WS25, WS26, WS27, WS28, WS32, WS34, WS36, WS39 y WS42», pero G_UI_WRITE incluye WS21 en `scope_nodes`. Obliga a decidir si WS21 (edición fuente desde UI) debe tener capability en este contrato o queda fuera de la whitelist.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, parameters y nodo WS12; aristas vecinas solo como contratos. Cambios previstos: redactar `contratos/operaciones.md`, tabla de capabilities, políticas y huecos; sin código. Dependencias: WS11 (navegación), WS08 (user-flows), WS07 (G_WRITE_POLICY, P01–P06, source_mode), G_CLOSEOUT externo, G_SOURCE de WS20 y aceptaciones G_UI_WRITE/G_SLDB_WRITE. Validaciones futuras: G_WRITE_CONTRACT, revisión por responsables designados, clasificación existente/faltante; no ejecutar.

## FUTURO
WS07/humano resuelve P01–P09 y source_mode; WS11/WS08 producen sus contratos; WS20 produce G_SOURCE; responsables de graph_ui/sldb aceptan deltas; la promoción sigue no autorizada y requiere preflight.
