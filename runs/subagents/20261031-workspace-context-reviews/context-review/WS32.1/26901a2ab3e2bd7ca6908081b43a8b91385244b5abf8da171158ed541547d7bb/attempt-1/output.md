REFORMULACION
Propósito: separar la identidad de intento del slug/agente y tratar `dispatch intent` y `confirmed` como hechos distintos del RunDoc, materializando el registro por intento que WS32.2 hará manifiesto canónico. Resultado: ticket de `external_references.scion` refinado, ids de intento generados por deskops antes del dispatch, registro por intento, cambios de RunDoc vía flujo SLDB y pruebas. Repo dueño: deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: no inventa almacenamiento ni contrato —los toma de WS12—, no usa tablas internas de Scion —WS05/WS44—, no crea segundo pipeline, no edita RunDoc ad hoc y no está autorizado a ejecutar: es candidato con gates pendientes.

AMBIGUEDADES
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc». La aceptación solo exige ids distintos para dos intentos y un dispatch fallido; no fija evidencia ni criterio comprobable de que `confirmed` quede registrado separado. El ejecutor tendría que inventar campo, registro y prueba de esa separación.

DRY-RUN
Sin ejecutar. Lecturas previstas: nodo y aristas, `external_references.scion`, auditoría WS05, contrato WS12, `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests. Cambios previstos: materializar registro por intento e identidades; generar id antes del dispatch; persistir `dispatch intent`/`confirmed`; adaptar `models/run.py` con registro/validación SLDB; pruebas de dos intentos y rechazo/timeout; ajustar el ticket. Dependencias: WS05 y WS12 como productores; G_CLOSEOUT satisfecho; G_WRITE_CONTRACT por delta; G_SCION no verificado. Validaciones futuras: ids distintos y propios; RunDoc por CLI sldb, sin edición ad hoc; separación intent/confirmed; recibos de gate por delta; idempotencia de WS32.2.

FUTURO
WS05 entrega inventario de identidad/API; WS44, probe real de G_SCION; WS12, contrato y ubicación del registro; WS32.2, manifiesto canónico e idempotencia; WS06, integración en ticket receptor; el responsable humano P01 emite acta por delta y autoriza promoción. Nada de esto se ejecuta aquí.
