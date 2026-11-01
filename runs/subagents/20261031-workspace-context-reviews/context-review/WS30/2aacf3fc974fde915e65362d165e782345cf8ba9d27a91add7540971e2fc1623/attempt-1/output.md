## REFORMULACION
Propósito: validar con una persona el recorrido de autoría y revisión manual —UF02, UF03 edición, UF04, UF05 y UF01 con entradas WS17— bajo `validacion-humana.md`, incluyendo errores, conflicto en dos ventanas y teclado. Resultado: acta humana y resolución de `G_HUMAN_MANUAL`, con plantillas WS17, paths/hashes y recorridos trazables para WS43. Repo dueño: `graph_ui`; salida en `runs/subagents/workspace-documental-acceptance/manual/`. Límites: no declarar ready por tests; una observación solo se registra; no corregir otro repo ni inventar causalidad; el cierre sigue siendo handoff externo; no publica el mapa real.

## AMBIGUEDADES
1. «el responsable del repo dueño abre tarea en el nodo que lo causó»: no aclara si es el responsable de `graph_ui` (owner_repo de WS30) o el del repo del nodo causante; obliga a inventar actor y repo destino.
2. «que supervisor receptor autorice diagnóstico»: «supervisor receptor» no está definido; obliga a inventar quién autoriza y con qué evidencia.

## DRY-RUN
Lecturas: `dag.yaml`, task_file promovido, `validacion-humana.md`, guion de WS08, manifiesto/plantillas WS17, corpus WS40 y contratos de gates. Cambios previstos: acta en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, commit atómico en `graph_ui`, registro de evidencia y resolución de `G_HUMAN_MANUAL`. Consumo: corpus WS40 materializado desde WS17; WS21 fuente/render; WS22 Board; WS23 procedimiento; WS24 conocimiento; WS25 captura; WS26 autoría; WS28 handoff; WS42 split/merge; gates `G_WRITE_CONTRACT`/`G_UI_WRITE`/`G_HUMAN_READ` transitivos. Validación: persona completa el guion sin rutas memorizadas; acta enlaza commit/blob, enumera plantillas/paths/hashes y recorridos; WS43 puede trazar. Errores: falta contrato/dato → detenerse y registrar hueco con repo dueño; fallo aislado → tarea en nodo causante; no aislado → incidente sin atribuir.

## FUTURO
La persona participante decide la aceptación y firma `G_HUMAN_MANUAL`. WS43 consume el acta para publicación real; WS31 usa el acta para el manual. Responsables de repo y supervisor receptor resuelven fallos; este nodo no corrige otros repos.
