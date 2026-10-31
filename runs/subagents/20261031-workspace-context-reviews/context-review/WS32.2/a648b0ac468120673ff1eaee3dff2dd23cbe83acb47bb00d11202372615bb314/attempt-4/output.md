REFORMULACION
- **Propósito:** hacer idempotentes manifiesto, RunDoc y cierre sobre el intento correcto, sin segundo pipeline.
- **Resultado:** una finalización repetida del mismo id de intento conserva identidad y evidencia sin crear registros nuevos.
- **Repo:** deskops; salidas previstas en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
- **Límites:** no sustituye el ticket Scion ni crea pipeline paralelo; promoción no autorizada; no incluye UI ni otros repos; exige gates.

AMBIGUEDADES
1. «sobre el intento correcto»: no se define cómo elegir ese intento entre varios del mismo agente o tras un dispatch fallido. Obliga a inventar la regla de selección y su efecto sobre el cierre.
2. «según el ticket de external_references.scion»: el ticket no se transcribe en el input y sería la única definición de manifiesto y registros de closeout. Obliga a inventar campos, formato y qué significa «materializa RunDoc».
3. «Manifiesto, RunDoc y cierre consistentes» frente a «Una finalización repetida... conserva identidad y evidencia sin crear registros nuevos»: la aceptación solo cubre idempotencia, no la consistencia entre los tres. Obliga a inventar cómo se comprueba esa consistencia.

DRY-RUN
- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS32.2, contratos vecinos WS05/WS12/WS32.1 y gates; el ticket Scion no está transcrito.
- **Cambios previstos:** `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`.
- **Dependencias:** WS05, WS12 y WS32.1; G_CLOSEOUT `blocked`, G_SCION `unverified`, G_WRITE_CONTRACT `pending`.
- **Validaciones futuras:** prueba de finalización repetida sobre el mismo id; identidad y evidencia conservadas; ausencia de registros nuevos; preflight task-only; resolución previa de gates. Sin ejecución.

FUTURO
WS32.1 aporta la separación intento/dispatch; WS12, la whitelist de escritura; WS44, el probe de G_SCION; el resolutor externo, G_CLOSEOUT; WS07 designa actores. El TaskDoc de promoción fijará archivos, pruebas y evidencias; la autorización de promoción corresponde a un humano. No son ambigüedades de este nodo.
