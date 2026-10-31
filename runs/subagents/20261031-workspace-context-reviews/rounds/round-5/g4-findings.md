### WS32.1 [3]
1. «confirmed desconocido hasta reconciliar»: no define quién reconcilia, con qué evidencia ni estado final; obliga a inventar el proceso y la aceptación del timeout.  
2. «ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico»: no aclara si WS32.1 crea el registro o solo escribe hechos que WS32.2 materializa; obliga a inventar el límite de salida frente a WS32.2.  
3. «Dos intentos del mismo agente y un dispatch fallido»: no precisa si el fallido es uno de esos dos o un tercer caso; obliga a inventar cardinalidad y evidencia esperada.

### WS32.2 [3]
1. «hash de sesión» — no se define qué sesión ni cómo se calcula (¿id de sesión de la API Scion, del RunDoc, derivado localmente?). El ejecutor debe inventar el origen y la función de hash para cumplir la coincidencia triple.
2. «conserva identidad y evidencia sin crear registros nuevos» — no dice qué ocurre si una segunda finalización aporta evidencia distinta. Obliga a inventar política de conflicto (rechazar, preservar la primera, marcar discrepancia).
3. «Manifiesto = registro canónico por intento que materializa RunDoc y registros de closeout» — «materializa» no aclara soporte ni forma (archivo aparte, campo embebido, registro de almacenamiento). El ejecutor debe elegir un mecanismo no fijado por la aceptación.

### WS33.1 [3]
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «una importación repetida (mismo Hub/proyecto y conversación)». No queda claro si la conversación integra la clave. Obliga a decidir si un mismo id de mensaje en conversaciones distintas deduplica o no.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente... con la misma regla de deduplicación y procedencia». No se fija la clave de resultados ni si «misma regla» remite a Hub/proyecto/mensaje. Obliga a inventar la composición de la clave.
3. «ni atribuye una conversación completa a un intento». No define criterio observable de «conversación completa» ni cómo probar la no atribución. La aceptación no es comprobable sin inventar ese criterio.

### WS38 [1]
1. «cada acuerdo durable deja su átomo vinculado»: no define qué acuerdos son «durables» ni quién los identifica. Obliga al ejecutor a inventar un criterio de selección y el conjunto de átomos exigidos. Si el acta de WS37 los enumera, la ambigüedad se resuelve con ella; el input no lo garantiza.
