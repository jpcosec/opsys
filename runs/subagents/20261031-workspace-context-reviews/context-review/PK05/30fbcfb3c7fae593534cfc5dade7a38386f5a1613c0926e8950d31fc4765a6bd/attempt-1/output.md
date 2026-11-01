## REFORMULACION (propósito, resultado, repo, límites)
PK05 es una agrupación no ejecutable cuyo resultado sustantivo es una rebanada integrada de autoría y operación manual: contrato de escritura y precondición de payload disponibles; edición de campos con conflicto visible; guardado raw-source reversible con campos protegidos; fuente/render con buffer conservado; intake/triage; autoría y Board; diff/evidencia; handoff de cierre; operaciones de conocimiento; todo validado humanamente en UF02–05. Repo dueño: `deskops`; hijos en `graph_ui` y `sldb`. Límites: no ejecuta por sí mismo, no autoriza tareas ni añade aristas, no hace commits ni cierre HTTP, no habilita mutaciones UI antes de `G_HUMAN_READ`, no inventa contratos ausentes y se detiene si falta un productor.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Hipotético, sin ejecutar. Lecturas: contratos y salidas de hijos, corpus/entradas de WS17 y contratos WS11/WS13/WS22/WS24.

Orden: WS12 produce contrato y whitelist; tras WS12 corren WS45 (precondición de payload) y WS20 (raw-source). WS19 espera WS12 y `G_PAYLOAD_PRECONDITION`; WS21 espera WS19 y, en editable, `G_SOURCE`. WS25 tras WS12. WS27 tras WS13+WS12. WS26 tras WS22+WS12. WS42 tras WS19+WS24+WS12. WS28 tras WS27+WS12. WS30 va al final, con salidas de WS17/21/22/23/24/25/26/28/42.

Artefactos entre hijos: WS12 entrega operaciones/efectos; WS45, inventario y pruebas de rechazo/aplicación que producen `G_PAYLOAD_PRECONDITION`; WS20, API y pruebas que producen `G_SOURCE`; WS19, edición de campos; WS21, fuente/render; WS25, captura/triage; WS27, diff/evidencia; WS26, tareas/Board; WS42, operaciones de conocimiento; WS28, diagnóstico y handoff de cierre; WS30, acta humana integrada.

Validación futura: WS30 recorre UF02–05, errores, conflicto en dos ventanas y teclado; comprueba que guardar no hace commit, que otro coordinador implica lectura/handoff, que evidencia declarada/encontrada/verificada es distinta y que el cierre se confirma por commit/Deskops.

## FUTURO
WS30 produce el acta humana; el receptor P01 emite recibos por delta; WS20/WS45 satisfacen sus gates; los TaskDoc de promoción fijan archivos, pruebas y textos; una persona decide la coordinación de escritores. No son ambigüedades de este nodo.
