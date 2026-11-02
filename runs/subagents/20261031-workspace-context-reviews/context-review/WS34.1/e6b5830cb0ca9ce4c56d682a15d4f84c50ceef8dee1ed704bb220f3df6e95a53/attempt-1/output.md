REFORMULACION

El nodo WS34.1 encarga, en el repo `deskops`, un adaptador público restringido para dispatch: confirmación, identidad de intento, timeout/errores y autoridad del coordinador. El resultado esperado es código en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, más pruebas. Límites: no shell arbitrario, no duplicar transporte, no fijar un umbral propio de timeout y no despachar durante planificación. Solo avanza con `G_EXEC`, `G_SCION` y el contrato por delta de WS12 verificado en `G_WRITE_CONTRACT`.

AMBIGUEDADES

Ninguna. La política de timeout ausente tiene productor nombrado (WS12) y conducta definida (detenerse y registrar el hueco); WS32.1/WS32.2 son artefactos de intento nombrados y alcanzables transitivamente por WS33→WS32. La elección entre `runtime/`, `cli/commands/runtime.py` o la API de WS12 queda delegada a ese contrato, y su ausencia activa la regla común de detención.

DRY-RUN

Un ejecutor futuro leería `dag.yaml` (WS34.1, WS33, WS12, gates), el contrato WS12 del delta, la salida de WS33/WS32.1/WS32.2 y la evidencia de `G_SCION`/`G_EXEC`. Verificaría que `G_WRITE_CONTRACT` contiene la política de timeout y la clasificación aceptado/rechazado/vencido. Si falta, se detiene y registra el hueco con repo dueño; no elige umbral.

Cambios previstos: implementar el adaptador en `runtime/` y el punto de entrada en `cli/commands/runtime.py` o la API fijada; añadir pruebas en `tests/`. No habría nuevas dependencias, transporte alternativo ni shell.

Validación esperada: un agente real obtiene un dispatch aceptado y otro rechazado o vencido; ambos se correlacionan con el id de intento previo WS32.1 y los registros WS32.2. Solo una respuesta observada del Hub cuenta como `confirmed`; la ausencia de confirmación no se convierte en éxito ni en fallo remoto no observado.

FUTURO

WS12 produce la sección de contrato y timeout por delta; WS44 produce `G_SCION`; un humano externo resuelve `G_EXEC`; WS34.2 consume el adaptador y añade reply. Nada de eso lo decide este nodo.
