REFORMULACION
WS13.3 es un delivery de implementación en `graph_ui`: añadir al lector workspace pestañas de documentos y dos documentos en divisiones, con documento activo, foco por documento e historia de navegación. Resultado: abrir, cambiar y cerrar pestañas; abrir dos documentos en divisiones, alternar el activo y volver conservando documento, foco, origen e historia; disposición local de sesión, sin persistencia tras recarga. Límites: reutilizar la base a1b2b22 y las rutas de lectura del contrato WS11; no duplicar workspace ni implementar edición; depende de WS11 y WS13.1; G_UI_READ por delta; promoción no autorizada.

AMBIGUEDADES
1. «Abrir, cambiar y cerrar pestañas» y «Volver sigue el orden inverso de navegación»: no se define qué documento queda activo ni qué pasa con el foco guardado y la historia al cerrar la pestaña activa o una no activa, ni si un documento cerrado sigue siendo alcanzable al volver. El ejecutor tendría que inventar esa transición y su comprobación.

DRY-RUN
Hipotéticamente, el ejecutor leería WS13.3, el contrato WS11, WS13.1, el código actual de `workspace.mjs`/`workspace-view.js`, P07 y la reconciliación WS06. Crearía el módulo de layout bajo `frontends/mindmap/views/workspace/layout/`, integraría estado de pestañas/divisiones, foco por documento e historia, y añadiría tests. Consumiría de WS11 identidad, rutas de lectura y semántica de historia/foco; de WS13.1, foco y lectura por documento. Antes de mutar, exigiría el recibo G_UI_READ del delta. Si falta contrato, ruta o recibo, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría apertura, cambio y cierre de pestañas; dos documentos en divisiones; alternancia del activo; vuelta en orden inverso conservando documento, foco, origen e historia; y ausencia de persistencia tras recarga.

FUTURO
WS11 produce el contrato de navegación, identidad e historia; WS13.1 produce lectura y foco por documento; el receptor P01 emite el acta G_UI_READ por delta; la promoción fija archivos, pruebas y textos; WS13.2 aporta el explorador y C-14/C-28 condicionan la serie si comparten archivos. WS13 cierra cuando cierran sus hijos.
