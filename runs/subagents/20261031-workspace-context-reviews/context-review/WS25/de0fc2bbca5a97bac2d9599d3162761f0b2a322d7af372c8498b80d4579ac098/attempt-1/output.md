## REFORMULACION
**Propósito:** integrar en la UI el tratamiento de mensajes/ack y la captura interna en drawer/protoátomo, usando solo operaciones permitidas por el contrato WS12 y sin confundir ack con aprobación.  
**Resultado:** nodo agregado no ejecutable; se cumple cuando WS25.1 y WS25.2 cumplen su aceptación, y su salida es la suma de ambas.  
**Repo dueño:** `graph_ui`.  
**Límites:** sin envío interdesk, sin tarea implícita, sin API/modelo nuevo; mutaciones UI sujetas a `G_HUMAN_READ`; `G_UI_WRITE` y `G_WRITE_CONTRACT` se evalúan por delta; promoción no autorizada.

## AMBIGUEDADES
Ninguna. La agregación y los gates pendientes no obligan a inventar: el alcance queda delimitado por WS25.1 y WS25.2, y la aceptación del agregado es comprobable por la aceptación de sus hijos.

## DRY-RUN
- **Lecturas previstas:** nodo WS25 en `dag.yaml`; contexto de WS25.1, WS25.2 y WS12; guía, brief, alcance, decisiones y cobertura. Los bloques de vecinos no se revisan.
- **Cambios previstos:** ninguno; este nodo no se ejecuta.
- **Dependencias:** contrato de operaciones WS12; aceptación de WS25.1 y WS25.2; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta.
- **Validaciones futuras:** aceptación de ambos hijos; acta humana de WS16; recibos del receptor P01; validación UF02 en WS30.

## FUTURO
WS12 publica el contrato de operaciones aplicable; WS25.1 y WS25.2 implementan y prueban sus deltas; WS16 produce el acta de lectura; el receptor P01 emite los recibos por delta; una persona decide la promoción; WS30 valida UF02.
