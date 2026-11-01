# Disposición WS05, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Resultado auditoria/scion.md, solo lectura sin endpoints vivos ni credenciales, WS05 no produce G_SCION (probe es WS44), separación slug/agente/intento/dispatch/mensaje/conversación, depende de WS01: coincide.

**Ambigüedades.**

1. «API pública… documentados o exportados» frente a campos internos (frontera público/interno). Clase: `no es ambigüedad`. el scope define lo público como «endpoints/SDK documentados o exportados; no tablas ni funciones internas»: un símbolo exportado cuenta como público aunque no esté documentado.
2. «puede leer configuración sin secretos» (perímetro y redacción). Clase: `detalle de promoción`. es una facultad, no una obligación, acotada por «Lee código y documentación en deskops y en el repo scion» y «no muestra tokens»; qué archivos de configuración revisar lo fija el TaskDoc.
