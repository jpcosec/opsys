## REFORMULACION
- **Propósito:** declarar ViewDoc y NotationDoc concretos para selecciones y notación ya soportadas por spec2viz, reutilizando `evaluate_view` y `/api/views` de graph_ui; no crear UI ni evaluador nuevos.
- **Resultado:** ViewDoc/NotationDoc en `spec2viz/sldb/views/` y pruebas que demuestren evaluación sobre store real y que la selección coincide con WS09/WS11.
- **Repo:** spec2viz; pruebas en `tests/`.
- **Límites:** sin portabilidad genérica, servicio/CLI/runtime fuera de graph_ui, extracción del evaluador ni páginas UI ficticias; no inventar selección. Deskops no escribe en spec2viz. `G_SPEC_VIEW` es per_delta.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas:** catálogo WS09, contrato WS11, filas C-37/C-49 de `reconciliacion.md`, código existente de `evaluate_view`, `resolve_documents` y rutas `/api/views`; capacidades WS03 si hace falta contrastar.
- **Cambios previstos:** futura TaskDoc en spec2viz; ViewDoc/NotationDoc concretos en `sldb/views/` y pruebas. Nada se ejecuta ahora.
- **Dependencias:** WS09 y WS11 como fuentes de selección/notación; `G_SPEC_VIEW` pendiente por delta; store real para validar.
- **Validaciones futuras:** evaluar los documentos con el camino existente de graph_ui sobre store real; comparar selección con WS09/WS11; comprobar que el ViewDoc documenta qué selecciona; no atribuir a dos stores el mismo payload completo; preflight de promoción de solo tarea.

## FUTURO
WS09 debe fijar la selección mínima y WS11 aportar el contrato; si falta, se detiene la promoción y se corrige el contrato antes de elegir. P01/receptor del repo emite el acta `G_SPEC_VIEW` por delta con commit/blob verificable. El supervisor/Executor de spec2viz promueve y ejecuta la TaskDoc futura; el store real proviene de la prueba o del corpus aplicable.
