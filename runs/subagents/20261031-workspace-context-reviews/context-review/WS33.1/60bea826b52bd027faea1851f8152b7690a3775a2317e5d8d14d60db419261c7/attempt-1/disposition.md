# Executor comparison — WS33.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION
Propósito: encargo de planificación para implementar en `deskops` la vinculación de mensajes y resultados Scion a un intento existente, con deduplicación y procedencia. Resultado: backend documental idempotente, independiente del editor UI, con claves de dedup por Hub/proyecto/conversación/mensaje y por Hub/proyecto/intento/id de fuente. Repo dueño: `deskops`. Límites: no tocar tablas Scion, no dispatch/reply, no UI; gates `G_SCION` y `G_WRITE_CONTRACT` pendientes son intencionales.

## Hallazgos/disposición contra intención

1 claves explícitas de scope gobiernan: mensajes por Hub/proyecto/conversación/mensaje; resultados por Hub/proyecto/intento/id fuente. Acceptance de importar conversación repetida es escenario para probar que ninguna de ambas clases se duplica, no agrega conversación a clave de resultados. 2 scope prohíbe vincular CUALQUIER mensaje/resultado sin id de intento existente; contrato WS12 define error/hueco de procedencia y TaskDoc el caso exacto antes implementar. No asignar por conversación ni inventar intento. Dry-run respeta backend/contrato/gates por efecto y no tablas Scion.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
