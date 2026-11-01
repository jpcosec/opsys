## REFORMULACION
WS11 es un nodo de planificación del repo `deskops` cuyo propósito es cerrar el contrato básico de navegación e identidad del workspace documental: identidad/ruta/modelo opcional de documentos Markdown, nodos graph/code con origen, resolución repo/store, foco, enlaces/historia y lectura multidesk read-only. El resultado es `contratos/navegacion.md`, con APIs reales citadas desde auditorías WS02–04, clasificación de huecos (instancia/vínculo/consulta/API/renderer) con productor dueño, y mapa de deltas que requieren recepción externa. Límites: no implementa UI, no escribe actas interrepo, no inventa modelos ni APIs, y puede cerrar sin recibos G_UI_READ ni G_SPEC_VIEW; cada delta queda bloqueado hasta su propio recibo.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el nodo WS11, `borradores/vistas.md` de WS09, `borradores/user-flows.md` de WS08, las auditorías WS02–04, `brief.md`, `decisiones.md`, `alcance.md` y los recibos G_UI_READ ya registrados, si existen. Escribiría `contratos/navegacion.md` con: contrato de identidad/origen/foco/enlaces/historia; resolución repo/store y lectura multidesk; tabla de huecos clasificados con productor; y mapa de deltas graph_ui/spec2viz con actor P01, IDs, efectos y enlace solo a actas existentes.

Consumiría G_PRODUCT ya satisfecho; no exigiría G_UI_READ para cerrar el contrato básico y no obtendría G_SPEC_VIEW, que corresponde preparar a WS18. Si falta una salida de WS08/WS09 o una API real, se detendría y registraría el hueco con repo dueño, sin sustituirlo. Si falta un acta, la dejaría como pendiente en el mapa, sin crearla.

Validaría que cada afirmación cite path/símbolo/commit o evidencia existente; que cada hueco tenga clasificación y productor; que el contrato no invente modelos, actores ni permisos; y que el cierre no afirme recepciones inexistentes.

## FUTURO
WS12 consume el contrato para operaciones y escritura. WS13.1–WS13.3, WS17, WS18, WS40 y WS41 lo usan para lectura, índices, proyecciones y multidesk. El receptor P01 produce las actas por delta en el repo dueño; WS18 prepara G_SPEC_VIEW. La implementación queda para nodos posteriores.
