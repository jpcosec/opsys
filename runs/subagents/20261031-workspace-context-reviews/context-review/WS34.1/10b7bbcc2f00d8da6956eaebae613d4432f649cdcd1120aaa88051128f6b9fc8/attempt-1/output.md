REFORMULACION
Propósito: fijar un encargo de planificación para un adaptador público restringido de dispatch Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: implementación en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, más `tests/`; dispatch correlacionado con el id de intento local WS32.1 y registros WS32.2; `confirmed` solo con respuesta observada del Hub. Repo dueño: `deskops`. Límites: no shell arbitrario, no duplicar transporte, no convertir la ausencia de confirmación en éxito/fallo remoto no observado. Este revisor no ejecuta nada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: `dag.yaml`, guía, brief, alcance, decisiones y cobertura; contrato WS12/`G_WRITE_CONTRACT`; salidas de WS33; ids/registros WS32.1–WS32.2; autorización `G_EXEC`; probe `G_SCION`/WS44. Cambios previstos: solo en `output_scope`, con adaptador y pruebas, sin tocar transporte ni shell. Dependencias: WS33 y WS12; gates `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT`; WS32.1/2 por vía transitiva. Validaciones futuras: gates pasan; agente real demuestra dispatch aceptado y uno rechazado o timeout; correlación con intento/registros; `confirmed` solo con respuesta Hub observada; ausencia no se interpreta; no shell arbitrario ni transporte duplicado; contrato por delta.

FUTURO
WS12 produce el contrato de operaciones y `G_WRITE_CONTRACT` del delta; WS44/operador produce `G_SCION`; humano/designee emite `G_EXEC` con agente/proyecto/acciones/alcance/sesión; WS32.1/WS32.2 y WS33 aportan identidad y registros; el TaskDoc de promoción fija archivos, pruebas y pills; WS34.2 cubre reply.
