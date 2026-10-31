REFORMULACION

Propósito: validar UF06 (delegación e intervención) con un agente Scion real y actor humano, cubriendo pregunta, intervención, corrección, evidencia, decisión y cierre por el handoff de WS28. Resultado: acta de aceptación en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, que produce `G_HUMAN_DELEGATE`. Repo dueño: `graph_ui`. Límites: no sustituir integración por mocks ni "completed" por aprobación; no bloquea WS31; promoción no autorizada; depende de WS36 y WS30; requiere `G_EXEC` y `G_SCION`.

AMBIGUEDADES

1. «G_SCION/G_EXEC y protocolo» (acceptance). No identifica qué protocolo: `validacion-humana.md` es el único protocolo suministrado, pero el nodo no lo cita ni concreta qué pasos o evidencia de ese protocolo aplican a UF06. Obligaría a inventar el protocolo de aceptación o a elegir entre fuentes. Cita textual: «acceptance: G_SCION/G_EXEC y protocolo».

DRY-RUN

Lecturas previstas: nodo WS37, vecinos WS36/WS30, gates `G_EXEC`/`G_SCION`/`G_HUMAN_DELEGATE`, `user-flows.md` UF06, `validacion-humana.md` y `alcance.md`. Cambios previstos: ninguno en código; solo revisión y, si se ejecutara, acta en el `output_scope`. Dependencias: WS36 (integración) y WS30 (validación manual) como prerrequisitos directos; `G_EXEC` pending y `G_SCION` unverified como gates; WS28 transitivo vía WS30 para el cierre. Validaciones futuras: acta con actor humano, versión, guion, resultado y soportes; comprobar ausencia de mocks y de autoaprobación; verificar que "completed" no se trata como aprobado; enlazar la evidencia en `graph_ui`, no en el paquete de planificación.

FUTURO

WS44, con operador designado en WS07, produce `G_SCION`; el humano resuelve `G_EXEC`; WS38 publica los capítulos verificados de delegación; WS37 produce `G_HUMAN_DELEGATE` y el acta; WS31 no se bloquea. La promoción de WS37 exige preflight y archivos/pills/átomos/evidencia precisos, no autorizados aquí.
