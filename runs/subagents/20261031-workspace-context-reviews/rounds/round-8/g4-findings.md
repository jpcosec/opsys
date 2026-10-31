### WS32.2 [3]
1. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos»: no define qué hacer si la repetición trae hash de sesión o evidencia distintos. Obliga a inventar si se rechaza, se conserva el primer registro o se actualiza.
2. «hash de sesión»: no indica qué sesión, quién lo produce ni cómo se verifica; la aceptación exige que manifiesto, RunDoc y cierre coincidan en él. Obliga a inventar fuente y cálculo.
3. «según el ticket de external_references.scion»: el contenido del ticket no se suministra y solo se listan campos mínimos. Si el ticket exige más campos o reglas, el ejecutor debe inventarlos; no se nombra quién lo produce ni qué hacer si falta.

### WS33 [1]
1. Posible dependencia sobrante de WS11. Cita: `depends_on: - WS32 - WS11 - WS33.1 - WS33.2`. Los hijos solo declaran WS32 y el alcance trata vínculos Scion, deduplicación y decisión, no la navegación/identidad documental de WS11; obligaría a inventar por qué WS11 es prerrequisito del agregado o a decidir ignorarlo. Ninguna otra.

### WS33.1 [2]
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, y se deduplican por Hub + proyecto + intento + id de fuente, conservando procedencia.»  
   No define qué hacer con un resultado que tenga intento pero carezca de id de fuente, o tenga varios. La aceptación solo cubre mensajes no vinculados. Obliga a inventar si se importa, se descarta o se registra como hueco.

2. «matriz WS06 llega de forma transitiva por WS11/WS12» frente a `depends_on: - WS32`.  
   WS32 garantiza WS12, pero no WS11. El ejecutor tendría que decidir si puede avanzar sin la aceptación/matriz de WS11 o inventar el orden; falta la arista o la justificación de que WS11 no aplica.
