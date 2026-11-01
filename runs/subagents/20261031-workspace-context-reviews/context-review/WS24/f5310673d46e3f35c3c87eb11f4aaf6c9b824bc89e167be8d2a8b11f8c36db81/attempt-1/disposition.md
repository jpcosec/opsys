# Disposición WS24, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Vista de documento genérica única, backlinks por API de grafo de sldb, clasificación tipo/tags, vecindad ≤2 hops, Code local de a1b2b22 preservado, ViewDoc opcional, repo graph_ui, depende de WS13 y WS09: coincide.

**Ambigüedades.**

1. Markdown no modelado «visible y navegable en la vista de documento genérica» frente a «se hereda del lector WS13.1/explorador WS13.2, no segundo lector». Clase: `detalle de promoción`. el scope dice que WS24 no crea lector; el resultado comprobable (abrir un Markdown sin modelo desde la vista y ver su ruta de origen) no depende de cuál de las dos vistas lo pinta; si el registro necesita un caso sin modelo lo fija el TaskDoc.
2. modelado sin tags declarados. Clase: `no es ambigüedad`. «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» y «no inferir clasificación ficticia»: se muestra el tipo y ningún tag.
