# Executor comparison — WS19.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
WS19.1 es un encargo de implementación para que `graph_ui` edite campos del workspace reutilizando editores y la API del contrato WS12, con revisión hash CAS y conflicto visible. Resultado: UI de edición de campos con guardado/recarga verificable, rechazo de escritura obsoleta conservando el texto local y campos workflow-protected no editables, más tests. Repo dueño: `graph_ui`; salida en `frontends/mindmap/views/workspace/fields/` y `tests/`, consumiendo endpoints WS12 sin cambios de contrato. Límites: solo campos (no relaciones, que corresponde a WS19.2), no raw-source, otros modos read-only hasta contrato; G_HUMAN_READ solo habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas de API; no duplicar la base a1b2b22.

##

## Hallazgos/disposición contra intención

Hallazgo descartado: scope remite P03 y depends_on WS12; contrato WS12 tiene explícitamente «policy coordinador», canal/actor/permisos y «lock solo UI no coordina CLI/agentes». Por tanto modo manual exclusivo y su señal/canal lo produce WS12, no el renderer ni una bandera inventada. Si no puede probarse, regla común mantiene lectura/handoff. Dry-run y futuro reconocen contrato/whitelist y límite.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
