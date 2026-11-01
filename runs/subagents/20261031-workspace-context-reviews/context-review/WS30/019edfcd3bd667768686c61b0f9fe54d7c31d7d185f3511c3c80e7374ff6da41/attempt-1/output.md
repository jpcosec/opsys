## REFORMULACION
WS30 es una validación humana en `graph_ui`: una persona recorre UF02, UF03 con edición, UF04, UF05 y UF01 usando entradas WS17 materializadas por WS40; ejecuta escenarios de error, conflicto en dos ventanas y navegación por teclado del guion WS08 y `validacion-humana.md`. Resultado: acta en `runs/subagents/workspace-documental-acceptance/manual/` y satisfacción de `G_HUMAN_MANUAL`. Límites: no inventar causalidad, no corregir otros repos, un fallo bloquea el gate, tests no equivalen a “ready”, sin mutar el desk de desarrollo.

## AMBIGUEDADES
1. «el responsable del repo dueño abre tarea en el nodo que lo causó» y «que supervisor receptor autorice diagnóstico antes de atribuir nodo»: no se identifica qué actor abre la tarea ni qué repo responde cuando el nodo causante pertenece a otro repo (p. ej. WS17 en `deskops`), ni quién es el «supervisor receptor». Obligaría a inventar actor y repo de destino.
2. «un fallo de guion bloquea el gate […] una observación solo se registra»: no se define el criterio que separa fallo de observación. Obligaría a inventar cuándo el gate queda bloqueado.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS30 y vecinos), `validacion-humana.md`, el guion WS08, las plantillas WS17, el manifiesto/corpus WS40 y los contratos WS11/WS12. Crearía `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` con participante, versión/commit, recorridos, entradas WS17 validadas, paths/hashes, resultados y ayudas; añadiría capturas/grabación si el protocolo lo exige y registraría el commit atómico. No editaría el plan ni otros repos. Consumiría WS17 materializado por WS40, WS21 (fuente/render y buffer), WS22 (Board), WS23 (procedimiento), WS24 (conocimiento), WS25 (captura), WS26 (autoría/Board), WS28 (handoff de cierre) y WS42 (split/merge/tipado), con sus gates técnicos. Validaría que la persona completa el guion sin instrucciones verbales correctivas, que el acta enumera rutas/hashes y que `G_HUMAN_MANUAL` enlaza acta y commit. Errores: plantilla WS17 ausente → detener y registrar hueco; fallo aislado → gate bloqueado y tarea en el nodo causante; causa no aislada → incidente con repo/superficie y diagnóstico autorizado.

## FUTURO
WS43 y WS31 consumen el acta; el participante humano decide la aceptación; el responsable del repo causante abre la corrección y el supervisor autoriza el diagnóstico.
