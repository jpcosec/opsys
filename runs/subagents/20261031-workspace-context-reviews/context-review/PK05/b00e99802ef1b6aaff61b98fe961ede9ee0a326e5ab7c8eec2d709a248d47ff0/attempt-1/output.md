REFORMULACION

PK05 es un agregado no ejecutable de la Entrega M. Propósito: reunir autoría y operación manual segura del workspace documental. Resultado sustantivo: capacidades integradas de edición por campos/fuente con conflicto, precondición, buffer y protegidos; captura/triage; autoría y Board; diff/evidencia; handoff de cierre; operaciones de conocimiento; y acta humana WS30 de UF02–05 y navegación. Repo dueño: deskops; hijos en graph_ui, sldb y deskops. Límites: no ejecuta ni autoriza tareas o aristas, no implementa, no sustituye contratos; gates pendientes; mutaciones UI esperan G_HUMAN_READ, mientras pruebas API aisladas pueden avanzar; guardar no hace commit ni closeout HTTP; con coordinador escritor, lectura/handoff.

AMBIGUEDADES

ninguna

DRY-RUN

Un ejecutor futuro no ejecuta PK05: promueve hijos ready siguiendo las aristas. Primero WS12 produce contrato, whitelist, canales y representación de precondición, consumido por todos. WS45 entrega inventario/pruebas y satisface G_PAYLOAD_PRECONDITION para WS19, WS21 y WS26.1. WS20 entrega API fuente reversible y G_SOURCE para WS21 editable. WS46 habilita captura con origen a WS25.2; WS47 protege contenido no declarado en WS19.1/2 y WS26.1; WS48 aporta admisión común de escritura a las rutas mutables.

Después, WS19.1/2 integran edición/conflicto y relaciones; WS25.1/2, mensaje/ack y captura; WS26.1/2, autoría desde candidato, Board y capa lista; WS27.1/2, diff y evidencia; WS28, verificación/handoff de cierre; WS42, split/merge/tipado y materializaciones. WS19 y WS24 alimentan WS42; WS27 alimenta WS28. Todas las salidas, más WS17, alimentan WS30.

Validación conjunta: pruebas por hijo y gates aplicables; WS30 registra recorrido humano UF02–05 y navegación, comprobando guardado sin commit, conflicto, evidencia declarada/encontrada/verificada y cierre confirmado por commit/Deskops. Si falta contrato, API o permiso, se registra hueco con dueño y la operación queda no disponible; no se inventa sustituto.

FUTURO

WS12 fija el contrato; WS45 y WS20 producen sus gates; WS48 produce la admisión; WS30 y el responsable humano generan el acta y G_HUMAN_READ. La recepción P01 decide por delta.
