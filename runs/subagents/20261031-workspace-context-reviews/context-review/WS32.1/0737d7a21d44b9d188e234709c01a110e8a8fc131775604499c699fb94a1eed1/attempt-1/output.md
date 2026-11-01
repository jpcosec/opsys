## REFORMULACION

**Propósito:** separar la identidad del intento local del dispatch real, registrando `intent` y `no confirmado` como hechos distintos del RunDoc, sin red ni Hub simulado.

**Resultado:** dos intentos locales con IDs distintos y persistidos mediante operaciones reales sobre store temporal; modelo `run.py` registrado/validado por SLDB; RunDoc trackeado editado por API/CLI, nunca por Markdown ad hoc.

**Repo:** deskops (`deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`).

**Límites:** sin dispatch/reply de red, sin evento Hub fingido, sin segundo pipeline y sin afirmar éxito/fallo de Hub. Depende de WS05 y WS12; WS32.2 consume el registro. Gates: G_CLOSEOUT satisfecho, G_SCION no verificado y G_WRITE_CONTRACT pendiente por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS32.1, brief, alcance, decisiones, cobertura, reconciliación, contratos vecinos WS05/WS12 y referencia externa Scion.

**Cambios previstos:** materializar el registro por intento según contrato WS12; generar identidad local distinta por intento; representar `intent`/`no confirmado`; ajustar modelo `run.py` y cierre para no confundir intento con slug; pruebas en store temporal.

**Dependencias:** WS05 aporta inventario de identidad/API pública; WS12 fija contrato y ubicación del registro; G_WRITE_CONTRACT debe cubrir este delta. G_SCION queda para WS44 y no se usa para simular confirmación.

**Validaciones futuras:** dos IDs distintos antes de dispatch; registro persistido sin red; ningún no confirmado etiquetado como fallo o aceptado; modelo validado por SLDB; RunDoc editado por API/CLI; sin Markdown ad hoc. WS34/WS37 probarán dispatch real y correlación exacta bajo G_EXEC.

## FUTURO

WS05 produce el inventario Scion. WS12 produce contrato, ubicación del registro y recibo de escritura por delta. WS44 produce G_SCION. El humano designa operador Scion y autoriza G_EXEC. WS32.2 convierte el registro en manifiesto canónico. WS34/WS37 demuestran dispatch/reply reales y correlación con el ID previo.
