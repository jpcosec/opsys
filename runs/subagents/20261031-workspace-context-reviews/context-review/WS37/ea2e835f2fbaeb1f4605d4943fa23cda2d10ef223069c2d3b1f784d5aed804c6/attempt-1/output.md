REFORMULACION
Propósito: validar UF06 con agente Scion real y actor humano, cubriendo pregunta, intervención, corrección, evidencia, decisión y cierre mediante el handoff de WS28. Resultado: acta y evidencia en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, y resolución de `G_HUMAN_DELEGATE`. Repo dueño: `graph_ui`; `output_base: graph_ui:repository_root/`; nodo `validation`, rol `delivery`. Límites: no sustituir integración por mocks ni confundir `completed` con aprobación; no bloquea WS31; promoción no autorizada; requiere `G_EXEC`, `G_SCION` y el protocolo de `validacion-humana.md`. Este revisor no ejecuta nada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: nodo y gates de `dag.yaml`, `validacion-humana.md`, UF06 en `user-flows.md` y contratos de dependencias WS36/WS30. Cambios previstos: ninguno durante la revisión; al ejecutarse el nodo, un acta en `output_scope` y la evidencia de `G_HUMAN_DELEGATE`. Dependencias: WS36 y WS30; `G_EXEC` externo; `G_SCION` producido por WS44; participante humano según P08. Validaciones futuras: recorrido UF06 con Scion real, acta con actor humano, versión, guion, resultado y soportes; comprobar ausencia de mocks y de autoaprobación; verificar que un fallo bloquea el gate. Sin ejecución.

FUTURO
Decisiones o producciones de otros: autorización `G_EXEC`, probe/contrato público de WS44 para `G_SCION`, implementación WS36, validación WS30 y publicación WS38. WS37 produce el acta y resuelve `G_HUMAN_DELEGATE`; un humano decide la aprobación.
