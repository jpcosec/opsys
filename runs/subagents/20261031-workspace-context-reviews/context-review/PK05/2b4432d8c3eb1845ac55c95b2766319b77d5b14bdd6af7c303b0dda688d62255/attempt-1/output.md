REFORMULACION
Propósito: agrupar la Entrega M de autoría y operación manual segura, ordenando contrato de escritura, edición de campos, guardado fuente, precondición de payload, captura/triage, tareas, evidencia, cierre por handoff, operaciones de conocimiento y validación humana. Resultado: flujo manual verificable captura→autoría→edición→revisión→cierre, con conflicto/buffer/protegidos probados, guardar sin commit, read-only/handoff si hay otro coordinador, evidencia diferenciada y cierre confirmado por commit/Deskops; acta WS30 cubre UF02–05 y navegación necesaria. Repo: `owner_repo: deskops` (paquete de plan); hijos implementan en graph_ui/sldb y WS30 registra acta en graph_ui. Límites: agrupación sin ejecución; no autoriza tareas ni añade aristas; no commit/close HTTP; mutaciones UI tras G_HUMAN_READ; no sustituir contratos/API/datos faltantes.

AMBIGUEDADES
ninguna.

DRY-RUN
1) WS12 (externo) entrega `contratos/operaciones.md`: whitelist, precondición, policy y huecos.
2) En sldb, WS45 y WS20 tras WS12; no en paralelo si comparten `src/sldb/api/documents/` y `tests/`. WS45 inventaría/prueba precondición y produce G_PAYLOAD_PRECONDITION; WS20 verifica/completa raw-source y produce G_SOURCE.
3) WS19 tras WS12+G_PAYLOAD_PRECONDITION; WS19.1/2 entregan edición de campos/conflicto. Desarrollo API aislado avanza; uso UI espera G_HUMAN_READ.
4) WS21 editable tras WS19+G_SOURCE+G_PAYLOAD_PRECONDITION: fuente/render, buffer y composición al documento dueño.
5) WS25 tras WS12; WS25.1/2 entregan mensaje/ack y captura drawer/proto.
6) WS26 tras WS22 (externo)+WS12; WS26.1→WS26.2 autoría/Board; G_CLOSEOUT para promoción.
7) WS27 tras WS13 (externo)+WS12; WS27.1 diff y WS27.2 evidencia.
8) WS42 tras WS19+WS24 (externo)+WS12: split/merge/proto typing y materializaciones; capability faltante se declara no disponible y bloquea solo su escenario.
9) WS28 tras WS27+WS12: closeout verify, diagnóstico y handoff CLI/coordinador; sin commit HTTP.
10) WS30 al final, tras WS17/21/22/23/24/25/26/28/42: acta humana UF02–05 y navegación necesaria, con WS17 materializado por WS40; fallo abre tarea en el nodo causante.

Integración: WS12 alimenta todos; G_SOURCE→WS21; G_PAYLOAD_PRECONDITION→WS19/21; WS19→WS21/42; salidas→WS30. Validaciones: roundtrip/conflicto/protegidos, precondición obsoleta/vigente, buffer, ack≠aprobación, Board route≠ejecución, evidencia distinta, closeout por commit/`deskops show task`, materialización válida/no disponible y acta humana. Si falta WS13/17/22/23/24 o un gate, parar y registrar hueco.

FUTURO
Otros nodos producen WS12, WS13, WS17, WS22, WS23, WS24, WS40, WS16/G_HUMAN_READ y WS43; el humano acepta deltas y acta. PK05 no los ejecuta.
