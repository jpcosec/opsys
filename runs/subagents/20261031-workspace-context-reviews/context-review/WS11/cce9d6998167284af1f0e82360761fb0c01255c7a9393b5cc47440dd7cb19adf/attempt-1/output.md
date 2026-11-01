REFORMULACION
WS11 es un nodo de planificación de deskops: cerrar el contrato básico de navegación e identidad del workspace documental. Resultado: `contratos/navegacion.md` con identidad/origen de documentos y nodos graph/code, resolución repo/store, foco, enlaces/historia y lectura multidesk read-only; huecos clasificados con productor; y mapa de deltas de graph_ui que requieren recibo G_UI_READ. Repo dueño: deskops. Límites: solo contrato y enlaces; no implementa, no escribe actas interrepo, no afirma recibos y puede cerrar sin acta receptora. Depende de WS09/WS08; G_PRODUCT ya está satisfecho.

AMBIGUEDADES
1. «WS11 cierra con contrato básico revisado»: no dice quién revisa ni qué evidencia acredita «revisado». Obligaría a inventar revisor, registro y criterio de cierre; riesgo de autodeclarar la revisión.
2. «cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño»: define instancia/vínculo, pero no el criterio para separar consulta/API/renderer ni la granularidad del productor cuando el hueco cruza repo/nodo. Obligaría a inventar reglas de clasificación y asignación.

DRY-RUN
WS11 no es agregado; es planificación: su ejecución futura sería documental, sin código. Lecturas: `borradores/user-flows.md` (WS08), `borradores/vistas.md` (WS09), auditorías WS02–04 por dependencia transitiva, `decisiones.md`, brief/alcance y gates. Cambios: crear/actualizar `deskops:desk/drawer/plans/workspace-documental/contratos/navegacion.md` con APIs citadas por path/símbolo/commit, foco/enlaces/historia, aliases/roots multidesk read-only, tabla de huecos y mapa G_UI_READ con IDs/efectos; enlaces externos solo si existen. No escribir en graph_ui/spec2viz/sldb. Gates: consumir G_PRODUCT (satisfied); no consumir G_UI_READ ni G_SPEC_VIEW; G_SPEC_VIEW queda para WS18. Errores: si falta auditoría, API o productor, detener y registrar hueco con dueño; no inventar sustituto. Validación: cada API con evidencia real, sin afirmar recibos, sin bloquear por G_SPEC_VIEW y cierre posible sin acta.

FUTURO
P01/receptor del repo emite actas por delta al preparar cada delta; WS18 obtiene G_SPEC_VIEW; WS12 y WS13.x/WS40/WS41 consumen el contrato; WS16/WS30 validan lectura/edición; la promoción de WS11 exige preflight task-only y archivos/pills/evidencia precisos. Nada de eso autoriza implementación ni recibos por adelantado.
