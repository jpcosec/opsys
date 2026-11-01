## REFORMULACION

WS37 valida UF06 con un agente Scion real: pregunta, intervención, corrección, evidencia, decisión humana y cierre mediante el handoff de WS28. El resultado es un acta en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` que registra actor humano, versión, guion, resultado y soportes. Repo dueño: `graph_ui`. Límites: no sustituir la integración por mocks ni `completed` por aprobación; no autoaprobar; no habilitar dispatch, mensajes o Scion por el plan; no bloquear WS31; promoción `not_authorized`. Requiere G_EXEC y G_SCION.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas: `task-ws37.md`, `validacion-humana.md`, contratos de WS36 y WS30 como dependencias, y definiciones de gates en `dag.yaml`; si existe, `autorizaciones/scion.md`.

Cambios previstos: crear/actualizar únicamente el acta bajo `output_scope`, con actor humano, versión/commit, guion, resultados, fallos y soportes. No se modifica código de `graph_ui`.

Dependencias consumidas: la integración de delegación/intervención de WS36 y la aceptación manual de WS30. Gates: G_EXEC debe estar autorizado externamente; G_SCION debe provenir del probe/contrato de WS44. Si faltan, el ejecutor se detiene, registra el hueco con repo dueño y no crea sustituto.

Validaciones futuras: ejecutar el guion con Scion real y participante humano; comprobar que mensajes, respuestas y decisiones quedan vinculados al intento correcto; verificar evidencia y cierre por handoff WS28; confirmar ausencia de mocks y que completado por agente no equivale a aprobado. El acta debe permitir satisfacer G_HUMAN_DELEGATE.

## FUTURO

WS44 produce el contrato/probe público de Scion que respalda G_SCION. Un humano o designado autoriza G_EXEC y ejecuta la aceptación como participante. WS38 publica los capítulos verificados de delegación usando el acta de WS37 y átomos de WS31. WS36 y WS30 aportan sus resultados previos; WS31 no depende de WS37.
