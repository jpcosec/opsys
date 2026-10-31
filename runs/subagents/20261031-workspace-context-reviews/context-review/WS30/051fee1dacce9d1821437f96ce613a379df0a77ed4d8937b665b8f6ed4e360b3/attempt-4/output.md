REFORMULACION
Propósito: validar con una persona real la autoría y revisión manual del workspace documental (UF02, UF03 edición, UF04 y UF05), integrando conocimiento y tarea en el ejemplo, con los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y `validacion-humana.md`, e incluyendo UF01 con entradas authored de WS17 materializadas por WS40. Resultado: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` y gate `G_HUMAN_MANUAL`. Repo dueño: `graph_ui`. Límites: nodo de validación; `promotion: not_authorized`; no implementa UI; no declara un flujo “ready” solo por tests; un fallo de guion bloquea el gate.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS30 y vecinos), `validacion-humana.md`, guion de WS08 —transitivo vía WS11/WS12—, corpus WS40 y entradas WS17, y contratos/actas de WS21–WS26, WS28 y WS42. Cambios previstos: solo registro y evidencias bajo `manual/`; ninguna mutación de código ni de otros repos. Dependencias: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28 y WS42; transitivas WS40, WS12 y WS08. Validaciones futuras: recorrido humano conforme al protocolo, registro de versiones, comandos, resultados, capturas y decisión explícita; el gate solo pasa con acta verificable y commit en el repo dueño. No se ejecuta nada en esta revisión.

FUTURO
P04 (`source_mode`) y P08 (participante, ejemplo y umbrales) los decide un humano; WS08 produce el guion detallado; WS40 materializa las entradas de WS17; el participante firma el acta. Si el recorrido falla, corresponde abrir una tarea de corrección en el nodo causante y en su repo dueño, sin que esta revisión la cree ni la sustituya.
