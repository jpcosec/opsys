## REFORMULACION
**Propósito:** validar con una persona real que UF01 (con entradas authored WS17), UF02, UF03 en edición, UF04 y UF05 funcionan en el ejemplo integrado, bajo el protocolo de `validacion-humana.md`, incluyendo error, conflicto en dos ventanas y navegación por teclado. **Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` que satisface `G_HUMAN_MANUAL`, enumerando plantillas/entradas WS17, paths/hashes y recorridos. **Repo dueño:** graph_ui. **Límites:** no implementa, no corrige otros repos, no declara "ready" por tests, no inventa causalidad de fallos; una observación solo se registra. Promoción no autorizada.

## AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08» — `depends_on` no incluye WS08. Obliga a inventar si se ejecuta sin el guion refinado de WS08 o si falta esa dependencia (además, `cobertura.md` dice que WS08 refina el guion).
2. «requires: []» frente a un nodo cuyos escenarios exigen mutaciones en UI (captura, edición, conflicto). `validacion-humana.md` dice que habilitar mutaciones de baseline requiere `G_HUMAN_READ`, pero el nodo no declara si lo requiere ni quién lo produce. Obliga a inventar si WS30 puede mutar o debe bloquearse.
3. «el responsable del repo dueño abre tarea en el nodo que lo causó» — no aclara qué "repo dueño" cuando la causa aislada está en WS17 (deskops). Obliga a inventar si el responsable de graph_ui abre tarea en otro repo (lo que `alcance.md` prohíbe) o quién lo hace.

## DRY-RUN
**Lecturas (sin ejecutar):** guide, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y nodo WS30 con sus aristas vecinas (WS17, WS21–WS26, WS28, WS42). **Cambios previstos:** ninguno de código; a futuro, acta y commit atómico en graph_ui. **Dependencias:** directas WS17 (deskops) y WS21/22/23/24/25/26/28/42 (graph_ui); transitivas WS11, WS12, WS40 (vía WS17); gates heredados G_SOURCE/G_WRITE_CONTRACT/G_UI_WRITE; G_HUMAN_MANUAL producido aquí. **Validaciones futuras:** acta versionada y enlazada al recibo del gate; contraste de paths/hashes WS17; corpus WS40 con instrucciones reproducibles.

## FUTURO
WS43 trazará la publicación real desde el acta; WS31 redactará el manual desde WS30/WS43; el supervisor receptor autoriza diagnóstico antes de atribuir nodo; el participante humano decide aceptación; la promoción fijará archivos y TaskDoc.
