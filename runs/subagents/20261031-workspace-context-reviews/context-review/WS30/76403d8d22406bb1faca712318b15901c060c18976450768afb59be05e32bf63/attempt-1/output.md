REFORMULACION
Propósito: validar con una persona el recorrido manual completo de autoría y revisión (UF02, UF03 edición, UF04, UF05) y UF01 con entradas authored de WS17 materializadas por WS40. Resultado: acta humana bajo protocolo en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, evidencia de `G_HUMAN_MANUAL`. Repo dueño: `graph_ui`. Límites: no implementa; no declara ready por tests; los problemas abren tareas de corrección; depende de WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28 y WS42. Aceptación: registro humano bajo protocolo y problemas convertidos en tareas de corrección de la misma capa; no llamar ready a un flujo solo por tests.

AMBIGUEDADES
1. Cita: «errores, teclado, dos ventanas y conflictos, con historial». Obliga a inventar qué errores, qué interacciones de teclado y qué «historial» —navegación, diff o tarea— deben probarse, y con qué resultado esperado.
2. Cita: «problemas implican tareas de corrección de la misma capa». Obliga a inventar qué cuenta como «problema» frente a observación, qué es «la misma capa» y si toda observación abre tarea o solo el fallo que bloquea el gate.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows, nodo WS30 y aristas vecinas solo como contexto. Cambios previstos: ninguno. Dependencias: WS40 vía WS17 para corpus; WS21 según variante P04; WS25/WS26 agregados; WS28 para cierre externo; WS42 para operaciones de conocimiento; `G_HUMAN_MANUAL` pendiente. Validaciones futuras: acta versionada y enlazada en `graph_ui`, participante designado, corpus WS40 y variante de edición aplicable.

FUTURO
Un humano resuelve P04 (`source_mode`) y P08 (participante); WS21 entrega la variante elegida; WS40 materializa las entradas de WS17; WS28/WS42 aportan capacidades; la tarea de validación del repo dueño versiona el acta; `G_HUMAN_MANUAL` se resuelve con esa evidencia, no por inferencia.
