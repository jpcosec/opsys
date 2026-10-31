## REFORMULACION

**Propósito:** planificar un adaptador público restringido para *dispatch* de Scion.

**Resultado:** dispatch con confirmación observable del Hub, identidad de intento, timeout/errores y autoridad del coordinador; sin shell arbitrario ni transporte duplicado.

**Repo:** `deskops` (`runtime/`, `cli/commands/runtime.py` o la API que fije WS12, `tests/`).

**Límites:** candidate, sin promoción autorizada; depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «timeout/errores» y «uno rechazado o vencido por timeout»: el nodo no fija umbral de timeout ni taxonomía de errores, y solo remite a WS12 para la autoridad del coordinador. Obligaría al ejecutor a inventar el valor del timeout y qué errores cuentan como rechazo/timeout, salvo que se considere detalle del TaskDoc de promoción.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (nodo, aristas, gates), WS12, WS33 y, transitivamente, WS32/WS32.1/WS32.2; `decisiones.md`, `alcance.md`.
- **Cambios previstos:** implementar adaptador y pruebas en `deskops`; ninguna mutación real durante planificación.
- **Dependencias:** WS33 y WS12; WS32 vía WS33. Gates G_EXEC/G_SCION/G_WRITE_CONTRACT pendientes.
- **Validaciones futuras:** dispatch real aceptado y otro rechazado o vencido por timeout; correlación con id de intento WS32.1 y registros WS32.2; confirmación solo con respuesta observada del Hub; ausencia de shell/transporte duplicado.

## FUTURO

- WS44 produce la evidencia de G_SCION.
- WS12 produce el contrato/canal y G_WRITE_CONTRACT por delta.
- El humano designado resuelve G_EXEC.
- WS32.1/WS32.2 aportan identidad y registros.
- El TaskDoc de promoción fija archivos, pruebas y umbrales concretos.
- WS34.2 cubre *reply*; el receptor valida el delta.
