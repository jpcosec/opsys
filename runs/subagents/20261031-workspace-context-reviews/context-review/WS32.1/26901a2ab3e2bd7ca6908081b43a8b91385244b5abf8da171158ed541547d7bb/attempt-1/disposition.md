# Executor comparison — WS32.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: separar la identidad de intento del slug/agente y tratar `dispatch intent` y `confirmed` como hechos distintos del RunDoc, materializando el registro por intento que WS32.2 hará manifiesto canónico. Resultado: ticket de `external_references.scion` refinado, ids de intento generados por deskops antes del dispatch, registro por intento, cambios de RunDoc vía flujo SLDB y pruebas. Repo dueño: deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: no inventa almacenamiento ni contrato —los toma de WS12—, no usa tablas internas de Scion —WS05/WS44—, no crea segundo pipeline, no edita RunDoc ad hoc y no está autorizado a ejecutar: es candidato con gates pendientes.

## Hallazgos/disposición contra intención

Supervisor resolvió efecto real: solo identidad/persistencia local y intent/no confirmado, sin dispatch/reply red ni fallo/éxito Hub fingido. Pruebas reales locales, sin mocks. Correlación dispatch real aceptado/fallido/timeout se demuestra WS34 con G_EXEC y WS37. Contrato cambiado exige nueva revisión.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
