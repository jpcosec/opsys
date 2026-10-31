REFORMULACION
- **Propósito:** revisar WS19.1 como encargo de planificación: edición de campos en el workspace, no implementación.
- **Resultado:** delta en graph_ui que edita campos consumiendo endpoints del contrato WS12 sin modificarlo, con revisión CAS y conflicto visible; campos workflow-protected fuera de este canal; mutación limitada a desk en modo manual exclusivo.
- **Repo:** `graph_ui` (`frontends/mindmap/views/workspace/fields/`, `tests/`).
- **Límites:** no ejecutar, no promover, no cambiar contratos ni revisar los bloques edge vecinos; gates pendientes son intencionales.

AMBIGUEDADES
1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.» No se define qué es «modo manual exclusivo», qué son «otros modos» ni qué «contrato» los habilita. P03 indica que «lock solo UI no basta» y exige canal público con autoridad compartida. El ejecutor tendría que inventar cómo detectar el modo, si basta un lock de UI y cuándo se libera el read-only, con riesgo de restricción insuficiente o excesiva.

DRY-RUN
- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.1 y gates.
- **Cambios previstos:** ninguno en esta revisión; si se promueve, archivos en `fields/` y `tests/`, consumo de endpoints WS12, sin cambios de contrato.
- **Dependencias:** WS12 (contrato, whitelist, endpoints), G_WRITE_CONTRACT, G_UI_WRITE por delta, G_HUMAN_READ y agregado WS19; WS11/WS08 y WS02–WS10 de forma transitiva.
- **Validaciones futuras:** guardar/recargar; escritura obsoleta conserva texto local y muestra conflicto; protegidos no editables; read-only en otros modos; no duplicar `editing`; TaskDoc y preflight.

FUTURO
WS12 publica contrato, whitelist y disponibilidad de endpoints; WS16 produce el acta de G_HUMAN_READ; el receptor P01 produce el acta por delta de G_UI_WRITE; WS06/WS19 promueven y fijan TaskDoc; el humano acepta; WS20/G_SOURCE cubre raw-source.
