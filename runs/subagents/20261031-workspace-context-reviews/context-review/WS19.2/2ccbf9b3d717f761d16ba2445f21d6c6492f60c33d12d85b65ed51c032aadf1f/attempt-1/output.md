## REFORMULACION
WS19.2 es un nodo de implementación en `graph_ui` que debe habilitar el alta y la baja de relaciones permitidas por el contrato WS12 sobre el workspace integrado, usando API real y la precondición de escritura que fije WS12. Resultado: relaciones persistidas y confirmadas tras recargar; rechazo visible de relación no permitida, protegida o con revisión obsoleta. Límites: no crear semántica de relaciones en el componente; no habilitar la baja de `RelationDoc` si el modo solo destrackea —debe declararse—; quitar una referencia de campo es otra operación; no duplicar en paralelo el ticket `editing`; `G_HUMAN_READ` solo habilita el uso de mutaciones en UI, no el desarrollo ni las pruebas aisladas de API.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas: `dag.yaml`, contrato WS12, salidas y aceptación de WS47/WS48, estado de `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT` y `G_HUMAN_READ`, ticket `editing` y `reconciliacion.md`; código existente en `frontends/mindmap/views/workspace/`.

Cambios previstos: extender el ticket/delta de edición en serie, sin duplicarlo; implementar alta y baja en `views/workspace/relations/` y `tests/`, consumiendo endpoints autorizados por WS12 y su precondición; usar la admisión de WS48 y la guarda de WS47; mostrar confirmación tras recarga y error visible ante rechazo.

Dependencias y gates: WS12 aporta whitelist, operaciones, efectos y representación de precondición; WS45/G_PAYLOAD_PRECONDITION debe verificarla antes de habilitar escritura; WS47 impide editar documentos con contenido no declarado hasta que sus pruebas pasen; WS48 debe admitir la escritura; G_UI_WRITE y G_WRITE_CONTRACT se consumen por delta; G_HUMAN_READ se exige antes de habilitar mutaciones en UI.

Errores: si falta contrato, guarda, admisión, precondición o recibo, detenerse y registrar el hueco con repo dueño, sin sustituto; rechazar relación no permitida o protegida y revisión obsoleta con error visible; si el modo no borra `RelationDoc` ni su índice, no habilitar la baja y declararlo.

Validación esperada: pruebas con store temporal real; alta/baja persisten tras recargar; rechazos visibles; baja borra documento e índice por canal público; referencia de campo se prueba aparte; no se duplica el ticket existente.

## FUTURO
WS12 fija el contrato y la precondición; WS45 produce la evidencia de `G_PAYLOAD_PRECONDITION`; WS47 y WS48 producen sus deltas; el receptor P01 emite acta por delta para `G_UI_WRITE`; WS16 aporta `G_HUMAN_READ`; la promoción fija TaskDoc, archivos y textos.
