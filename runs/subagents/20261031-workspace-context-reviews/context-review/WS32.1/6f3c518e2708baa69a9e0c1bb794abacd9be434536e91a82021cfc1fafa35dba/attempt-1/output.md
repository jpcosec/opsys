REFORMULACION
Propósito: separar la identidad de intento del slug y registrar `dispatch intent` y `confirmed` como hechos distintos, sin crear un segundo pipeline. Resultado: cambios en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`, con ids de intento propios y un registro por intento que WS32.2 convertirá en manifiesto canónico. Repo dueño: `deskops`. Depende de WS05 y WS12; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT. Límites: no edición ad hoc de RunDoc —se usa el flujo SLDB/CLI sldb—, no duplicar pipeline y no promover todavía.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: nodo WS32.1, guía, brief, alcance, decisiones, gates y bloques vecinos; el ticket de `external_references.scion` si forma parte de `dag.yaml`. Cambios previstos: los archivos listados en `output_scope`; registrar intento y confirmación; pruebas de dos intentos del mismo agente y un dispatch fallido. Dependencias: WS05 y WS12 como prerrequisitos; WS32.2 consume el registro producido; G_SCION depende de WS44 y G_WRITE_CONTRACT de WS12. Validaciones futuras: aceptación con ids de intento distintos; comprobación de identidad pública de Scion; contrato de operaciones; preflight task-only de promoción. No se ejecuta nada.

FUTURO
WS32.2 convierte el registro por intento en manifiesto canónico e idempotente. WS44 produce la evidencia de G_SCION. WS12 cierra G_WRITE_CONTRACT. WS07 designa al operador Scion. Un humano resuelve los gates y autoriza o rechaza la promoción; el nodo no se promueve por esta revisión.
