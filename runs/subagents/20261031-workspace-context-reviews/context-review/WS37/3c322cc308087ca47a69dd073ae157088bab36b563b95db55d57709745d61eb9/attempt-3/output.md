## REFORMULACION
WS37 es una validación de entrega en `graph_ui`: una persona debe recorrer UF06 real con Scion —pregunta, intervención, corrección, evidencia y decisión— y cerrar por el handoff de WS28. Produce un acta humana en `runs/subagents/workspace-documental-acceptance/delegacion/`. Depende de WS36 y WS30; exige G_EXEC y G_SCION. Límites: no sustituir la integración por mocks, no confundir “completed” con aprobación, no bloquear WS31 y no ejecutar dispatch/mensajes sin autorización.

## AMBIGUEDADES
Ninguna. El actor humano, el guion y el registro del acta quedan cubiertos por `validacion-humana.md`; el handoff de WS28 es un contrato de un nodo existente y WS28 ya es prerrequisito transitivo vía WS30. Los gates pendientes son intencionales y tienen productor declarado.

## DRY-RUN
Un ejecutor futuro leería el nodo WS37, `validacion-humana.md`, el acta de WS30, la integración entregada por WS36, el contrato del adaptador WS34/WS35 y el handoff de cierre de WS28. Antes de actuar comprobaría G_EXEC en `autorizaciones/scion.md` y G_SCION mediante el probe de WS44; si falta cualquiera, se detendría registrando el hueco con repo dueño, sin crear sustituto. Con gates satisfechos y promoción autorizada, prepararía el entorno Taller, ejecutaría el escenario con el participante humano y Scion real, y escribiría `delegacion/acta.md` con actor, versión/commit, guion, resultados, evidencias y decisión explícita. El commit atómico iría en `graph_ui`, no en el plan. Validaría que cada mensaje/resultado corresponde al intento correcto, que la revisión muestra actor y evidencia, y que “completado” no se registra como aprobado. Un fallo de recorrido bloquearía G_HUMAN_DELEGATE y abriría corrección en el nodo causante; un fallo de permisos/API se registraría como error visible, no simulado.

## FUTURO
WS38 publicará los capítulos verificados de delegación solo tras WS37 y WS31, usando el acta y G_HUMAN_DELEGATE. El solicitante o su designee decide la aceptación humana y autoriza G_EXEC; WS44 produce la evidencia de G_SCION. WS31 aporta átomos existentes para enlazar o actualizar.
