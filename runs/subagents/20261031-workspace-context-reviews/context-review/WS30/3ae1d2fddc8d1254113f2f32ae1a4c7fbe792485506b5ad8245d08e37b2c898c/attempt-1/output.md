REFORMULACION
WS30 es un nodo de validación en `graph_ui`: una persona recorre UF02, UF03 edición, UF04, UF05 y UF01 con entradas WS17 materializadas por WS40, bajo `validacion-humana.md` y el guion de WS08. Resultado: acta en `runs/subagents/workspace-documental-acceptance/manual/` que enumera plantillas/entradas WS17, paths/hashes y recorridos; produce `G_HUMAN_MANUAL`. Límites: no implementa, no fija textos/archivos exactos (TaskDoc), no corrige otros repos; un fallo bloquea el gate y una observación solo se registra; tests no equivalen a ready.

AMBIGUEDADES
1. «el responsable del repo dueño abre tarea en el nodo que lo causó»: no se nombra al responsable de `graph_ui` ni cómo identificarlo; obligaría a inventar el actor que abre la tarea de corrección.
2. «que supervisor receptor autorice diagnóstico antes de atribuir nodo»: «supervisor receptor» no está definido; obligaría a inventar quién autoriza o a atribuir esa autoridad al ejecutor.
3. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08»: WS08 no figura en `depends_on` de WS30 ni se fija qué hacer si el guion falta; obligaría a inventar escenarios o asumir un guion no garantizado.

DRY-RUN
Un ejecutor futuro leería `task-ws30.md`, `validacion-humana.md`, el guion de WS08, plantillas WS17, manifiesto WS40 y contratos WS11/WS12. Prepararía Taller y verificaría las entradas materializadas. Con la persona participante ejecutaría UF01/02/03 edición/04/05, errores, conflicto en dos ventanas y teclado; registraría comandos, versiones/commits, timestamps, observaciones y 20 aperturas, 10 búsquedas y 10 guardados. Crearía `runs/subagents/workspace-documental-acceptance/manual/acta.md` y evidencias con paths/hashes WS17, y las incluiría en el commit atómico. Consumiría WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42 y, transitivamente, WS40 y gates técnicos. Validaría que la persona completa el guion sin rutas memorizadas ni correcciones verbales y que el acta enlaza commit/blob. Un fallo bloquearía `G_HUMAN_MANUAL`; si la causa no está aislada, registraría incidente con repo/superficie.

FUTURO
WS08 produce el guion; WS40 el corpus; WS17 las plantillas; la persona P08 ejecuta y decide; el responsable de `graph_ui` abre correcciones; el supervisor autoriza diagnóstico si procede; WS43 traza la publicación desde el acta y WS31 la cita.
