# Executor comparison — WS30, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
**Propósito:** validar con una persona real que UF01 (con entradas authored WS17), UF02, UF03 en edición, UF04 y UF05 funcionan en el ejemplo integrado, bajo el protocolo de `validacion-humana.md`, incluyendo error, conflicto en dos ventanas y navegación por teclado. **Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` que satisface `G_HUMAN_MANUAL`, enumerando plantillas/entradas WS17, paths/hashes y recorridos. **Repo dueño:** graph_ui. **Límites:** no implementa, no corrige otros repos, no declara "ready" por tests, no inventa causalidad de fallos; una observación solo se registra. Promoción no autorizada.

##

## Hallazgos/disposición contra intención

1 descartado: WS30→WS17→WS11→WS08 y WS30→WS21→WS19→WS12→WS08, prerrequisitos transitivos cuentan según alcance.md. 2 G_HUMAN_READ transita por mutaciones WS19/25/26/28/42; no requiere gate duplicado para saltarse dependencia. 3 repo dueño de causa es el que tiene owner_repo del nodo, no permiso para escribir desde graph_ui; supervisor receptor coordina diagnóstico, tarea correctiva se captura en repo dueño y sin causa aislada no se inventa. Dry-run entiende protocolo y acta real.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
