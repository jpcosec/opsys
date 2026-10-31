## REFORMULACION
- **Propósito:** declarar proyecciones de grafo reutilizables mediante ViewDoc/NotationDoc para selecciones y notación ya soportadas.
- **Resultado:** una vista portable evaluada sobre store real y documentación de qué selecciona; tareas receptoras promovidas por el dueño de spec2viz.
- **Repo:** `spec2viz`, con `output_scope: sldb/views/ (nombres confirmados por contrato); tests/`.
- **Límites:** no crear UI pages declarativas ficticias; no modificar spec2viz desde este plan; depende de WS09/WS11 y requiere G_SPEC_VIEW; `promotion: not_authorized`.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas:** nodo WS18, contratos vecinos WS09/WS11, G_SPEC_VIEW, guía, brief, alcance y decisiones; `task_file` al promoverse.
- **Cambios previstos:** solo declaración/propuesta de ViewDoc/NotationDoc y tests; nombres exactos según contrato. Sin edición real.
- **Dependencias:** catálogo WS09, contrato WS11, acta G_SPEC_VIEW y dueño de spec2viz designado.
- **Validaciones futuras:** nombres confirmados por contrato; vista portable sobre store real; selección documentada; sin UI ficticia; sin modificación desde este plan; preflight y evidencia task-only.

## FUTURO
WS11 produce G_SPEC_VIEW; el solicitante/P01 designa al responsable de spec2viz; ese dueño promueve las tareas receptoras. WS24 consume WS18. La evaluación sobre store real y la promoción ocurren fuera de esta revisión, sin ejecución aquí.
