## REFORMULACION
**Propósito:** declarar proyecciones de grafo reutilizables —ViewDoc y NotationDoc— para selecciones y notación ya soportadas por spec2viz.

**Resultado:** ViewDoc/NotationDoc concretos en spec2viz (`sldb/views/` y `tests/`, con ruta y registro que fije la promoción) y su comprobación con `evaluate_view` y `/api/views` de graph_ui sobre un store real.

**Repo dueño:** spec2viz; deskops solo registra enlaces, no escribe allí.

**Límites:** no portabilidad genérica, servicio/CLI/runtime fuera de graph_ui, extracción o compartición del evaluador, ni UI pages declarativas ficticias. No inventar selección: si WS09 no fija selección mínima, detener la promoción y corregir el contrato. Depende de WS09/WS11; G_SPEC_VIEW queda pendiente y es per_delta.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas:** catálogo WS09, contrato WS11, filas C-37/C-49 de `reconciliacion.md`, `evaluate_view`, `resolve_documents`, rutas `/api/views` y un store real.

**Cambios previstos:** crear los ViewDoc y NotationDoc y sus pruebas en spec2viz; no modificar graph_ui ni el evaluador.

**Dependencias y gates:** WS09/WS11 deben aportar selección y notación; G_SPEC_VIEW debe recibirse por delta antes de promover/ejecutar la tarea receptora.

**Errores:** si falta selección mínima, detenerse y corregir WS09; si falta contrato, API o dato, registrar el hueco con repo dueño y no crear sustituto; si falla la evaluación, ajustar ViewDoc/NotationDoc, no el evaluador.

**Validación esperada:** tests sobre store real; selección idéntica a WS09/WS11 y notación resuelta por `resolve_documents`; no alegar que dos stores prueban el mismo payload completo.

## FUTURO
El acta G_SPEC_VIEW la produce el receptor P01 en spec2viz. La promoción, TaskDoc y ejecución corresponden al supervisor/Executor de spec2viz. Una posible corrección de WS09/WS11 si falta selección y la aceptación del delta son decisiones externas a este nodo.
