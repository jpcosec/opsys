## REFORMULACION

WS26 es un **agregado no ejecutable** de implementación en `graph_ui`: integrar autoría y contexto de tareas mediante sus hijos WS26.1 y WS26.2. Su resultado son las salidas agregadas de ambos, no un artefacto propio. Límites: no reemplazar el workflow por drag-and-drop; enrutar en Board no equivale a ejecutar; la promoción solo procede cuando el contrato WS12 resuelve commits previos por canal autorizado; las mutaciones en UI no se habilitan sin G_HUMAN_READ; G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta; G_CLOSEOUT ya está satisfecho.

## AMBIGUEDADES

ninguna

## DRY-RUN

Al ser agregado, un ejecutor futuro no ejecuta nada propio: recorre el cumplimiento de sus hijos.

- **WS26.1** consume el contrato WS12 y la representación Board de WS22. Cambia `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados y `tests/`. Produce autoría desde candidato con evidencia declarada, dependencias y pills vinculadas, visibles tras recargar; nunca edita `status` para avanzar. Si una operación Git carece de contrato/dueño, deja handoff y la declara no disponible. Transfiere a WS26.2 una tarea ya autorada con su contexto.
- **WS26.2** recibe esa salida y añade `views/workspace/routing/`, endpoints autorizados y `tests/`. Invoca solo una operación de promoción completa admitida por WS12; si falta, prepara handoff. Valida `deskops show board`, distingue tarea enrutada de una en ejecución y separa la capa lista de tareas con dependencias pendientes o archivos solapados; glob o resolución dudosa queda no comprobado y requiere revisión del supervisor.

Validación conjunta: aceptación de ambos hijos más recibos per_delta de G_WRITE_CONTRACT y G_UI_WRITE para WS26/WS26.1/WS26.2. G_HUMAN_READ pendiente solo bloquea habilitar mutaciones en UI; pruebas aisladas de API pueden avanzar. WS30 verifica después UF04/UF05 sobre TaskDoc real.

## FUTURO

WS12 publica el contrato de operaciones; WS22 entrega la representación Board; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite actas G_UI_WRITE por delta. El TaskDoc de promoción fija archivos, endpoints y pruebas concretas. WS30 realiza la validación humana completa.
