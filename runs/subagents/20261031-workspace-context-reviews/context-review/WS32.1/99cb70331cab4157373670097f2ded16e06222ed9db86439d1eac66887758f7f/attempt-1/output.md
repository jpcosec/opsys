## REFORMULACION
Propósito: separar identidad de intento y dispatch en deskops, materializando el registro por intento según WS12 y el inventario WS05. Resultado: dos intentos locales con IDs distintos y registro intent/no confirmado en store temporal, sin red ni Hub simulado. Repo: deskops. Límites: sin dispatch/reply, sin segundo pipeline, sin almacenamiento inventado, sin etiquetar no confirmado como fallo/éxito Hub; RunDoc solo por API/CLI SLDB, no Markdown ad hoc.

## AMBIGUEDADES
1. «contrato de integración explícito» (acceptance). No define artefacto, ubicación, productor ni verificación; `output_scope` solo enumera código y tests. Obligaría a inventar si es documento, prueba o interfaz. Cita: «WS34 ... y WS37 demostrarán ...; contrato de integración explícito.»
2. «Código models/run.py se cambia como código de modelo con registro/validación SLDB» (scope). No concreta modelo, campos, registro ni validación esperada. WS05 inventaría y WS12 contrata operaciones, pero no fija ese esquema; obligaría a inventar el contrato del modelo RunDoc. Cita: «Código models/run.py se cambia como código de modelo con registro/validación SLDB».

## DRY-RUN
Lecturas: nodo WS32.1, referencia externa Scion, WS05/WS12 y gates. Cambios previstos: `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`. Dependencias: WS05 y WS12; G_CLOSEOUT satisfecho, G_SCION no verificado, G_WRITE_CONTRACT pendiente. Validaciones futuras: store temporal, dos IDs distintos, sin red ni Hub simulado, sin etiquetar no confirmado, registro/validación SLDB y correlación posterior WS34/WS37. Sin ejecutar.

## FUTURO
WS05 entrega el inventario de identidad/API; WS12, el contrato y ubicación del registro por intento; WS44, el probe y G_SCION; WS34/WS37 prueban dispatch real y correlación bajo G_EXEC. El humano designa operador Scion y autoriza ejecución.
