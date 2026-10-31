# Executor comparison — WS26.2, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
Propósito: implementar en `graph_ui` el enrutamiento explícito de tareas en el Board y una vista de “capa lista” basada en dependencias y solapamiento de `files`. Resultado: tras enrutar, `deskops show board` muestra la tarea y la UI separa capa lista, ejecución, dependencias pendientes y solapamientos. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/routing/` y `tests/`. Límites: no implementar promoción nueva; usar solo una operación completa admitida por WS12 o dejar handoff/pendiente; no editar `status`; no marcar lista con globs dudosos ni heurística optimista.

##

## Hallazgos/disposición contra intención

Descartado: «no comprobado» es el resultado visible obligatorio ante glob/resolución dudosa; revisión supervisor es acto del rol de workflow del repo, que TaskDoc/promoción identifica, no autorización UI nueva ni override de API. WS12 produce normalización y canal; nada requiere que el renderer invente actor o marque ready por sí mismo. Escenario de aceptación puede y debe mantener no comprobado hasta evidencia/no solapamiento.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
