**REFORMULACION**
WS25.2 debe implementar en graph_ui (`frontends/mindmap/views/workspace/capture/`, endpoints autorizados y `tests/`) la captura interna a drawer o protoátomo, con destino explícito, origen preservado, sin tarea activa y colisión controlada. Depende de WS12 (contrato), WS46 (capacidad probada de captura con origen por destino) y WS48 (admisión común de escritura). Límites: no crear API/modelo por reflejo, no mutar el desk real ni crear tarea, y probar drawer y protoátomo por separado.

**AMBIGUEDADES**
1. «origen = referencia tipada… representación fijada por el contrato WS12» / contrato 7.2: «propuesta del contrato, sin prueba». Obligaría a inventar el formato exacto, normalización y detección de mensaje si WS46 no lo fija.
2. «endpoints autorizados por el contrato WS12»: el contrato remite a HO-01 y no nombra rutas concretas. Obligaría a inventar nombres, métodos y forma de error del endpoint de captura.
3. «colisión… se controla según el contrato»: el contrato no aprueba una opción completa y WS46 debe probarla. Obligaría a inventar semántica de rechazo, mensaje y derivación de id ante archivo existente.

**DRY-RUN**
Nodo ejecutable, no agregado. Lecturas: contrato WS12 (§3, 4.4, 5.9, 7), pruebas/inventario de WS46 por destino y módulo/pruebas de WS48. Cambios previstos: vista de captura con selector de destino; endpoint que invoca solo el canal público probado por WS46; uso del punto único de admisión WS48 antes de escribir; representación de origen validada; refresco de lectura; tests de persistencia tras recargar, origen ruta/mensaje visible, ausencia en Board y `list tasks`, colisión sin sobrescritura y rechazo/handoff sin admisión. Dependencias: WS46 debe entregar prueba real de origen y colisión para drawer y protoátomo; WS48, la admisión. Errores esperados: falta WS46/WS48 → detener; colisión → error controlado; falta de admisión → lectura/handoff con buffer conservado. Validación futura: tests en store temporal, acta P01 y gates `G_WRITE_CONTRACT`, `G_UI_WRITE`, `G_HUMAN_READ`.

**FUTURO**
WS46 produce la capacidad y pruebas de captura con origen. WS48 produce la admisión de escritura. Root/revisión decide `G_WRITE_CONTRACT`; P01 registra `G_UI_WRITE`; el humano habilita `G_HUMAN_READ`.
