## REFORMULACION
**Propósito:** refinar el ticket `external_references.scion` para que la identidad de intento no se confunda con slug y para separar los hechos `dispatch intent` (intención registrada) y `confirmed` (Scion aceptó) del `RunDoc`, sin crear un segundo pipeline.
**Resultado:** código y pruebas en `deskops` que demuestren identidades distintas para dos intentos del mismo agente y para un dispatch fallido, con cambios de `RunDoc` por el flujo de modelos SLDB.
**Repo:** `deskops`, con `output_scope` en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
**Límites:** depende de WS05 y WS12; exige G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; promoción no autorizada; no duplicar el ticket ni el pipeline existente.

## AMBIGUEDADES
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc»: no se define dónde se registra cada hecho ni qué evento exacto constituye «Scion aceptó». El ejecutor tendría que inventar el modelo de estados.
2. «cambios de RunDoc por el flujo de modelos SLDB»: el input no describe ese flujo ni su autoridad; obligaría a inventar el canal y el criterio de comprobación.
3. «un dispatch fallido conservan identidades distintas»: no se delimita qué fallos cubre (rechazo, timeout, error de transporte) ni cómo se evidencia la identidad distinta. Obligaría a inventar el criterio de aceptación.

## DRY-RUN
**Lecturas previstas:** nodo y aristas de `dag.yaml`; ticket `external_references.scion`; `auditoria/scion.md` de WS05; `contratos/operaciones.md` de WS12; `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/` en `deskops`.
**Cambios previstos:** refinamiento del ticket y ajustes en los archivos de `output_scope`, con pruebas de identidad de intento y dispatch.
**Dependencias:** WS05 y WS12; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.
**Validaciones futuras:** dos intentos del mismo agente con identidades distintas; dispatch fallido sin colisión; `RunDoc` modificado por el flujo SLDB. Sin ejecución.

## FUTURO
WS32.2 consume la separación para idempotencia de manifiesto y cierre; WS33/34/36 y WS37 dependen de esta base. WS44 produce G_SCION y WS12 produce G_WRITE_CONTRACT. El humano resuelve P01/P03–P06; WS07 designa al operador Scion. La promoción exige preflight task-only y fijación de archivos, pills y evidencia en el TaskDoc.
