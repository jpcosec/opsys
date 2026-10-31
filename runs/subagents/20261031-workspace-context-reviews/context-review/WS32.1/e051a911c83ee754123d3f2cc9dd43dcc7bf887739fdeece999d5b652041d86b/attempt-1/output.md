REFORMULACION  
Propósito: separar la identidad de intento de slug/agente y separar los hechos `dispatch intent`/`confirmed` del RunDoc, sin segundo pipeline. Resultado: ids de intento propios generados por deskops antes del dispatch; RunDoc modificado vía flujo SLDB, no ad hoc. Repo: deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: depende de WS05/WS12 y gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT; no autoriza promoción ni ejecución.

AMBIGUEDADES  
1. «confirmed desconocido hasta reconciliar»: no define quién reconcilia, con qué evidencia ni estado final; obliga a inventar el proceso y la aceptación del timeout.  
2. «ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico»: no aclara si WS32.1 crea el registro o solo escribe hechos que WS32.2 materializa; obliga a inventar el límite de salida frente a WS32.2.  
3. «Dos intentos del mismo agente y un dispatch fallido»: no precisa si el fallido es uno de esos dos o un tercer caso; obliga a inventar cardinalidad y evidencia esperada.

DRY-RUN  
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS32.1, edges WS05/WS12/WS32/WS32.2 y gates; sin ejecución. Cambios previstos en promoción: separar intento/dispatch, generar ids antes del dispatch, registrar `intent`/`confirmed`, integrar RunDoc vía sldb y pruebas. Dependencias: WS05/WS12; G_SCION vía WS44; manifiesto en WS32.2. Validaciones futuras: dos intentos del mismo agente, fallo/timeout, ids distintos, `confirmed`, idempotencia de WS32.2 y contrato de WS12.

FUTURO  
WS05 inventaría la API pública; WS44 produce G_SCION; WS12 produce G_WRITE_CONTRACT; G_CLOSEOUT lo resuelve un actor externo; WS32.2 vuelve canónico el manifiesto; el humano designa operador Scion en WS07 y resuelve las Pxx aplicables.
