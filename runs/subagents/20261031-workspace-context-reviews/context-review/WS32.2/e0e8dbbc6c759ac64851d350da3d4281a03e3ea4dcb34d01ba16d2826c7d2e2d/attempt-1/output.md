## REFORMULACION
Propósito: hacer idempotentes el manifiesto por intento, el RunDoc y el cierre de Scion, usando siempre el id de intento citado por el cierre, nunca agente o slug. Resultado: manifiesto canónico que materializa RunDoc y registros de closeout con los campos mínimos indicados; una finalización repetida no crea registros nuevos y mantiene identidad, evidencia, id de intento y hash de sesión coincidentes. Repo dueño: `deskops`, con salidas en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`. Límites: no crear un segundo pipeline, no editar fuera de esos archivos, no ejecutar promoción (`not_authorized`) y respetar los gates y contratos de WS05, WS12, WS32.1, G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «hash de sesión» aparece como campo mínimo y criterio de coincidencia en la aceptación, pero no se define en el input cómo obtenerlo, calcularlo ni compararlo. El ejecutor tendría que inventar su fuente y semántica de igualdad; si depende de Scion, debería indicarlo un contrato o el inventario de WS05.
2. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos» no fija qué ocurre si la repetición trae evidencia o hash distintos: conservar, rechazar o diagnosticar. El ejecutor tendría que inventar la política de conflicto.

## DRY-RUN
Lecturas previstas: `task-ws32-2.md`, ticket `external_references.scion`, inventario WS05, contrato WS12, evidencias de G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT y código/tests de `runtime/scion.py`, `models/run.py`, `services/closure.py`. Cambios previstos: registro idempotente por id de intento, materialización de RunDoc, closeout sin duplicados y pruebas en `tests/`. Dependencias: WS05, WS12 y WS32.1; gates externos bloqueantes. Validaciones futuras: repetir finalización con el mismo id; comprobar ausencia de registros nuevos y coincidencia de id, hash y evidencia; verificar dos intentos del mismo agente y un dispatch fallido.

## FUTURO
WS05/WS44 aportan API e identidad de sesión; WS12 y G_CLOSEOUT definen evidencia y operaciones; WS07/P01 designa actores; la promoción fija archivos, pruebas y TaskDoc. Nada de esto se ejecuta aquí.
