## REFORMULACION
PK05 es un **agregado no ejecutable** de “Autoría y operación manual”. Su propósito es planificar un paquete integrado para escribir de forma segura, capturar/intake, operar tareas, revisar evidencia y cerrar mediante handoff verificable. El resultado sustantivo es la integración de las salidas de sus hijos —contrato de operaciones, precondiciones, guardas, captura, autoría, revisión, cierre y conocimiento—, no la ejecución de una tarea única. `owner_repo: deskops`, aunque varios hijos pertenecen a graph_ui y sldb. Límites: no ejecuta, no cierra gates, no autoriza mutaciones ni sustituye las aceptaciones de sus hijos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Hipotéticamente, WS12 produce primero `contratos/operaciones.md`, whitelist, policy y representación de precondición, consumidos por WS45, WS46, WS47, WS48, WS19, WS20, WS25, WS26, WS27, WS28 y WS42.

WS45 entrega inventario y pruebas de precondición y satisface `G_PAYLOAD_PRECONDITION`, consumido por WS19, WS21 y WS26.1. WS46 entrega captura con origen y control de colisiones para WS25.2. WS47 entrega la guarda de contenido no declarado para WS19.1/2, WS21, WS25.1/2, WS26.1/2, WS28 y WS42. WS48 entrega el punto único de admisión de escritura para esos mismos consumidores. WS20 entrega `G_SOURCE`; junto con WS19 habilita WS21 editable.

WS25 integra ack/captura; WS26 autoría y contexto; WS27 diff/evidencia; WS28 handoff/cierre; WS42 operaciones de conocimiento. WS27 alimenta WS28; WS19 y WS24 alimentan WS42; WS25, WS26, WS28 y WS42, con salidas externas WS17/21/22/23/24, alimentan WS30.

La validación conjunta exige pruebas de guardado sin commit, conflicto, buffer, campos protegidos, lectura/handoff con coordinador escritor, evidencia declarada/encontrada/verificada distinta y cierre confirmado por commit/Deskops. WS30 registra el recorrido humano UF02–05 y navegación; las mutaciones UI esperan `G_HUMAN_READ`.

## FUTURO
WS12 publica contrato y huecos; WS45/46/47/48 producen capacidades y gates; los hijos de implementación entregan sus pruebas; WS30 y el responsable humano producen el acta. La aceptación de deltas y permisos Scion quedan fuera de PK05.
