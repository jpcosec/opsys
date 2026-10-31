## REFORMULACION
**Propósito:** que manifiesto, RunDoc y cierre de Scion sean consistentes e idempotentes sobre el intento correcto, identificado por el id citado en el cierre, nunca por agente o slug.
**Resultado:** un registro canónico por intento que materializa RunDoc y registros de closeout, con campos mínimos definidos en el ticket `external_references.scion`, y finalizaciones repetidas que no duplican registros ni pierden identidad/evidencia.
**Repo dueño:** `deskops`, limitado a `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
**Límites:** no es segundo pipeline; depende de WS05, WS12 y WS32.1; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT. No ejecuta ni promueve.

## AMBIGUEDADES
1. «hash de sesión» — no se define qué sesión ni cómo se calcula (¿id de sesión de la API Scion, del RunDoc, derivado localmente?). El ejecutor debe inventar el origen y la función de hash para cumplir la coincidencia triple.
2. «conserva identidad y evidencia sin crear registros nuevos» — no dice qué ocurre si una segunda finalización aporta evidencia distinta. Obliga a inventar política de conflicto (rechazar, preservar la primera, marcar discrepancia).
3. «Manifiesto = registro canónico por intento que materializa RunDoc y registros de closeout» — «materializa» no aclara soporte ni forma (archivo aparte, campo embebido, registro de almacenamiento). El ejecutor debe elegir un mecanismo no fijado por la aceptación.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (nodo, gates), `external_references.scion`, auditoría WS05, contrato WS12, ticket refinado WS32.1, plantilla RunDoc y tests existentes en `deskops`.
**Cambios previstos:** `runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`.
**Dependencias:** WS05 (inventario), WS12 (contrato de operaciones), WS32.1 (identidad intento/dispatch); gates G_CLOSEOUT bloqueado, G_SCION sin verificar, G_WRITE_CONTRACT pendiente.
**Validaciones futuras:** prueba de finalización repetida sobre el mismo id de intento; coincidencia de id/hash/evidencia entre manifiesto, RunDoc y closeout; dos intentos del mismo agente con ids propios; dispatch fallido conserva `confirmed` desconocido. El TaskDoc de promoción fijará archivos y escenarios exactos.

## FUTURO
- WS44 (operador designado en WS07) produce el probe y G_SCION.
- WS12 produce G_WRITE_CONTRACT.
- Resolver externo de G_CLOSEOUT estabiliza evidencia.
- WS32.1 refina el ticket de `external_references.scion`.
- La promoción (`not_authorized`) y el TaskDoc fijan archivos, pills y preflight.
- WS06/WS11/WS12 aportan la matriz y aceptación de alcance receptor.
