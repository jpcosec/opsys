## REFORMULACION
**Propósito:** integrar conocimiento y grafo local en el lector workspace, reutilizando el grafo existente y una vista de documento genérica.
**Resultado:** navegación ida/vuelta por fuentes y backlinks; Markdown no modelado visible y navegable con su ruta de origen; clasificación por tipo/tags; vecindad de hasta 2 hops; sin renderer nuevo obligatorio por clase.
**Repo:** `graph_ui`; salidas en `frontends/mindmap/views/workspace/graph/`, `node/workspace-view.js` (panel Context), `shell/registry.js` y `tests/`.
**Límites:** solo lectura bajo `G_UI_READ`; no crear segundo lector para Markdown no modelado; preservar Code local; ViewDoc WS18 solo tras `G_SPEC_VIEW`; promoción no autorizada; no duplicar implementación ni inferir cierre por commit.

## AMBIGUEDADES
ninguna

## DRY-RUN
Un ejecutor futuro leería el lector/explorador de WS13, el catálogo de WS09 y el contrato WS11 (transitivo), además de la API de grafo de sldb según la auditoría. Consumiría `G_UI_READ` únicamente con el acta per-delta de este nodo.

Cambiaría la vista de grafo bajo `views/workspace/graph/`, el panel Context de `workspace-view.js`, el registro de vista genérica en `shell/registry.js` y pruebas en `tests/`. Concretamente: renderizar relaciones entrantes/salientes hasta 2 hops; mapear átomos, protoátomos, crossroads, materializaciones y pills a la vista genérica; incorporar Markdown no modelado heredado de WS13 con su ruta; mostrar tipo y tags leídos del payload; conservar la proyección Code y su comportamiento.

Errores previstos: falta de contrato/inventario, API de grafo no disponible o 503, nodo no modelado ausente del explorador, modelo/tags desconocidos y referencia rota. Ante un hueco de dependencia: detenerse y registrar repo dueño, sin sustituto.

Validación esperada: con store temporal real o corpus WS40, abrir fuente, seguir backlink y volver; ver un Markdown no modelado con ruta de origen; comprobar tipo/tags sin clasificación ficticia; confirmar vecindad ≤2 hops y ausencia de regresión en Code. Después, acta humana per-delta de `G_UI_READ`.

## FUTURO
WS13 entrega lector/explorador; WS09, el catálogo de renderizaciones; WS11, el contrato de navegación. WS18/ViewDoc queda opcional tras `G_SPEC_VIEW`. La persona P01 decide la aceptación per-delta de `G_UI_READ`. WS40 aporta el corpus de prueba y WS30 valida UF03 posteriormente.
