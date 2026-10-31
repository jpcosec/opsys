REFORMULACION
Propósito: revisar WS30 como encargo de validación humana de autoría y revisión manual, no como implementación. Resultado: acta humana y decisión de `G_HUMAN_MANUAL`; un fallo bloquea el gate y abre tarea en el nodo causal. Repo dueño: `graph_ui`; salida en `runs/subagents/workspace-documental-acceptance/manual/`. Límites: no ejecutar, no revisar vecinos, no resolver P04/P08 y no declarar `ready` por tests.

AMBIGUEDADES
1. Cita: «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». `WS08` no figura en `depends_on` de WS30 y `validacion-humana.md` no fija el guion de teclado; esto obligaría a inventar esos escenarios o a suponer una dependencia no declarada.

DRY-RUN
Lecturas previstas: nodo WS30, guía, `validacion-humana.md`, `cobertura.md`, `user-flows.md` y decisiones P04/P08; contratos de WS17/21/22/23/24/25/26/28/42 solo como dependencias. Cambios previstos: ninguno de código; acta en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` y, si falla el guion, tarea correctiva en el nodo causal. Dependencias: las listadas; WS40 llega vía WS17; el guion de WS08 no está declarado. Validaciones futuras: UF01 con entradas WS17 materializadas por WS40 y UF02/03/04/05, errores, conflicto en dos ventanas, teclado, registro humano y gate. Sin ejecutar.

FUTURO
P04 (`source_mode`) y P08 (participante/umbrales) los decide un humano. WS08 produciría el guion si se declara como dependencia; WS40 materializa el corpus; WS17 aporta entradas; WS25/WS26 cierran cuando cierran sus hijos. El participante firma el acta, el nodo causal recibe la tarea correctiva y WS31 consume el acta. No son ambigüedades de WS30.
