## REFORMULACION
**Propósito:** nodo backend documental que vincula mensajes y resultados a un intento existente, con deduplicación y procedencia. **Resultado:** importación idempotente, sin duplicados ni atribución indebida, sin tocar tablas Scion. **Repo:** deskops; salidas en runtime/, modelos/reportes y tests. **Límites:** solo ids de intento existentes; mensajes con varios intentos o sin intento resoluble no se vinculan y registran procedencia como hueco; depende de WS32 y G_SCION; no es editor UI.

## AMBIGUEDADES
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «una importación repetida (mismo Hub/proyecto y conversación)». No queda claro si la conversación integra la clave. Obliga a decidir si un mismo id de mensaje en conversaciones distintas deduplica o no.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente... con la misma regla de deduplicación y procedencia». No se fija la clave de resultados ni si «misma regla» remite a Hub/proyecto/mensaje. Obliga a inventar la composición de la clave.
3. «ni atribuye una conversación completa a un intento». No define criterio observable de «conversación completa» ni cómo probar la no atribución. La aceptación no es comprobable sin inventar ese criterio.

## DRY-RUN
**Lecturas:** solo el input suministrado (guía, brief, alcance, decisiones, cobertura, reconciliación y nodos/gate del DAG); sin herramientas. **Cambios previstos:** ninguno en esta revisión; el nodo implementaría adaptador runtime, modelos/reportes y tests. **Dependencias:** WS32 (identidad de intento), WS11/12 por contrato y matriz, G_SCION producido por WS44; WS05 aporta inventario. **Validaciones futuras:** importación repetida sin duplicados, no atribución completa, no tocar tablas Scion, contrato público real; el TaskDoc de promoción fija archivos y escenarios.

## FUTURO
WS44 produce G_SCION; WS05 inventaría; WS32 fija identidad y contrato; WS07 designa operador Scion; WS12 fija la operación de escritura; la promoción humana autoriza TaskDoc y otro nodo ejecuta. Nada de esto es ambigüedad del nodo.
