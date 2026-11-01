## REFORMULACION
Propósito: agrupar el ramal Scion opcional posterior con intentos, trazas e intervención verificables. Resultado: paquete integrado por identidad de intento/cierre, mensajes/decisiones, dispatch/reply autorizado, trazas/UI, validación humana y publicación del capítulo. Repo dueño: `deskops`; WS35–WS37 pertenecen a `graph_ui`. Límites: PK08 no ejecuta ni autoriza tareas, no añade aristas, no duplica el pipeline Scion, no convierte permisos de núcleo en dispatch, no admite mocks ni `completed` como aprobación; sin acceso real el ramal queda bloqueado y WS38 espera WS37/WS31.

## AMBIGUEDADES
ninguna

## DRY-RUN
PK08 es un agregado no ejecutable: termina cuando terminan sus hijos. Un ejecutor futuro haría: 1) con WS05/WS07 disponibles, WS44 ejecuta el probe read-only, escribe `auditoria/scion-probe.md` y solo una respuesta real con actor/Hub/fecha/capabilities satisface G_SCION; si falta, se detiene y no avanza WS32. 2) WS32 (WS32.1/.2) fija identidad intento/manifiesto/RunDoc/cierre idempotente sin red y entrega esa base a WS33. 3) WS33 (WS33.1/.2) vincula mensajes/resultados/decisiones con procedencia y dedup; entrega modelo/API a WS34 y WS35. 4) WS34 (WS34.1/.2) adapta dispatch/reply separando intent/confirmed, con timeout/errores y autoridad; requiere G_EXEC y entrega el adaptador a WS36. 5) WS35 consume WS33 y WS27 y muestra intento/tarea/fuente/evidencia; puede avanzar en paralelo a WS34. 6) WS36 integra UI solo contra WS34 y WS33.2; exige G_EXEC/G_SCION/G_UI_WRITE/G_WRITE_CONTRACT. 7) WS37 ejecuta el recorrido real UF06 con humano y acta en `runs/subagents/.../delegacion/`, tras WS36 y WS30. 8) WS38 publica en `docs/workspace-user-manual.md` y átomos, tras WS37 y WS31. Integración esperada: la identidad de WS32 aparece en mensajes WS33, dispatch WS34, trazas WS35 y UI WS36; WS37 valida el conjunto sin mocks. Si falta contrato/API/permiso: parar y registrar hueco, sin sustituto; fallo del probe bloquea el ramal y fallo del acta bloquea WS38.

## FUTURO
WS44 y el operador designado producen G_SCION; un humano externo otorga G_EXEC y firma el acta WS37; WS30/WS31 aportan validación y manual base; WS12 fija la política de timeout.
