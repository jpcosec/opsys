## REFORMULACION
**Propósito:** definir un adaptador público restringido para publicar una respuesta (`reply`) vinculada al intento correcto, con timeout/errores y autoridad del coordinador.
**Resultado:** implementación en `runtime/`; `cli/commands/runtime.py` o API definida; pruebas. Aceptación: `G_SCION`/`G_EXEC` pasan y un agente real demuestra respuesta vinculada al intento correcto.
**Repo:** `deskops`.
**Límites:** nodo candidato, no ejecutable; no enviar mensajes durante la planificación; promoción `not_authorized`; depende de WS33, WS12 y WS34.1; requiere `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT`.

## AMBIGUEDADES
1. «con timeout/errores» frente a «agente real demuestra respuesta vinculada al intento correcto». La aceptación solo exige demostrar el caso exitoso; no fija comportamiento observable para timeout ni para errores. El ejecutor tendría que inventar el umbral de timeout, qué errores cubrir y cuándo considerarlos aceptados.

No encuentro otras: el repo está identificado, el resultado está acotado, las dependencias y gates están nombrados, y los contratos externos tienen productores designados.

## DRY-RUN
**Lecturas previstas:** nodo WS34.2, guía, `dag.yaml` (vecinos WS33, WS12, WS34.1 y gates), `decisiones.md` y `alcance.md`.
**Cambios previstos:** adaptador de reply y pruebas en `deskops`, sin emitir mensajes reales en planificación.
**Dependencias:** WS33 aporta vinculación mensaje/intento; WS12, autoridad y canal; WS34.1, dispatch previo; gates humanos/técnicos pendientes.
**Validaciones futuras:** probe `G_SCION`, autorización `G_EXEC`, contrato `G_WRITE_CONTRACT` y prueba con agente real. No se ejecuta nada.

## FUTURO
WS44 produce la evidencia de `G_SCION`; WS12 produce `G_WRITE_CONTRACT`; el humano resuelve `G_EXEC`. WS33 y WS34.1 aportan vinculación y dispatch. La promoción fijará archivos, escenarios y evidencia dentro de la aceptación.
