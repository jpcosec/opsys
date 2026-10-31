## REFORMULACION
**Propósito:** que el workspace muestre errores de lectura y modo degradado en el panel afectado, sin borrar historial ni fingir vacío. **Resultado:** implementación o delta en `graph_ui` que distingue errores según la respuesta de la API (contrato WS11), informa límites reales, hace visible el fallo CDN y permite reintento manual recuperando conexión sin perder pestañas, foco ni historia; incluye tests. **Repo:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/errors/`, rutas de lectura del contrato WS11 y `tests/`. **Límites:** solo lectura; empaquetado offline fuera; no se autoriza promoción; integración como delta o ticket existente, sin duplicado paralelo.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas:** nodo WS15.1 y gates en `dag.yaml`; guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `reconciliacion.md`. Los bloques edge no se revisan.

**Cambios previstos:** ninguno en esta revisión; no se ejecuta ni promueve. Si se promoviera, el TaskDoc fijaría archivos, escenarios y textos dentro de la aceptación.

**Dependencias:** WS13 (agregado cuyos hijos WS13.1–13.3 entregan lector, historia y foco); WS11 de forma transitiva aporta contrato de lectura y `G_UI_READ`, actualmente pendiente. La regla común de alcance cubre la ausencia de contrato: detenerse y registrar el hueco.

**Validaciones futuras:** tests de distinción de errores por respuesta API; test de fallo CDN; comprobación de reintento manual preservando pestañas, foco e historia; lectura de Markdown cuando el soporte lo permita; validación humana de WS16 sobre el corpus WS40.

## FUTURO
WS11 produce el contrato de lectura y resuelve `G_UI_READ`; WS07 designa al responsable de `graph_ui`; WS13 entrega las capacidades de lector, historia y foco de las que depende este nodo; la promoción fija archivos, pills, átomos y evidencia; WS16 valida el recorrido humano. La decisión sobre `source_mode` (P04) y la aceptación de gates corresponden a actores humanos, no a este revisor. Nada de ello obliga a inventar dentro de WS15.1.
