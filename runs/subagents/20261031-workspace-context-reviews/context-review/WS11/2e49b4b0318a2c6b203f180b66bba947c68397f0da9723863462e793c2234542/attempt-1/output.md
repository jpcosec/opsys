**REFORMULACION**
- **Propósito:** cerrar el contrato de navegación e identidad para documentos Markdown y otros nodos con origen, incluyendo resolución repo/store, foco, enlaces/historia y lectura multidesk.
- **Resultado:** `contratos/navegacion.md` y actas de aceptación de `G_UI_READ` y `G_SPEC_VIEW`.
- **Repo:** `owner_repo: deskops`; las actas se ubican “en el repo receptor”.
- **Límites:** no implementa UI ni código; no asume migración Kimun; no publica el contrato como cerrado sin recepción de graph_ui/spec2viz; si falta API, debe abrir una dependencia acotada del repo dueño.

**AMBIGUEDADES**
1. “Resolver cada hueco como instancia/vínculo/consulta/API/renderer” y “Clasificar huecos sin modelos hipotéticos”: el input no enumera los huecos ni indica explícitamente qué artefacto de WS09/WS08 los aporta. Obligaría a inventar el inventario de huecos o a asumir una fuente no fijada.
2. “actas de aceptación de G_UI_READ y G_SPEC_VIEW en el repo receptor” frente a “owner_repo: deskops”: no queda claro si WS11 redacta/registra las actas en graph_ui/spec2viz, solo obtiene la aceptación, o las guarda en deskops. Obligaría a inventar autoría y ubicación del artefacto.
3. “graph/code admiten otros nodos con origen”: no se precisa el alcance de esa admisión para Code, mientras alcance.md limita “Code local a 1–2 hops”. Obligaría a decidir si Code navega nodos no documento o solo el ámbito local.

**DRY-RUN**
- **Lecturas:** guía, brief, alcance, decisiones, cobertura y nodo WS11; sin ejecutar.
- **Cambios previstos:** redactar `contratos/navegacion.md`; registrar evidencia/actas de gates; si aparece API faltante, proponer dependencia acotada; no tocar UI.
- **Dependencias:** WS09 y WS08; designación de responsables vía WS07; `G_PRODUCT` pendiente es intencional. WS11 produce `G_UI_READ` y `G_SPEC_VIEW`.
- **Validaciones futuras:** comprobar clasificación de cada hueco; obtener aceptación de graph_ui/spec2viz; verificar que las actas enumeran sus `scope_nodes`; mantener pendiente si no hay recepción.

**FUTURO**
WS07 designa responsables y registra `G_PRODUCT`; WS09/WS08 producen catálogo y flujos; los responsables de graph_ui/spec2viz aceptan o rechazan las actas. Esas decisiones y entregas ajenas no son ambigüedad de WS11.
