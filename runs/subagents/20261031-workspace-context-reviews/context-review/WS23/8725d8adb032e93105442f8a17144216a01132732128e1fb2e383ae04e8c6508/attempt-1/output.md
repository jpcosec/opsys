## REFORMULACION

**Propósito:** encargo de implementación en `graph_ui` para una vista de procedimiento que represente `RitualDoc`/`StepDoc`/lifecycle sobre referencias reales, en solo lectura.

**Resultado:** renderer en `frontends/mindmap/views/workspace/procedure/` y `tests/` que abre documentos y soporte, muestra transiciones declaradas del lifecycle y no permite avance ni mutaciones. El progreso de paso solo se muestra si WS02/WS09/WS11 identifican un campo/API real de deskops; si no, los pasos authored quedan inertes.

**Repo/límites:** repo dueño `graph_ui`; depende de WS13 y WS09; requiere `G_UI_READ` por delta. Pruebas con corpus WS40 o store temporal real. No escribe estado, no auto-marca pasos por lectura, no inventa progreso ni controles de avance.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** `dag.yaml` (WS23, WS13, WS09, gates), brief, alcance, decisiones, reconciliación; salidas de WS09/WS11 y acta `G_UI_READ`; corpus WS40 o store temporal.

**Cambios previstos:** módulo de procedimiento en `procedure/` y pruebas; vista read-only con navegación a documentos/soporte, transiciones origen/destino/condición y ausencia de peticiones de escritura.

**Dependencias:** WS13 como agregado completado; WS09 como inventario; WS11 transitivamente como contrato de navegación; datos de lifecycle desde deskops; acta de recepción por delta del receptor P01. Si falta contrato/API, aplica la regla común: detenerse y registrar el hueco.

**Validaciones futuras:** apertura de documentos/soporte; no auto-marcado por lectura; progreso solo con campo/API real; pasos inertes sin él; transiciones sin controles de avance; prueba de no peticiones de escritura.

## FUTURO

El TaskDoc de promoción fijará archivos, escenarios y textos. WS09/WS11 deben aportar la identificación del campo/API de progreso y el contrato de navegación. El receptor humano P01 emite el acta `G_UI_READ` por delta. WS40 puede aportar el corpus y WS30 la validación manual. WS06 integrará el delta en el ticket receptor sin duplicar implementación. Nada de esto autoriza ejecución todavía.
