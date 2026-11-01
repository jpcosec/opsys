## REFORMULACION
**Propósito:** cerrar el contrato básico de navegación e identidad del workspace documental. **Resultado:** `contratos/navegacion.md` con identidad/origen, foco, enlaces/historia y lectura multidesk read-only; clasificación de huecos (instancia/vínculo/consulta/API/renderer) con productor dueño; mapa de deltas que requieren recepción G_UI_READ y, opcionalmente, G_SPEC_VIEW. **Repo:** deskops. **Límites:** nodo de planificación; no implementa, no escribe actas interrepo ni afirma recibos; depende de WS08 y WS09; G_PRODUCT ya satisfecho; puede cerrar sin acta receptora.

## AMBIGUEDADES
1. «WS11 cierra con contrato básico revisado»: no se identifica quién revisa ni con qué criterio se declara revisado. Obligaría a inventar un revisor/aceptación o a equipararlo a un gate inexistente.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, la guía, `brief.md`, `alcance.md`, `decisiones.md`, `borradores/user-flows.md` (WS08), `borradores/vistas.md` (WS09), auditorías WS02–04 y `reconciliacion.md`. Crearía `desk/drawer/plans/workspace-documental/contratos/navegacion.md` con: identidad/ruta/modelo opcional y origen; foco por documento; enlaces/historia; resolución repo/store y multidesk read-only; tabla de huecos clasificados con productor; mapa de deltas G_UI_READ por delta con actor P01, IDs y efectos, y G_SPEC_VIEW opcional. Consumiría WS08/WS09 como fuentes; G_PRODUCT está satisfecho. Validaría que cada afirmación cite path/símbolo/commit de auditoría, que ningún hueco quede sin categoría ni dueño, que no se inventen APIs/modelos y que no se declare recibo alguno. Si faltan WS08/WS09 o evidencia de auditoría, se detendría y registraría el hueco según reglas comunes. No escribiría en graph_ui, sldb ni spec2viz. El cierre esperado es contrato básico revisado, clasificación de huecos y mapa de deltas.

## FUTURO
WS12 consume el contrato; WS13.x, WS17, WS18, WS40 y WS41 lo usan. El solicitante P01/receptor emite actas por delta en su repo; WS18 prepara G_SPEC_VIEW. La revisión del cierre y cualquier recepción quedan fuera de este nodo.
