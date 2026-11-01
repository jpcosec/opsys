## REFORMULACION
WS11 es un nodo de planificación en `deskops` cuyo propósito es cerrar el contrato básico de navegación e identidad documental. El resultado es `contratos/navegacion.md`, con identidad/origen, resolución repo/store, foco, enlaces/historia y lectura multidesk read-only, más la clasificación de huecos y el mapa de deltas que requerirán recepción externa. Depende de WS09 y WS08 (con WS02–04 detrás) y de G_PRODUCT, ya satisfecho. Límites: no implementa UI, no escribe actas interrepo, no afirma recibos G_UI_READ/G_SPEC_VIEW, no crea modelos hipotéticos y puede cerrar sin acta receptora.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, las auditorías WS02–04, `borradores/vistas.md` (WS09) y `borradores/user-flows.md` (WS08). Crearía o modificaría `desk/drawer/plans/workspace-documental/contratos/navegacion.md`, definiendo: identidad/ruta/modelo opcional; origen para graph/code; resolución explícita repo/store; foco por documento; enlaces e historia; aliases/roots multidesk read-only; tabla de huecos clasificados instancia/vínculo/consulta/API/renderer con productor; y mapa de deltas graph_ui/spec2viz con actor P01, IDs y efectos.

Consumiría G_PRODUCT como evidencia registrada y las salidas de WS09/WS08. Si falta el catálogo, la matriz UF o una API auditada, registraría el hueco con repo dueño conforme a “Reglas comunes de ejecución”, sin inventar sustituto. Errores esperados: ausencia de evidencia API → hueco API; selección no fijada por WS09 → detener esa parte del contrato; delta sin efecto identificable → marcarlo no definido con productor. Validación: cada ítem de aceptación cubierto; APIs citadas con path/símbolo/commit; ningún recibo declarado; G_SPEC_VIEW tratado como opcional y separado de WS18. Resultado esperado: contrato básico revisable y cerrable sin acta receptora.

## FUTURO
El solicitante P01 o el repo receptor produce cada acta G_UI_READ/G_SPEC_VIEW al preparar el delta concreto. WS12, WS13, WS17, WS40, WS41 y WS33 consumen el contrato; WS18 obtiene G_SPEC_VIEW por separado. Un humano decide la promoción y recepción de deltas.
