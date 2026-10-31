## REFORMULACION
**Propósito:** revisar si WS30 se entiende como encargo de planificación: validación humana de autoría y revisión manual completas.
**Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, bajo el protocolo de `validacion-humana.md`, con guion, versión, resultados y soportes.
**Repo dueño:** `graph_ui`.
**Límites:** no ejecutar; `promotion: not_authorized`; no declarar `ready` por tests; usar corpus WS40 y entradas WS17 materializadas; no revisar contratos de nodos vecinos.

## AMBIGUEDADES
1. **Dependencia ausente para el guion.** Cita: «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS30 no incluye WS08 en `depends_on` y no se deduce de sus dependencias listadas. Obliga a inventar el guion, asumir que WS08 ya lo produjo o decidir si basta `validacion-humana.md`.

## DRY-RUN
**Lecturas previstas:** `dag.yaml#node:WS30`; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `validacion-humana.md`; `borradores/user-flows.md`; guía de revisión; contratos de vecinos WS17/21/22/23/24/25/26/28/42 y gate G_HUMAN_MANUAL, solo como contexto.
**Cambios previstos:** ninguno en esta revisión. Si se promoviera: `desk/drawer/tasks/workspace-documental/task-ws30.md` y, en ejecución humana, el acta en `graph_ui`.
**Dependencias:** WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42; transitivas relevantes: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT, G_CLOSEOUT. P04 pendiente bloquea WS21 y, por tanto, WS30.
**Validaciones futuras:** acta humana con actor, versión, guion, resultado y soportes; el fallo de guion abre tarea en el nodo causal y bloquea G_HUMAN_MANUAL; una observación no equivale a aprobación.

## FUTURO
- WS08 debe aportar el guion referido o confirmar su ausencia; no lo decide este nodo.
- El participante designado por P08 ejecuta el recorrido y firma el acta.
- WS30 produce G_HUMAN_MANUAL; WS31 y WS43 consumen el acta.
- P04 y P08 son decisiones humanas pendientes, no ambigüedades de este encargo.
