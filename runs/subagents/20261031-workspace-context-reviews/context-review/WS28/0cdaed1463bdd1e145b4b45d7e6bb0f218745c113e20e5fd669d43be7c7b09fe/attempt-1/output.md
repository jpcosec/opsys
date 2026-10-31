## REFORMULACION
**Propósito:** integrar en `graph_ui` la verificación del resultado de un cierre externo y el handoff explícito con evidencia.  
**Resultado:** vista/endpoints/tests en `frontends/mindmap/views/workspace/review/`, `endpoints` y `tests/` que confirmen el cierre real y refresquen estado.  
**Repo:** `graph_ui`.  
**Límites:** sin commit/cierre por HTTP en baseline; sin terminal embebido genérico; promoción no autorizada; el cierre ocurre por CLI/coordinador externo.

## AMBIGUEDADES
1. «Verificar con autoridad Deskops» no identifica la API, comando, estado o artefacto concreto que constituye esa autoridad. Obligaría a inventar cómo consultar el resultado real y qué fuente prevalece frente al contrato de WS12.
2. «ofrecer handoff explícito a closeout CLI/coordinador» plantea dos canales alternativos sin criterio de elección ni forma de confirmación. Obligaría a inventar cuál se implementa y qué evidencia demuestra que el cierre externo terminó, pese a que «comando o solicitud no equivalen a cierre».
3. La lista `requires` incluye `G_HUMAN_READ` sin relación declarada con el cierre. Obligaría a inventar por qué la aprobación del recorrido de lectura condiciona la verificación/handoff de WS28.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura y nodo WS28; `task_file` referenciado no viene suministrado.  
**Cambios previstos:** UI de revisión, endpoints y tests; handoff y diagnóstico de faltantes; ningún cierre/commit HTTP ni terminal.  
**Dependencias:** WS27 aporta diff/evidencia; WS12 aporta contrato de operaciones. Gates requeridos: `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.  
**Validaciones futuras:** gates satisfechos con evidencia; WS30 valida UF05 en recorrido manual.

## FUTURO
WS12 produce y verifica el contrato/whitelist y las aceptaciones de escritura. WS27 entrega diff y artefactos de evidencia. El cierre externo produce commit y prueba de contrato. El humano resuelve gates y autoriza promoción. WS30 registra la aceptación manual.
