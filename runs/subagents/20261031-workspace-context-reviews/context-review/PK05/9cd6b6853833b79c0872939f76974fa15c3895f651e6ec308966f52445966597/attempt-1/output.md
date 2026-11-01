## REFORMULACION
PK05 es un paquete agregado de planificación, no ejecutable, que fija el resultado sustantivo de **autoría y operación manual**: editar campos con conflicto visible y precondición de escritura, guardar fuente reversible sin commit, alternar fuente/render conservando buffer, capturar intake/drawer/tareas, revisar diff/evidencia y cerrar por handoff verificable. Se apoya en el contrato WS12 y en las salidas de WS19/20/21/45/25/26/27/28/42; WS30 valida UF02–05 con acta humana. `owner_repo: deskops` agrupa; el producto se reparte entre graph_ui y sldb. Límites: no autoriza tareas ni añade aristas, no implementa, no habilita UI sin G_HUMAN_READ, no hace closeout HTTP ni toca Scion.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Ejecución hipotética: inicia WS12, que consume WS11/WS08 e inventarios WS02–04, y entrega contrato de operaciones, whitelist, representación de precondición y efectos. Luego ramifica: WS19 (con WS19.1/19.2) integra edición/conflicto tras WS12 y G_PAYLOAD_PRECONDITION; WS20 produce guardado raw-source y G_SOURCE; WS45 entrega inventario/pruebas y G_PAYLOAD_PRECONDITION; WS21 consume WS19 y, en variante editable, WS20/G_SOURCE; WS25 integra captura; WS22 habilita Board para WS26; WS26 consume WS12/WS22 y G_CLOSEOUT; WS27 consume WS13/WS12; WS42 consume WS19/WS24/WS12; WS28 consume WS27/WS12; WS30 consume salidas de WS17/21/22/23/24/25/26/28/42. Transferencias: contrato WS12 → campos, captura, cierre y conocimiento; gate de payload → WS19/21; raw-source → WS21 editable; tareas → WS26; diff → WS28; todas las salidas → WS30. Validación integrada: pruebas de roundtrip/conflicto/protegidos, guardado sin commit, read-only/handoff con coordinador, distinción evidencia declarada/encontrada/verificada y cierre confirmado por commit/Deskops; WS30 registra UF02–05. Si falta contrato, se detiene y registra hueco con repo dueño.

## FUTURO
Decisiones humanas de aceptación de producto y recepción por delta; WS16 produce G_HUMAN_READ; WS20/WS45 producen G_SOURCE/G_PAYLOAD_PRECONDITION; WS12 publica contrato; WS30 emite acta; WS43 publica entradas reales.
