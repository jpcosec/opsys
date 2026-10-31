## REFORMULACION
WS11 es un nodo de planificación en `deskops` que debe cerrar `contratos/navegacion.md`: identidad/ruta/modelo opcional, origen, foco, enlaces/historia, lectura multidesk read-only y clasificación de huecos (instancia/vínculo/consulta/API/renderer) con productor dueño antes de code. Depende de WS09 y WS08; G_PRODUCT ya está satisfecho. No implementa ni escribe actas interrepo: solo enlaza recibos externos por delta. Límites: el contrato básico puede cerrar sin recepción de Changes, Scion ni ViewDoc opcional.

## AMBIGUEDADES
1. «Registrar recepción lector por delta en graph_ui (actor P01, IDs, efecto y evidencia)» frente a «puede cerrar sin acta receptora» y «Recibos son producidos por solicitante P01/repo receptor..., no por Executor de WS11». Obliga a inventar si el Executor debe obtener/registrar un recibo, o solo enlazar uno existente; sin esa decisión la aceptación no es comprobable.
2. «Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales» no nombra inventario ni prueba que acredite «real»; las auditorías WS02–04 son dependencias transitivas, no citadas. Obliga a elegir qué fuente y qué evidencia cuentan como API real, y podría hacer que el criterio varíe entre repos.

## DRY-RUN
- Lecturas previstas: este input, `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, bloque WS11 y gates G_UI_READ/G_SPEC_VIEW.
- Cambios previstos: redactar `contratos/navegacion.md` y añadir enlaces a recibos externos por delta; ningún cambio de código ni acta.
- Dependencias: salidas de WS09/WS08; G_PRODUCT satisfecho; WS02–WS10 transitivas.
- Validaciones futuras: contrato revisado, cada hueco con clase y dueño, mapa de deltas, enlaces de recibo; no se exige acta propia.

## FUTURO
WS12 consume el contrato de navegación; WS13/WS40/WS41 usan rutas y aliases; el solicitante P01 o el repo receptor producen los recibos G_UI_READ/G_SPEC_VIEW por delta; WS18 obtiene G_SPEC_VIEW al prepararse. La revisión humana decide el cierre del nodo.
