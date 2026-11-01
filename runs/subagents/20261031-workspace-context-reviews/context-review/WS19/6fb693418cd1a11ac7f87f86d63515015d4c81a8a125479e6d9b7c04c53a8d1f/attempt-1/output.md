## REFORMULACION
WS19 es un **agregado no ejecutable** de graph_ui: integra la edición de campos con conflicto visible y la edición de relaciones permitidas, reutilizando editores/API existentes y la precondición de escritura que fije WS12/verifique WS45. Su resultado es la suma de las salidas de WS19.1 y WS19.2; sus dependientes siguen dependiendo de WS19. Límites: no edita campos workflow-protected, no crea semántica de relaciones, no duplica el ticket `editing` ni ejecuta en paralelo, y la promoción no está autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Al ser agregado, no se ejecuta ni produce cambios propios. Un ejecutor futuro leería la aceptación de WS19.1 y WS19.2, el contrato WS12 aplicable a cada delta, la evidencia de WS45 para `G_PAYLOAD_PRECONDITION`, los recibos `G_WRITE_CONTRACT` por delta y `G_UI_WRITE` del receptor P01, y `G_HUMAN_READ` antes de habilitar mutaciones en UI. Comprobaría que WS19.1 aporta guardado/recarga real, rechazo de escritura obsoleta sin pérdida del texto local y conflicto visible; que WS19.2 aporta alta/baja persistente y rechazo visible de relación no permitida o revisión obsoleta. También verificaría que ninguno editó campos protegidos ni introdujo semántica de relaciones en el componente. Sin contrato, precondición o recibo aplicable, el hijo correspondiente se detiene y registra el hueco; no se sustituye. El agregado solo se valida cuando ambos hijos aceptan y sus dependencias no dejan huecos abiertos. No hay cambios de archivos en WS19; solo se registraría el cierre agregado.

## FUTURO
WS12 fija whitelist, representación de precondición y contrato por operación; WS45 produce `G_PAYLOAD_PRECONDITION`; WS16 produce `G_HUMAN_READ`; el receptor P01 emite `G_UI_WRITE` y los contratos por delta se comprueban. Otro nodo/humano decide la promoción, el TaskDoc y si el delta se integra en el ticket `editing` existente o en una tarea atómica, sin duplicar implementación. WS21 y WS42 consumen después el resultado.
