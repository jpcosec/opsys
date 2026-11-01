## REFORMULACION
**Propósito:** planificar en graph_ui el alta y baja de relaciones permitidas por el contrato WS12, usando la API real y la precondición de escritura que ese contrato fije, sin definir semántica de relaciones en el componente.
**Resultado:** un delta implementable y comprobable donde las relaciones autorizadas persisten tras recargar y las no permitidas o con revisión obsoleta se rechazan con error visible.
**Repo:** graph_ui, con salidas previstas bajo `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.
**Límites:** depende de WS12; exige G_WRITE_CONTRACT, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_HUMAN_READ para habilitar mutaciones en UI; no crea semántica propia ni duplica el ticket de edición; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

Las referencias a «relaciones permitidas por contrato», «endpoints autorizados por el contrato WS12» y «la precondición de escritura que fije WS12» tienen productor nombrado y regla de faltante en alcance.md. G_HUMAN_READ queda acotado por el propio nodo: no bloquea desarrollo ni pruebas aisladas de API. «Confirmadas tras recargar» y «error visible» son criterios comprobables cuyo detalle fija el TaskDoc de promoción.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12, sus operaciones y precondición, el ticket receptor vigente y la aceptación de este nodo. Cambiaría únicamente archivos de relaciones bajo el output_scope y pruebas asociadas; no tocaría semántica de relaciones fuera del componente.

Consumiría G_WRITE_CONTRACT mediante el recibo por delta de WS12; G_PAYLOAD_PRECONDITION desde WS45; G_UI_WRITE mediante acta del receptor P01 para este delta; G_HUMAN_READ solo antes de habilitar mutaciones de UI. Si falta el contrato, endpoint o precondición, se detendría registrando hueco y repo dueño, sin sustituto.

Casos de error previstos: relación no permitida rechazada con error visible; precondición obsoleta rechazada sin cambios; API ausente deja la operación no disponible. Validación esperada: alta y baja persisten y se confirman tras recargar; rechazos son observables; pruebas con store temporal real y contrato WS12 vigente. No se ejecuta nada.

## FUTURO
WS12 publica el contrato y su representación de precondición; WS45 verifica G_PAYLOAD_PRECONDITION; el receptor P01 emite el acta G_UI_WRITE por este delta; WS16 produce G_HUMAN_READ; la promoción fija TaskDoc, archivos, pruebas y textos.
