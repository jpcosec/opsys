# Executor comparison — WS32.2

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION

Propósito: hacer idempotente la finalización de un intento Scion, de modo que manifiesto, RunDoc y registros de closeout queden ligados al mismo id de intento.

Resultado esperado: repetir la finalización sobre un id de intento ya finalizado no crea registros nuevos y conserva identidad y evidencia; manifiesto, RunDoc y closeout coinciden en id de intento, hash de sesión y evidencia.

Repo dueño: `deskops`, con salidas en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.

Límites: no es un segundo pipeline; el manifiesto es el registro canónico por intento según el ticket de `external_references.scion`; integración por delta o ticket existente, sin duplicado paralelo (matriz WS06 llega transitivamente por WS11/WS12). No autoriza implementación hasta promoción.

##

## Comparación con intención / hallazgos

Sesión/hash asignados a inventario WS05+contrato WS12 (artefacto log intento, campo/algoritmo/fuente reales). Si faltan no calcular hash inventado: hueco bloqueado con productor antes de promoción.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
