## REFORMULACION

Encargo: validar con una persona y un agente Scion reales el recorrido UF06 de delegación e intervención (pregunta, respuesta/decisión, corrección, evidencia y cierre por el handoff de WS28), tras integrar WS36 y el recorrido manual WS30. Resultado: acta humana versionada en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, con guion, actor, versión, resultados y soportes, que además resuelve `G_HUMAN_DELEGATE`. Repo dueño: `graph_ui`. Límites: no sustituir integración por mocks ni confundir `completed` con aprobación; no bloquea WS31; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro, con `G_EXEC` autorizado y `G_SCION` verificado por WS44, leería `task-ws37.md`, las salidas de WS36, el protocolo de `validacion-humana.md`, el acta de WS30 y la evidencia del probe Scion. No modificaría código de producto.

Cambios previstos: crear guion y acta bajo `runs/subagents/workspace-documental-acceptance/delegacion/` en `graph_ui`, incluyendo versiones/commits, comandos públicos, timestamps, intento, mensajes, decisión humana, corrección, evidencia enlazada, fallos y resultado explícito. El acta sería el soporte de `G_HUMAN_DELEGATE`; no se copiaría al plan.

Dependencias: WS36 debe ofrecer invocación real del adaptador WS34 y registro WS33.2; WS30 debe haber validado autoría/revisión manual. Consumiría `G_EXEC` como permiso externo registrado y `G_SCION` como contrato público comprobado. Si falta cualquiera, se detendría y registraría el hueco con repo dueño, sin crear sustituto.

Casos de error: Scion inaccesible o sin permisos debe mostrarse como error, no simularse; respuesta no vinculada al intento invalida la validación; integración mockeada invalida el acta; autoaprobación o `completed` usado como aprobación invalida el gate; fallo del guion bloquea el gate y abre corrección en el nodo causante.

Validación esperada: la persona completa el recorrido sin rutas memorizadas ni correcciones verbales; el acta enlaza commit/blob verificables y demuestra decisión humana separada del resultado del agente.

## FUTURO

Tras WS37, WS38 publica capítulos verificados de delegación y átomos durables. `G_HUMAN_DELEGATE` queda resuelto por el acta; `G_EXEC` lo aporta el solicitante o designado; `G_SCION` lo produce WS44. La promoción de WS37 requiere decisión humana y preflight de solo tarea.
