REFORMULACION
WS14 es un encargo de implementación en `graph_ui`: integrar búsqueda navegable en el workspace usando la API real (`sldb find` o su ruta en `sldb serve`, según auditoría WS03 y contrato WS11), sin parser propio. El resultado debe abrir el documento con identidad y ruta de origen, conservar consulta y foco al volver, y distinguir sin resultados, error de backend y búsqueda degradada. Límites: `output_scope` solo `frontends/mindmap/source/`, `views/workspace/` y `tests/`; depende de WS13 y requiere G_UI_READ; promoción no autorizada. No es un agregado.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería el contrato WS11, `auditoria/infraestructura.md`, el estado de WS13 y el código actual de `source/`, `views/workspace/` y pruebas. Cambios previstos: añadir cliente/UI de búsqueda y estados en `views/workspace/`, soporte en `source/` si hace falta, y pruebas en `tests/`; sin parser. Consumiría de WS13 la apertura de documento, identidad, ruta y foco; de WS03 la API real; de WS11 la navegación; y de G_UI_READ solo el recibo per-delta de WS14. Si falta WS11, la ruta/API o el recibo, se detendría y registraría el hueco con repo dueño, sin sustituto. Errores esperados: backend caído, respuesta parcial y ausencia de resultados, cada uno declarado. Validaría con prueba de peticiones que teclear no dispara carga completa del grafo, recorrido de teclado buscar→abrir→volver con consulta/foco, y los tres estados. El mecanismo de debounce/umbral, archivos exactos y textos quedan al TaskDoc.

FUTURO
WS16 hará la validación humana de lectura/búsqueda y medirá tiempos; el receptor P01 emitirá el acta de G_UI_READ por este delta; la promoción fijará TaskDoc, archivos, pruebas y textos. Nada de eso es ambigüedad del encargo.
