## REFORMULACION

- **Propósito:** encargo agregado para unificar identidad de intento y cierre Scion, refinando el candidato de drawer citado en `external_references.scion`.
- **Resultado:** salidas de WS32.1 y WS32.2: separación intento/dispatch, registro por intento, manifiesto/RunDoc/cierre consistentes e idempotentes. WS32 no se ejecuta: termina cuando terminan sus hijos.
- **Repo dueño:** `deskops`.
- **Límites:** sin segundo pipeline, sin dispatch/reply de red, sin mocks ni eventos Hub inventados; validación local con store temporal. Estados Hub reales corresponden a WS34/37 bajo G_EXEC.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS32, gates y bloques edge de dependencias.
- **Cambios previstos:** ninguno; esta revisión no modifica el plan ni ejecuta código.
- **Dependencias identificadas:** WS05, WS12, WS32.1 y WS32.2; referencia externa con SHA-256.
- **Gates:** G_CLOSEOUT satisfecho; G_SCION no verificado; G_WRITE_CONTRACT pendiente. Su estado pendiente es intencional.
- **Validaciones futuras:** aceptación de ambos hijos, idempotencia local sin red, contrato WS12 por delta, probe real de WS44 para G_SCION y autorización humana de promoción. `promotion: not_authorized`.

## FUTURO

- **WS32.1:** materializa identidad y registro local del intento.
- **WS32.2:** hace idempotentes manifiesto, RunDoc y cierre.
- **WS05:** inventaría la API pública Scion.
- **WS12:** fija contrato y ubicación del registro por intento.
- **WS44:** produce G_SCION mediante probe real.
- **WS34/37:** prueban estados Hub reales bajo G_EXEC.
- **Humano:** autoriza promoción/ejecución y designa operador Scion al abordar el ramal E.
