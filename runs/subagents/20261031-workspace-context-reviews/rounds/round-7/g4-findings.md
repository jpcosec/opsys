### WS32 [1]
1. «Refinar el ticket de external_references.scion, sin segundo pipeline» frente a «Agregado: salidas de WS32.1, WS32.2». No se identifica ruta, ID ni ubicación del ticket, ni se aclara si el entregable aceptado es ese ticket refinado o el código agregado de los hijos. Obliga a inventar el artefacto concreto y su ubicación. La aceptación remite a los hijos, pero no acredita el ticket citado.
No se detectan otras ambigüedades en el bloque WS32: repo, propósito, dependencias, límites y aceptación agregada están expresados.

### WS32.1 [1]
1. «un dispatch fallido (rechazo de la API o timeout, que deja confirmed desconocido hasta reconciliar)»: no se define qué es reconciliar, quién lo ejecuta, con qué evidencia ni cuándo el estado deja de ser desconocido. Obligaría a inventar el mecanismo, el actor y el criterio comprobable; también si un rechazo explícito debe quedar desconocido o como fallo confirmado.

### WS33 [1]
1. La dependencia WS11 no se refleja en alcance, salidas ni aceptación. Cita: «depends_on: - WS32 - WS11 - WS33.1 - WS33.2» y «se cumple cuando todos sus hijos cumplen su aceptación». Aunque `integration_mode` dice «matriz WS06 llega de forma transitiva por WS11/WS12», no fija qué salida de WS11 consume WS33 ni cómo se comprueba. Obliga a inventar si WS11 condiciona el cierre del agregado o si la arista sobra; según la guía, un agregado termina con sus hijos.

### WS33.1 [2]
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, con la misma regla de deduplicación y procedencia.» La clave declarada es «Hub + proyecto + conversación + id de mensaje», campos que un resultado puede no tener. Aunque se nombra WS05/WS44 para comprobar el identificador, no se define cómo se compone la clave de resultados ni su ámbito de unicidad. Obligaría a inventar la tupla de deduplicación de resultados y si dos resultados con el mismo id de fuente en conversaciones distintas son el mismo.
2. «un mensaje con varios intentos o sin intento resoluble no se vincula»: no se fija cómo decidir que hay «varios intentos» ni el criterio de «resoluble». Obligaría a inventar la regla de resolución/desambiguación y si esos mensajes también quedan como hueco.

### WS44 [3]
1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» — no se define cómo comprobar de forma read-only la capacidad de mensajes si enviar mensajes está prohibido. Obligaría a inventar si basta con consultar un endpoint de capacidades, documentación o un listado, y qué respuesta cuenta como prueba.
2. «El operador indica el Hub desde la configuración existente» — no se identifica qué configuración ni quién la localiza/registra. Obligaría a inventar la ruta/fuente del Hub y si WS05 debe dejarlo inventariado o si el operador lo aporta por conocimiento propio.
3. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene» — no queda claro si un mapeo parcial también detiene el probe o si basta con las capabilities que sí aparezcan. Obligaría a decidir entre bloquear todo o probar un subconjunto.
