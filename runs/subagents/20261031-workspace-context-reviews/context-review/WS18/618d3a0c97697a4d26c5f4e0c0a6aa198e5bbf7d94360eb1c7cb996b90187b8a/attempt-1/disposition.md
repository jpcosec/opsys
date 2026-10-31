# Executor comparison — WS18, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: declarar en spec2viz proyecciones de grafo reutilizables —ViewDoc y su NotationDoc— para selecciones y notación ya soportadas. Resultado: una Vista portable, sin código específico del host, que renderiza sobre un store real la selección declarada, coincide con ella y documenta qué selecciona. Repo dueño: spec2viz (`output_base: spec2viz:repository_root/`; rutas concretas las confirma su dueño al promover). Límites: no crear UI pages declarativas ficticias ni inventar selección; si el catálogo WS09 no fija selección mínima, detener promoción y corregir ese contrato antes de elegir una. Depende de WS09 y WS11; requiere G_SPEC_VIEW, pendiente e intencional. Deskops no escribe en spec2viz.

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
