# Executor comparison — WS24, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

# REFORMULACION

**Propósito:** integrar conocimiento y grafo local reutilizando el gráfico existente y una vista genérica de documento registrada en `shell/registry.js`, cubriendo átomos/protoátomos/crossroads (WS02/WS09), materializaciones, pills, clasificación y vecindad.
**Resultado:** navegación ida/vuelta por fuentes y backlinks; Markdown no modelado visible y navegable con su ruta de origen; clasificación (tipo y tags) y vecindad de hasta 2 hops; sin renderer nuevo obligatorio por clase.
**Repo:** graph_ui.
**Límites:** depende de WS13 (lector/explorador, vía sus hijos) y WS09 (catálogo); API de grafo y tags provienen de WS03/WS11; ViewDoc WS18 es opcional y no bloquea; G_UI_READ por delta; reutiliza a1b2b22 sin duplicar implementación.

#

## Hallazgos/disposición contra intención

1 corregida frase heredada: preservar Code local existente a1b2b22, no Code sobre acta. 2 sin modelo/tags declarados se muestra ausencia, no clasificación ficticia. No duplicar lector ni esperar WS18.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
