## REFORMULACION

WS19 es un nodo agregado, no ejecutable, del plan workspace-documental. Propósito: integrar en graph_ui la edición de campos y relaciones permitidas sobre el workspace ya integrado (a1b2b22), con precondición de escritura y conflicto visible. Resultado: se cumple cuando WS19.1 (campos con conflicto visible) y WS19.2 (relaciones permitidas) cumplen su aceptación; el agregado no produce artefactos propios. Repo dueño: graph_ui. Límites: no edita workflow-protected fields; no crea semántica de relaciones en el componente; usa API real y la precondición que fije WS12 (verificada por WS45); G_HUMAN_READ solo habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas de API; no duplica el ticket de edición (`never_parallel_duplicate`); promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Nodo agregado: no hay ejecución propia ni archivos que toque. Un ejecutor futuro recorrería sus hijos según `dag.yaml`: WS19.1 y WS19.2 dependen ambos de WS12 y no tienen arista entre sí; pueden consumir el mismo contrato WS12, pero no se transfieren nada. WS19.1 escribiría en `frontends/mindmap/views/workspace/fields/` y tests, consumiendo endpoints de WS12 y la precondición de payload (WS45), con gate G_HUMAN_READ antes de habilitar mutaciones UI, G_UI_WRITE por delta y G_WRITE_CONTRACT. WS19.2 haría lo propio en `relations/`, con alta/baja y rechazo visible. Integración conjunta: ambos deltas deben convivir sobre el mismo workspace y ticket de edición, sin ejecución paralela; si un contrato, endpoint o precondición falta, se detiene y registra el hueco con repo dueño, sin sustituto. Validación conjunta: aceptación de ambos hijos (persistencia tras recarga, texto local conservado en conflicto, rechazo de relación no permitida u obsoleta) y recibos por delta; el agregado no añade prueba propia.

## FUTURO

WS12 fija la representación de la precondición y operaciones; WS45 verifica la precondición de payload; WS16 produce el acta G_HUMAN_READ; el receptor P01 emite actas G_UI_WRITE por delta. La promoción y el TaskDoc corresponden a otro nodo o a una decisión humana.
