## REFORMULACION

- **Propósito:** revisar WS32 como encargo de planificación agregado: unificar identidad de intento y cierre Scion sin crear un segundo pipeline.
- **Resultado:** agregado no ejecutable; sus salidas son las de WS32.1 y WS32.2. Sus dependientes siguen dependiendo de WS32.
- **Repo dueño:** `deskops`.
- **Límites:** no ejecutar; promoción no autorizada; integración `delta_or_existing_ticket` y `never_parallel_duplicate`; no se revisan los bloques edge vecinos; los gates pendientes son intencionales.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación y definición de WS32. Sin herramientas ni ejecución.
- **Cambios previstos:** ninguno directamente en WS32; el agregado termina cuando cumplen WS32.1 y WS32.2.
- **Dependencias:** WS32.1, WS32.2, WS05 y WS12; gates `G_CLOSEOUT`, `G_SCION` y `G_WRITE_CONTRACT`; dependencias transitivas según WS11/WS12.
- **Validaciones futuras:** aceptación de ambos hijos; resolución de gates; preflight de promoción con archivos, pills, átomos y evidencia; ninguna se ejecuta aquí.

## FUTURO

- **WS05** produce el inventario de identidad/API Scion.
- **WS12** produce el contrato técnico de operaciones y escritura (`G_WRITE_CONTRACT`).
- **WS44**, con operador designado por WS07, produce el probe de Scion (`G_SCION`).
- **Actor externo** estabiliza la evidencia de closeout (`G_CLOSEOUT`).
- **Humano** autoriza promoción y decisiones pendientes; el agente no las infiere.
- **WS32.1/WS32.2** implementan y materializan las salidas del agregado.
