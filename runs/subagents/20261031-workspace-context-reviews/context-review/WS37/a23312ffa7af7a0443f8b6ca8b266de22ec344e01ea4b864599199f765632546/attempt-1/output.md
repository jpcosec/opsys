REFORMULACION  
Propósito: validar UF06 con un agente Scion real, incluyendo pregunta, intervención, corrección, evidencia, decisión y cierre mediante el handoff de WS28. Resultado: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` conforme al protocolo de `validacion-humana.md`. Repo dueño: `graph_ui`; `output_base: graph_ui:repository_root/`. Límites: no sustituir la integración por mocks ni confundir “completed” con aprobación; requiere `G_EXEC` y `G_SCION`; no bloquea WS31; promoción no autorizada.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas previstas: nodo WS37, gates `G_EXEC`/`G_SCION`/`G_HUMAN_DELEGATE`, `validacion-humana.md`, UF06 en `user-flows.md` y decisiones P08. Cambios previstos: este revisor no modifica nada; el ejecutor futuro produciría el acta de WS37 y su recibo verificable. Dependencias: WS36 y WS30; WS28 queda cubierta transitivamente vía WS30. Gates: `G_EXEC` pendiente y `G_SCION` sin verificar, producido por WS44. Validaciones futuras: ejecutar el guion UF06 con agente real y participante humano; comprobar correspondencia mensaje/intento, decisión humana, evidencia enlazada, corrección y cierre por handoff; registrar actor, versión, comandos, tiempos y resultados; verificar que no hay mocks ni autoaprobación.

FUTURO  
WS44 o el operador designado debe producir la prueba pública de Scion para `G_SCION`. El solicitante humano o su designee decide `G_EXEC` y participa en la validación. Esa persona decide si el acta acredita `G_HUMAN_DELEGATE`. WS38 documentará después lo verificado en WS37. WS31 no depende de este nodo.
