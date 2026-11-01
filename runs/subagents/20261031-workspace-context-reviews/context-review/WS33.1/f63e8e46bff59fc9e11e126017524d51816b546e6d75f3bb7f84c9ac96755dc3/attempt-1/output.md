## REFORMULACION
WS33.1 es un nodo de implementación (no agregado) cuyo encargo es vincular mensajes y resultados de Scion a un intento ya existente, conservando procedencia y evitando duplicados. Resultado: adaptador en `runtime/`, modelos/reportes y pruebas en `deskops`. Deduplicación: Hub+proyecto+conversación+id de mensaje, y Hub+proyecto+intento+id de fuente para resultados. Solo se vinculan mensajes/resultados con referencia a un intento existente; los no resolubles quedan como hueco de procedencia. Límites: backend documental, sin tocar tablas Scion, sin dispatch/reply. Depende de WS32 y de G_SCION/G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna. El identificador de resultados «a comprobar en WS05/WS44» tiene productor nombrado y, si falta, aplica la regla común de detenerse y registrar el hueco. G_SCION/G_WRITE_CONTRACT son gates pendientes intencionales, no defectos.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el `task_file`, el contrato WS12 por delta, las salidas de WS32 sobre identidad de intento/RunDoc y la evidencia de WS05/WS44 sobre la fuente de mensajes e identificadores.

Cambios previstos: adaptador en `runtime/` que resuelva Hub/proyecto/conversación/mensaje/intento y Hub/proyecto/intento/id de fuente; modelos/reportes de procedencia; tests que importen dos veces la misma conversación y verifiquen no duplicación, no atribución de conversación completa y huecos para mensajes sin intento o con varios. Sin modificar tablas Scion.

Dependencias: WS32 (identidad de intento), WS12 (operación/actor/contrato), WS05/WS44 (API e identificadores de fuente), G_SCION. Si falta una, detenerse y registrar el hueco. Gates: G_SCION sin verificar y G_WRITE_CONTRACT `per_delta`; solo cuenta el recibo de WS33.1, no otros deltas.

Validación esperada: importación repetida idempotente, deduplicación por ambas claves, procedencia conservada y mensajes no vinculados registrados como hueco.

## FUTURO
WS32/WS32.1/WS32.2 producen identidad de intento, manifiesto y RunDoc. WS12 fija contrato, actor y operación. WS05/WS44 prueban la API pública de Scion y los identificadores de resultados. WS33.2 registra la decisión humana. WS34 habilita dispatch/reply. El operador Scion se designa al abordar el ramal E; la promoción y el acta quedan fuera de este nodo.
