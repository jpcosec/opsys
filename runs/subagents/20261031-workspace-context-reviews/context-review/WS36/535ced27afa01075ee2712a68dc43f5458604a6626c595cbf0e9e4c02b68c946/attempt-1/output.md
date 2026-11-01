## REFORMULACION
WS36 es un nodo de implementación (delivery) en **graph_ui**: integrar en la vista de ejecución la delegación e intervención humanas invocando **solo** el adaptador público WS34 para dispatch/reply y usando la operación de decisión de WS33.2. Resultado: acciones UI y tests que vinculan la respuesta al intento, confirman la operación y muestran como error la ausencia de API o permisos, con actor humano y evidencia enlazada de WS33.1/WS33.2; sin autoaprobación ni simulación. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/execution/`, con ruta fina al adaptador autorizada por WS12, y `tests/`. Límites: no implementa el adaptador, modelos Scion/deskops ni permisos; depende de WS34 y WS35 y consume G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT por delta.

## AMBIGUEDADES
ninguna

## DRY-RUN
Nodo no agregado. Un ejecutor leería el contrato del adaptador WS34, las vistas/componentes de WS35, el contrato WS12, la operación/esquema de WS33.2 y la evidencia de WS33.1, además de los recibos de gates. Cambios previstos: handlers/acciones de dispatch y reply contra WS34; llamada de registro de decisión a WS33.2; presentación de respuesta ligada al intento, actor/evidencia y estados de error; tests. Dependencias: WS34 aporta API y confirmación; WS35, lectura/trazabilidad; WS33.1/WS33.2, evidencia y decisión; WS12, canal/efectos. G_EXEC autoriza el escenario y comunicaciones; G_SCION se comprueba por WS44; G_UI_WRITE exige recibo del delta; G_WRITE_CONTRACT, prueba del contrato. Si falta contrato, API o permiso: detener, registrar el hueco con repo dueño y no crear sustituto. Validación esperada: tests de respuesta vinculada al intento, decisión con actor humano y evidencia enlazada, error visible por ausencia de API/permisos y ausencia de autoaprobación/simulación.

## FUTURO
WS37 validará UF06 con agente real y acta; WS44/operador producirá G_SCION; el receptor P01 emitirá G_UI_WRITE por delta; WS12 fijará G_WRITE_CONTRACT; el solicitante autorizará G_EXEC. La aceptación humana y las autorizaciones se deciden fuera de este nodo.
