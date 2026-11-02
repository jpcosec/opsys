REFORMULACION
WS30 es un nodo de validación ejecutable, no un agregado. Su propósito es que una persona recorra UF02, UF03-edición, UF04 y UF05 sobre el ejemplo Taller, más UF01 con entradas authored de WS17 materializadas por WS40, registrando un acta humana. El resultado es evidencia y el gate G_HUMAN_MANUAL, en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/`. Límites: no implementa ni corrige otros repos, no declara flujos disponibles por tests, no sustituye la lectura de WS16 y no autoriza Scion.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08»: WS08 no figura en `depends_on` ni se aporta su guion. Obliga a inventar de dónde obtenerlo y si debe estar terminado antes de WS30.
2. «que supervisor receptor autorice diagnóstico antes de atribuir nodo»: no se identifica ese actor ni su repo/canal. Obliga a inventar quién autoriza y cómo se registra.
3. «un fallo de guion bloquea el gate…; una observación solo se registra»: no hay criterio que separe fallo de observación, y `validacion-humana.md` habla de «fallo de recorrido». Obliga a inventar la clasificación y permitiría degradar un fallo real a observación.

DRY-RUN
Un ejecutor leería guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y el nodo. Comprobaría gates de WS21/WS25/WS26/WS28/WS42 y consumiría: plantillas WS17, corpus WS40, fuente/render WS21, Board WS22, procedimientos WS23, grafo WS24, captura WS25, autoría WS26, handoff WS28 y split/merge WS42. Crearía el directorio de acta en graph_ui, ejecutaría el guion con la persona, y guardaría acta con recorridos, capturas, métricas del protocolo (20 aperturas, 10 búsquedas, 10 guardados) y lista de plantillas/entradas WS17 con paths/hashes para WS43. Si un fallo no se aísla, registraría incidente repo/superficie. Validaría que la persona completa sin instrucciones verbales correctivas; un fallo de recorrido bloquearía el gate. Sin ejecutar nada aquí.

FUTURO
La persona firmante decide el acta y resuelve G_HUMAN_MANUAL. El repo dueño abre la tarea de corrección si el guion falla. WS31 publica el manual usando el acta; WS43 contrasta la lista de WS17 validada para la publicación real. WS37 consume WS30, pero sigue sujeto a G_EXEC/G_SCION.
