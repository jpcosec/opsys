REFORMULACION
WS24 encarga integrar conocimiento y grafo local en el lector de graph_ui: reutilizar el grafo y una vista de documento genérica registrada en shell/registry.js para átomos, protoátomos, crossroads, materializaciones y pills, con clasificación (tipo y tags declarados) y vecindad de hasta 2 hops. Resultado: navegación ida/vuelta por fuentes y backlinks derivados de la API de grafo de sldb; Markdown no modelado visible y navegable con su ruta de origen; sin renderer nuevo obligatorio por clase. Repo dueño: graph_ui. Límites: solo lectura (G_UI_READ per_delta); preservar Code local de a1b2b22; no duplicar el lector WS13; tags solo si el modelo los declara; ViewDoc WS18 opcional tras G_SPEC_VIEW, sin bloquear navegación básica.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería WS13 (lector/explorador y Code local), WS09 (catálogo y estado de clases), WS03/WS11 (API de grafo, payload/semantic_tags y contrato de navegación), auditoria/ui.md y reconciliacion.md (base a1b2b22). Cambiaría en graph_ui: views/workspace/graph/ (proyección de vecindad/backlinks), views/workspace/node/workspace-view.js (panel Context), shell/registry.js (registro de la vista genérica) y tests. Reutilizaría _build_graph_neighborhood, _build_code_projection y WorkspaceView; no tocaría modelos de deskops. Consumiría WS13 y WS09 como prerrequisitos y el recibo G_UI_READ por delta del receptor P01. Si falta catálogo, API o dato de tags/backlinks, se detendría y registraría el hueco con repo dueño, sin inventar clasificación ni sustituto. Validaría en store temporal real/corpus WS40: navegación ida/vuelta, backlinks entrantes, clasificación tipo/tags declarados, vecindad ≤2 hops, Markdown no modelado con ruta de origen y Code preservado; las pruebas fijarían escenarios concretos.

FUTURO
WS09 produce el catálogo de clases y su estado; WS11 fija el contrato de navegación; WS03 aporta el inventario de API de grafo/tags; WS18 y G_SPEC_VIEW deciden la conexión opcional de ViewDoc; el receptor P01 emite el acta G_UI_READ por delta; WS30 valida el uso humano y WS29 consume después; WS06 reconcilia al promover.
