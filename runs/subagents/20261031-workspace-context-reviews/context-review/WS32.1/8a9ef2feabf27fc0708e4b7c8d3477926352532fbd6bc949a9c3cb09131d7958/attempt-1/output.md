## REFORMULACION
**Propósito:** separar identidad de intento y dispatch en el ramal Scion, sin segundo pipeline. **Resultado:** un registro local por intento con IDs distintos antes de dispatch y estado intent/no confirmado, sin red ni Hub simulado; código de modelo y RunDoc tratados por SLDB/API-CLI. **Repo:** `deskops`. **Límites:** no dispatch/reply, no evento Hub fingido, no afirmar fallo/éxito de Hub, no Markdown ad hoc; `promotion: not_authorized`. Depende del inventario WS05 y del contrato/ubicación WS12.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** nodo WS32.1, guía, brief/alcance/decisiones/reconciliación, referencia externa Scion, y contratos/artefactos de WS05 y WS12 cuando existan. **Cambios previstos:** `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`, limitados a identidad/persistencia local. **Dependencias:** WS05 aporta inventario; WS12 especifica contrato y ubicación del registro; G_CLOSEOUT está satisfecho; G_SCION sigue no verificado y G_WRITE_CONTRACT pendiente por delta. **Validaciones futuras:** dos intentos generan IDs distintos; el registro intent/no confirmado usa operaciones reales sobre store temporal; no se invoca red ni se simula Hub; el modelo se registra/valida por SLDB; RunDoc trackeado se edita por API/CLI; ningún no confirmado se etiqueta como fallo/aceptado Hub. La prueba de dispatch real y correlación queda para WS34/WS37.

## FUTURO
WS12 debe producir el contrato/ubicación del registro por intento; WS05, el inventario de identidad/API; WS44 y G_SCION, el probe público de Scion. WS34/WS37 demostrarán dispatch real fallido/confirmado y correlación exacta. La promoción requiere TaskDoc, preflight y autorización posteriores; este nodo no las concede.
