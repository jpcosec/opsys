REFORMULACION
Propósito: encargo de planificación para implementar en `deskops` la vinculación de mensajes y resultados Scion a un intento existente, con deduplicación y procedencia. Resultado: backend documental idempotente, independiente del editor UI, con claves de dedup por Hub/proyecto/conversación/mensaje y por Hub/proyecto/intento/id de fuente. Repo dueño: `deskops`. Límites: no tocar tablas Scion, no dispatch/reply, no UI; gates `G_SCION` y `G_WRITE_CONTRACT` pendientes son intencionales.

AMBIGUEDADES
1. «Los resultados se deduplican por Hub + proyecto + intento + id de fuente» frente a la aceptación «una importación repetida (mismo Hub/proyecto y conversación) no duplica mensajes ni resultados». Obliga a inventar si la conversación forma parte de la idempotencia de resultados o solo del caso de mensajes.
2. «Solo se vinculan mensajes y resultados con referencia a un id de intento existente; un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco». No fija qué ocurre con un resultado sin intento resoluble o con varios: descartarlo, registrarlo como hueco o fallar. Obliga a inventar ese comportamiento.

DRY-RUN
Lecturas: nodo WS33.1, brief/alcance/decisiones, contrato WS12, inventario WS05, probe WS44 y TaskDoc de promoción. Cambios previstos: adaptador en `runtime/`, modelos/reportes y tests en `deskops`; ninguna escritura en tablas Scion. Dependencias: WS32 (con WS11/WS12 transitivos), `G_SCION`, `G_WRITE_CONTRACT`; el identificador de fuente se comprueba en WS05/WS44. Validaciones futuras: importación repetida sin duplicados, conversación completa no atribuida a un intento, mensajes no vinculados como hueco, resultados con procedencia y ausencia de mutaciones Scion.

FUTURO
WS12 produce el contrato técnico por operación; WS44 el probe público de Scion; WS05 inventaría la fuente; WS06 integra el delta en ticket receptor o tarea atómica; el TaskDoc fija archivos, pruebas y textos; una persona autoriza promoción y aceptación por delta. Nada de esto es ambigüedad del nodo.
