REFORMULACION
Propósito: refinar el ticket `external_references.scion` para que la identidad del intento no sea el slug y para separar `dispatch intent` (intención registrada por deskops) de `confirmed` (aceptación de la API pública de Scion). Resultado: ids de intento propios generados antes del dispatch; dos intentos del mismo agente y un dispatch fallido (rechazo o timeout) conservan identidades distintas; ambos hechos quedan en el registro por intento que WS32.2 convertirá en manifiesto canónico; RunDoc se modifica por el flujo SLDB, no ad hoc. Repo: deskops. Límites: sin segundo pipeline, sin edición ad hoc, con WS05/WS12 y gates pendientes; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: input completo (guía, brief, alcance, decisiones, cobertura, reconciliación, nodo y contratos vecinos/gates). Sin ejecutar tests ni contactar APIs.
Cambios previstos: generar/registrar id de intento y separar `dispatch intent`/`confirmed` en `runtime/scion.py`; registro por intento; ajustar `models/run.py`, `services/closure.py` y `tests/`; editar RunDoc vía CLI sldb.
Dependencias: WS05 (inventario), WS12 (contrato), WS32.2 (manifiesto), WS44/G_SCION, G_CLOSEOUT, G_WRITE_CONTRACT.
Validaciones futuras: dos intentos del mismo agente y dispatch fallido con ids distintos; `confirmed` solo con respuesta API; RunDoc por SLDB; gates y aceptación.

FUTURO
WS05 produce inventario; WS44 ejecuta probe y produce G_SCION; WS12 produce whitelist y G_WRITE_CONTRACT; WS32.2 hace manifiesto/cierre idempotente; WS07/humano designa actores y resuelve Pxx; la promoción fija TaskDoc, archivos y pruebas; G_CLOSEOUT aporta evidencia externa.
