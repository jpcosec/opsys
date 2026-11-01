# Disposición WS12, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Propósito, resultado (whitelist, matriz, mapa de recibos, huecos con dueño, elección razonada de la precondición, comparación de captura directa), repo deskops, depende de WS11/WS08 y G_WRITE_POLICY: coincide. Tres precisiones: (1) la reformulación no recoge que el «receptor P01» solo aplica a graph_ui/sldb/spec2viz y que en deltas de deskops no se crea recepción nueva; (2) no define «falta conducta de workflow»; (3) el dry-run lista «prueba real del canal de captura» como validación futura sin dueño, aunque WS12 no ejecuta mutaciones. No contradice el contrato.

**Ambigüedades.**

1. «Elegir la representación de la precondición es entregable de este contrato» (¿quién decide?). Clase: `no es ambigüedad`. el input lo asigna a WS12 con criterio: «justificado por operaciones y escritores alcanzados y reutilizando lo existente; WS45 la verifica»; sin forzar CAS ni algoritmo.
2. recepción en deltas de deskops. Clase: `no es ambigüedad`. «“Receptor P01” aplica a graph_ui, sldb y spec2viz: en deltas de deskops no se crea recepción nueva y rige la autorización de trabajo local».
3. «Falta conducta de workflow cuando ni la API ni su composición de llamadas pueden, con prueba real…» frente a «no ejecuta mutaciones» (punto más cercano a un hueco real de WS12). Clase: `no es ambigüedad`. WS12 no prueba: cita evidencia existente («comprobado requiere evidencia real citada de API/prueba existente») y el input da los hechos a citar (`create_document` sobrescribe, DrawerService rechaza destino existente, `promote` borra la nota). Si no hay prueba existente, lo no comprobado es hueco con productor Deskops explícito antes de WS25.2; el TaskDoc debe escribir ese valor por defecto (ver promotion-notes.md).
