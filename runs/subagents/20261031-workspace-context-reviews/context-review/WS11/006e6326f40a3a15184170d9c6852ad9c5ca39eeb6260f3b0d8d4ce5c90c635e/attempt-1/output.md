## REFORMULACION
Propósito: cerrar un contrato básico de navegación e identidad para el workspace documental, sin implementar. Resultado: `contratos/navegacion.md` con identidad/ruta/modelo opcional de documentos Markdown, origen de nodos graph/code, resolución explícita repo/store, foco, enlaces/historia, lectura multidesk read-only, clasificación de huecos (instancia/vínculo/consulta/API/renderer) con productor dueño y mapa de deltas graph_ui que requieren recibo. Repo dueño: deskops; no escribe en graph_ui ni spec2viz. Límites: solo contrato; no mutaciones, no actas interrepo, no código; G_UI_READ por delta y G_SPEC_VIEW opcional no se dan por recibidos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: brief, alcance, decisiones, dag (WS11, WS08, WS09 y gates), cobertura y guía; auditorías WS02–04 por dependencia transitiva. Cambios previstos: redactar/actualizar `contratos/navegacion.md` y enlazar solo recibos ya registrados; no tocar otros repos. Dependencias: WS09/WS08 y G_PRODUCT satisfecho; G_UI_READ pendiente `per_delta`; G_SPEC_VIEW opcional pendiente. Validaciones futuras: revisión del contrato, cita de path/símbolo/commit de APIs reales, clasificación completa de huecos con productor, mapa de IDs/efectos, ausencia de afirmaciones de recepción y de permiso de escritura; promoción posterior mediante TaskDoc.

## FUTURO
P01/receptor del repo dueño produce las actas G_UI_READ por delta al preparar cada implementación; WS18 prepara y obtiene G_SPEC_VIEW; WS12 y los nodos graph_ui consumen el contrato. Las decisiones humanas ya registradas se reutilizan, no se vuelven a pedir.
