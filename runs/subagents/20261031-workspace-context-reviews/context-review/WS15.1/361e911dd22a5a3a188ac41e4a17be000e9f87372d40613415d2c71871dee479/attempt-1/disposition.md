# Executor comparison — WS15.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
Encargo: definir e implementar en graph_ui la presentación de errores de lectura y modo degradado del lector, como delta sobre el workspace integrado. Resultado: el panel afectado muestra referencia rota, documento ausente, modelo no importable, backend caído, fuente no editable y fallo CDN, sin borrar historial, pestañas ni foco, y sin fingir vacío; un reintento manual recupera el estado. Repo: graph_ui; salida en `frontends/mindmap/views/workspace/errors/` más `tests/`. Límites: solo lectura/error, sin empaquetado offline; depende de WS13, del contrato de lectura WS11 y del gate G_UI_READ por delta; no autoriza promoción.

##

## Hallazgos/disposición contra intención

Corregido contrato completo, sin caveats contradictorios: read-only es límite, no fallo de lectura; red sin respuesta/CDN distinguidos por contrato WS11 y prueba; reintento backend tras restaurarlo conserva estado, no exige offline ni otro lector/guardado.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
