## REFORMULACION
Revisar WS25 como encargo de planificación: agregado de UI para mensaje/ack y captura interna en drawer/protoátomo. El resultado esperado es un juicio de claridad, no una implementación ni una evaluación del producto. Repo dueño: `graph_ui`. Límites: WS25 es `aggregate` no ejecutable; termina cuando cumplen WS25.1 y WS25.2. No se revisan los bloques edge vecinos ni se exige aprobación de gates pendientes. `promotion: not_authorized`.

## AMBIGUEDADES
Ninguna. El nodo define propósito, alcance, repo, hijos, dependencias y aceptación agregada sin obligar al ejecutor de WS25 a inventar un resultado propio: «Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación». Las operaciones quedan delegadas al contrato WS12 y los hijos precisan qué hacer si una operación no existe.

## DRY-RUN
- Lecturas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS25 y contratos de vecinos incluidos en el input.
- Cambios previstos: ninguno; esta revisión no modifica archivos ni ejecuta comandos.
- Dependencias: WS12 y agregación de WS25.1/WS25.2; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, pendientes e intencionales, evaluados por delta.
- Validaciones futuras: aceptación de ambos hijos; recibos por delta; promoción mediante TaskDoc/preflight; validación humana en WS30.

## FUTURO
WS12 produce el contrato técnico de operaciones. WS16 produce `G_HUMAN_READ`. El receptor humano P01 emite recibos `G_UI_WRITE` por delta. WS12 verifica `G_WRITE_CONTRACT` por operación/efecto. La promoción de WS25 requiere autorización humana y TaskDoc; WS30 valida los recorridos UF02/UF03. Nada de ello convierte WS25 en tarea ejecutable ni implica aprobación de implementación.
