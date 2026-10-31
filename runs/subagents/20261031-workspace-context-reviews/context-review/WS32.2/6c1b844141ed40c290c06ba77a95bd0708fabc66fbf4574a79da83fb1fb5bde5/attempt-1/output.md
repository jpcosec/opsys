## REFORMULACION
**Propósito:** hacer idempotentes manifiesto, RunDoc y cierre sobre el intento correcto, identificado por id de intento, nunca por agente o slug.  
**Resultado:** registro canónico por intento y cierre consistente en id de intento, hash de sesión y evidencia, sin duplicados.  
**Repo:** `deskops` (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`).  
**Límites:** no inventar sesión/hash; si falta artefacto o contrato, registrar hueco con WS05/WS12 y bloquear; no segundo pipeline; no ejecutar; promoción no autorizada; gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT.

## AMBIGUEDADES
1. **Repetición con payload divergente.** Cita: «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos» y «manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia». No define si una segunda finalización con el mismo id pero distinto hash/evidencia/commit debe rechazarse como conflicto, devolver el registro existente como no-op o sobrescribir. Obligaría a inventar la política de idempotencia/conflicto y el resultado observable, que la aceptación no fija.

## DRY-RUN
- **Lecturas previstas:** nodo WS32.2 y aristas WS05/WS12/WS32.1; inventario WS05; contrato WS12; ticket `external_references.scion`; evidencia G_CLOSEOUT; código y tests actuales de `deskops`. Sin ejecutar.
- **Cambios previstos:** registro canónico por id de intento; manifiesto, RunDoc y closeout con hash de sesión/evidencia; pruebas de repetición y de dos intentos distintos.
- **Dependencias:** WS05, WS12, WS32.1; G_CLOSEOUT satisfecho; G_SCION no verificado; G_WRITE_CONTRACT pendiente `per_delta`.
- **Validaciones futuras:** repetir finalización del mismo id sin duplicar; dos intentos del mismo agente con identidades distintas; dispatch fallido distinguido; ausencia de artefacto/hash → hueco registrado; recibo `per_delta`.

## FUTURO
WS05 produce inventario de identidad/API; WS12 contrato de sesión/digest/registro; WS32.1 materializa registro e identidades; WS44 produce G_SCION; P01/humano acepta deltas por repo; WS06/promoción fija TaskDoc, archivos y pruebas exactas. No son ambigüedad.
