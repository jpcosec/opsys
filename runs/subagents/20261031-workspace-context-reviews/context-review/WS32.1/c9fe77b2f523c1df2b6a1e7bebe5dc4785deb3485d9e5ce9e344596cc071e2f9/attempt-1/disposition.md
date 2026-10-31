# Executor comparison — WS32.1

State: requires_contract_correction_rereview

## Reformulación examinada

REFORMULACION  
Propósito: separar identidad de intento de slug/agente y registrar `dispatch intent` y `confirmed` como hechos distintos, sin segundo pipeline. Resultado: implementación en `deskops` que genera ids de intento antes del dispatch, conserva identidades distintas ante dos intentos y un fallo, y deja evidencia en tests. Repo dueño: `deskops`; `output_scope`: `runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`. Límites: nodo candidato, promoción no autorizada; no ejecutar; gates `G_SCION` y `G_WRITE_CONTRACT` pendientes; si falta contrato, detenerse y registrar hueco, sin sustituto.

## Comparación con intención / hallazgos

1 registro input WS32.2 es contrato WS12 derivado inventario WS05, WS32.1 materializa, no almacenamiento inventado. 2 código modelo cambiado como código con registro/validación SLDB; instancias trackeadas por API/CLI, no ad hoc.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
