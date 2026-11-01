REFORMULACION
Propósito: implementar en deskops el backend documental que vincula mensajes y resultados de Scion a un intento existente, con deduplicación y procedencia. Resultado: importación repetida sin duplicar mensajes ni resultados, sin atribuir una conversación completa a un intento y dejando huecos de procedencia para lo no vinculable. Repo dueño: deskops. Límites: depende de WS32; exige G_SCION y G_WRITE_CONTRACT; escribe en runtime/, modelos/reportes y tests; no toca tablas Scion ni UI.

AMBIGUEDADES
1. «Solo se vinculan mensajes y resultados con referencia a un id de intento existente; un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco» frente a «los mensajes no vinculados quedan como hueco de procedencia». Obliga a inventar qué hacer con un resultado sin intento resoluble o con varios: la regla solo menciona mensajes y la aceptación solo comprueba mensajes.
2. «no atribuye una conversación completa a un intento». Obliga a inventar el criterio de «conversación completa» y la comprobación que lo demuestra.
3. «una importación repetida (mismo Hub/proyecto y conversación) no duplica mensajes ni resultados». Obliga a inventar la operación o canal de importación y su repetición, pues el scope solo dice «Vincular» y no asigna quién produce la importación.

DRY-RUN
Lecturas previstas: dag.yaml, contrato G_WRITE_CONTRACT de WS12, evidencia G_SCION de WS44, inventario WS05, salidas de WS32 y matriz WS06. Cambios previstos: adaptador en runtime/, modelos/reportes y tests en deskops. Dependencias: WS32; WS12/WS05/WS44 por gates o de forma transitiva. Validaciones futuras: doble importación focalizada, ausencia de duplicados, no atribución total de conversación, huecos de procedencia y ninguna escritura en tablas Scion. Sin ejecutar.

FUTURO
WS12 produce el contrato de operaciones; WS44 produce y valida G_SCION; WS05 entrega el inventario Scion; WS32 fija la identidad de intento. El TaskDoc de promoción concretará archivos, escenarios y textos. La recepción del delta y la autorización de ejecución corresponden a actores humanos, no a este nodo.
