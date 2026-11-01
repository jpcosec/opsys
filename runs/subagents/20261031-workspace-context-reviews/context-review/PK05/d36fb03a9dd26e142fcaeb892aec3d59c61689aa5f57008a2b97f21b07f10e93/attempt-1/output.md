REFORMULACION
PK05 es un paquete de planificación no ejecutable, propiedad de deskops. Su resultado sustantivo es dejar verificable la autoría manual segura, el intake/trabajo y la revisión/cierre por handoff en el workspace documental. Agrupa hijos de graph_ui/sldb/deskops: contrato WS12; campos WS19; fuente WS20/WS21; precondición WS45; captura WS25; tareas WS26; diff/evidencia WS27; cierre WS28; conocimiento WS42; validación humana WS30. Límites: no implementa ni autoriza tareas, no crea UI/API, no toca Scion, no hace commits/closeout HTTP, no añade aristas ni aprueba contratos; su completitud es la de sus hijos e integración.

AMBIGUEDADES
ninguna.

DRY-RUN
Al ser agregado, no se ejecuta: un ejecutor futuro recorrería hijos. WS12 produciría contratos/whitelist/matriz y los entregaría a WS19, WS20, WS45, WS25, WS26, WS27, WS28 y WS42. WS45 consumiría WS12 y entregaría inventario/pruebas/G_PAYLOAD_PRECONDITION a WS19/WS21; WS20 entregaría API/tests raw-source/G_SOURCE a WS21 editable. WS19, con WS12 y G_PAYLOAD_PRECONDITION, entregaría edición de campos/conflicto a WS21 y WS42. WS21 integraría fuente/render y entregaría a WS30. WS25 captura, WS26 tareas, WS27 diff/evidencia, WS28 handoff; WS42 conocimiento. WS30 consumiría WS17/21/22/23/24/25/26/28/42 y validaría UF02–05/navegación. WS20 y WS45 comparten output_scope sldb: no paralelizar sin archivos disjuntos fijados por TaskDoc. Gates: G_HUMAN_READ antes de mutaciones UI; G_SOURCE solo editable; G_PAYLOAD_PRECONDITION; G_WRITE_CONTRACT/G_UI_WRITE por delta. Validación conjunta: corpus WS40, guardar sin commit, conflicto/buffer/protegidos, evidencia declarada/encontrada/verificada, cierre por commit/Deskops. Si falta contrato/dato, detener y registrar hueco; no sustituir.

FUTURO
Quedan a cargo de otros: WS12 fija la representación de la precondición; WS45 produce evidencia; WS20 G_SOURCE; WS19/21/25/26/27/28/42 implementan; WS17 produce entradas; WS40 corpus; WS30 acta humana; P01 receptor acta por delta; G_HUMAN_READ de WS16. No se reabren decisiones P01–P09.
