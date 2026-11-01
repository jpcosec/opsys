## REFORMULACION

WS19.2 es un encargo de implementación en `graph_ui` para permitir alta y baja de relaciones **solo si el contrato WS12 las autoriza**, usando API real y la precondición de escritura que ese contrato fije. El resultado esperado es persistencia verificable tras recargar y rechazo visible de relaciones no permitidas o revisiones obsoletas. Límites: no crear semántica de relaciones en el componente; trabajar en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados y `tests/`; no duplicar el ticket `editing`. Depende de WS12 y de los gates G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT. La promoción no está autorizada.

## AMBIGUEDADES

Ninguna. Lo que falta —relaciones permitidas, endpoints, representación de la precondición y manejo de revisión obsoleta— lo produce WS12, nombrado en el nodo; su ausencia activa la regla común de detenerse y registrar el hueco. Los textos exactos de error y los archivos concretos corresponden a la promoción/TaskDoc.

## DRY-RUN

Un ejecutor futuro leería el nodo, WS12 (`contratos/operaciones.md`), el ticket `editing`, la base de workspace y las pruebas existentes. Cambiaría la UI de relaciones en `views/workspace/relations/` para invocar únicamente endpoints autorizados por WS12, añadiendo alta/baja y presentación de rechazos; no añadiría validaciones semánticas propias. Consumiría la precondición fijada por WS12 y verificaría antes G_PAYLOAD_PRECONDITION; para desarrollo/pruebas aisladas de API podría avanzar con contratos técnicos, pero el uso de mutaciones en UI exigiría G_HUMAN_READ. G_WRITE_CONTRACT y G_UI_WRITE se evaluarían por delta. Si WS12 no define endpoint, relación permitida o precondición, se detendría y registraría el hueco, sin inventar sustituto. Validaría con store temporal real o corpus WS40: alta y baja persisten tras recargar; relación no permitida y revisión obsoleta producen error visible y no modifican datos. Evitaría ejecución paralela con `editing`.

## FUTURO

WS12 publica el contrato y satisface G_WRITE_CONTRACT por delta. WS45 verifica G_PAYLOAD_PRECONDITION. WS16 produce G_HUMAN_READ. El receptor P01 emite el acta G_UI_WRITE del delta concreto. La promoción decide ticket receptor, archivos, pills y evidencias; WS19 solo cierra cuando cumplen sus hijos.
