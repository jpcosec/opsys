## REFORMULACION

- **Propósito:** separar identidad de intento de slug/agente y los hechos `dispatch intent` (registro local) y `confirmed` (solo respuesta Hub observada), materializando el registro por intento que WS32.2 convertirá en manifiesto canónico, sin segundo pipeline.
- **Resultado:** registro por intento e identidades según contrato WS12; dos intentos locales con IDs distintos antes de dispatch; registro intent/no confirmado mediante operaciones reales en store temporal; sin red ni Hub simulado; RunDoc/modelos vía API/CLI SLDB, no Markdown ad hoc.
- **Repo:** `deskops`. `output_scope`: `deskops/runtime/scion.py; models/run.py; services/closure.py; tests/`.
- **Límites:** sin dispatch/reply de red ni evento Hub fingido; no etiquetar no confirmado como fallo o aceptado Hub sin evidencia; no inventar almacenamiento (lo fija WS12); promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** candidato de drawer referenciado por `external_references.scion` (sha256 `125b862b…`); salidas futuras de WS05 (`auditoria/scion.md`) y WS12 (`contratos/operaciones.md`); código actual `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
- **Cambios previstos:** identidad de intento y registro por intento según el contrato WS12; pruebas con store temporal real. Nada ejecutado.
- **Dependencias:** WS05 (inventario, no gate) y WS12 (contrato/ubicación del registro); transitivas por WS12. Gates: `G_CLOSEOUT` satisfecho; `G_WRITE_CONTRACT` pendiente y evaluado por delta; `G_SCION` no verificado, producido por WS44.
- **Validaciones futuras:** dos intentos → IDs distintos; registro intent/no confirmado sin red; modelos registrados/validados por SLDB; RunDoc editado por API/CLI; ausencia de etiquetas Hub sin evidencia.

## FUTURO

- WS12 fija representación, ubicación y operaciones del registro por intento.
- WS05 entrega el inventario del runtime/API Scion.
- WS44 produce `G_SCION`; un humano designa el operador Scion al abordar el ramal E.
- WS32.2 canonicaliza manifiesto y cierre idempotente.
- WS34/WS37 prueban dispatch real y correlación bajo `G_EXEC`; un humano autoriza ejecución.
