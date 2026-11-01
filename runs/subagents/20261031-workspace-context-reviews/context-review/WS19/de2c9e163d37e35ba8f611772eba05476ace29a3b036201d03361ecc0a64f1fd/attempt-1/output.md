REFORMULACION
WS19 es un agregado no ejecutable de graph_ui para integrar edición de campos y relaciones sobre el workspace a1b2b22, reutilizando editores/API y una precondición de escritura fijada por WS12. Resultado: las salidas de WS19.1 y WS19.2; WS19 termina cuando ambos hijos cumplen su aceptación. Límites: no crear semántica de relaciones en el componente, no editar campos protegidos por workflow, no duplicar el ticket de edición ni ejecutar en paralelo, y consumir solo endpoints/precondición del contrato WS12. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES
Ninguna.

DRY-RUN
WS19 no se ejecuta ni modifica archivos: es un agregado. Un ejecutor futuro leería `dag.yaml`, comprobaría WS12 y esperaría el cierre de WS19.1 y WS19.2. WS19.1 produciría edición de campos con conflicto visible, conservando texto local ante escritura obsoleta; WS19.2 produciría alta/baja de relaciones permitidas y rechazo visible de relación no permitida o revisión obsoleta. Ambos consumen WS12; WS19.1 exige además la precondición verificada por WS45. G_HUMAN_READ solo habilita uso de mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta. Si falta contrato, precondición o recibo, se detiene y registra el hueco con repo dueño, sin sustituto. La validación conjunta es la evidencia de aceptación de ambos hijos: guardar/recargar confirma el dato, el conflicto se muestra y no pierde texto local; las relaciones persisten y las inválidas se rechazan. WS19 no añade producto propio: transfiere esas dos capacidades conjuntas a WS21 y WS42, que no deberían consumirlas antes del cierre de ambos hijos.

FUTURO
WS12 produce contrato, representación de precondición y whitelist; WS45 verifica G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 en graph_ui produce G_UI_WRITE por delta; WS12 produce G_WRITE_CONTRACT por delta. WS19.1/WS19.2 y después WS21/WS42 completan o consumen el resultado. La promoción del TaskDoc y sus archivos exactos quedan fuera de esta revisión.
