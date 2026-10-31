### PK05 [0]
ninguna.

### PK06 [0]
ninguna.

### PK08 [1]
1. «cuyo hash de input y de contrato coinciden con los actuales». El input no define qué artefacto constituye el «contrato» del hijo ni cómo se calcula o conserva su hash. Obligaría a inventar el objeto hasheado y el procedimiento de comparación, salvo que se presuma que `context_review.py status` lo define por completo; el input no lo afirma.

### WS05 [2]
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input suministrado. Para clasificar sus capabilities el ejecutor tendría que inventar el alcance o las necesidades de WS33.
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)». No se fija qué prevalece si documentación y exports discrepan, ni el límite exacto entre símbolo exportado y función interna. Obligaría a inventar un criterio de “público” para decidir qué campos son interfaz.

### WS12 [0]
Ninguna. Las aparentes faltas —actor graph_ui/sldb, `source_mode`, G_CLOSEOUT/G_SOURCE— están cubiertas por gates, WS07 o las reglas comunes; no obligan al ejecutor de WS12 a inventar resultado, aceptación, repo o límite.

### WS17 [3]
1. Mecanismo de resolución dinámica: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» frente a «El generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se define si las plantillas usan rutas relativas, placeholders o reescritura por WS40; obligaría a inventar el formato de parametrización y quién lo aplica.
2. Cobertura entre dos desks: título/scope «entradas/índices del desk ejemplo» y aceptación «los dos desks del manifiesto WS40». No queda fijado si WS17 debe authorar índices para ambos o solo enlazar desde uno; obligaría a inventar qué plantillas pertenecen a cada desk.
3. Límite de no duplicación: «no duplicar el registry de deskops» y «sin copiar inventarios derivados» no definen qué contenido de índice cuenta como duplicado; obligaría a inventar el borde entre enlace authored y copia de inventario.

### WS21 [0]
ninguna.

### WS22 [3]
1. «con las dependencias declaradas en el TaskDoc» / «Las tres representaciones (lista, tablero y dependencias) abren el mismo TaskDoc»: no se define qué debe mostrar la representación de dependencias (aristas, lista, dirección, agrupación) ni qué hacer si el TaskDoc no las declara. Obliga a inventar el resultado y permite aceptar una vista vacía.
2. «no duplicar tareas ni presentar predicado satisfecho como test aprobado»: «predicado» no está definido en las fuentes. Obliga a inventar qué elemento de Board/lifecycle es predicado y cómo comprobar que no se confunde con un test aprobado.
3. «matriz WS06 llega de forma transitiva por WS11/WS12»: WS12 no figura en `depends_on` ni en la cadena visible (WS22→WS13→WS11; WS22→WS09). Obliga a decidir si falta una dependencia o si la matriz no es requisito de este nodo.

### WS23 [0]
Ninguna. El nodo define propósito, resultado, repo, límites, dependencias y aceptación comprobable; los detalles exactos quedan para la promoción/TaskDoc.

### WS24 [3]
1. «Vecindad = hasta 2 hops» y «la vecindad de hasta 2 hops». No indica dirección ni tipos de relación: ¿entrantes, salientes o ambas? Obliga a inventar el criterio de recorrido y qué validar.
2. «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» frente a «La vista muestra la clasificación (tipo y tags)» y «un soporte no modelado (Markdown sin modelo)». No queda definido qué clasificación mostrar sin modelo, ni si los tags provienen del modelo o del documento. Obliga a inventar representación y fuente.
3. «preservar Code local del ticket workspace en draft que identifique el acta WS11» figura en `scope`, pero no en `acceptance`. El ejecutor tendría que inventar cómo preservarlo, cómo verificarlo y qué significa identificar el acta.

### WS25 [0]
Ninguna. El nodo declara agregado no ejecutable, hijos, repo, dependencias, gates y aceptación por cumplimiento de hijos. Las concreciones de destinos, origen, permisos y respuesta local están delegadas a WS25.1/WS25.2 y al contrato WS12, sin obligar a inventar al ejecutor de este agregado.

### WS26 [0]
Ninguna. La aceptación del agregado es comprobable por composición: «se cumple cuando todos sus hijos cumplen su aceptación». El alcance remite el contrato de promoción a WS12 y el estado de commits a `G_CLOSEOUT`; no obliga a inventar resultados, actores ni límites para este nodo.

### WS28 [1]
1. **“endpoints” sin delimitar frente a “No commit/close desde HTTP en baseline”.**  
   Cita: `output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/` y `No commit/close desde HTTP en baseline.`  
   Obliga a inventar qué endpoints puede producir WS28: si son solo de verificación/diagnóstico o si se espera exponer alguna operación de cierre. El alcance prohíbe cerrar por HTTP, pero no define el conjunto permitido.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no está en `depends_on` ni se aporta su guion. Obligaría a inventar la lista de escenarios, el criterio de conflicto/teclado y sus condiciones de paso, o suponer que `validacion-humana.md` los define, aunque solo menciona conflicto y gates.
2. «el responsable del repo dueño abre tarea en el nodo que lo causó». No aclara si el responsable es `graph_ui` (dueño de WS30) o el `owner_repo` del nodo causante, ni cómo atribuir fallos de corpus/entorno (WS17/WS40). Obligaría a inventar actor y criterio de atribución.

### WS31 [1]
1. **Base de rutas de los insumos.** Cita: «incorporar el índice de borradores/manual.md» y «cada contrato en contratos/». El nodo no fija si `borradores/manual.md` y `contratos/` se resuelven desde el paquete de plan, desde `deskops:repository_root/` o desde otro repo. Obligaría a inventar la ruta base para localizar el índice y los contratos de WS11/WS12, pese a que sus productores sí están nombrados.

### WS32 [0]
Ninguna. La aceptación es comprobable por agregación: «se cumple cuando todos sus hijos cumplen su aceptación». El alcance y el resultado quedan delimitados por «Agregado: salidas de WS32.1, WS32.2» y por el carácter no ejecutable del nodo. Las referencias a gates pendientes son intencionales y no obligan a inventar.

### WS32.1 [0]
ninguna.

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

### WS33.2 [0]
Ninguna.

### WS37 [0]
Ninguna.

### WS42 [4]
1. «validan contra el modelo SLDB registrado en el store de la tarea» — no se identifica qué store («de la tarea» no coincide con «store temporal real»/«corpus WS40» de alcance.md) ni qué registro del modelo. Obliga a inventar la fuente de validación.
2. «una materialización que no valida se muestra como inválida» — no hay criterio de validación definido en las fuentes; el ejecutor tendría que inventar reglas y umbrales.
3. «bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad» — no existe mapa capability→escenario UF03 en las fuentes suministradas; obliga a inventar la correspondencia.
4. «ve el origen y el efecto de la operación antes de ejecutar» — «efecto» no se define (¿diff, lista de cambios, recuento?); obliga a inventar el contenido de la confirmación.

### WS43 [3]
1. «Repos a enlazar = todos los de `deskops list repositories`» frente a «el mapa publicado corresponde a las entradas/índices validados en Taller». Taller/WS40 solo materializa dos desks; no se define cómo representar repos listados sin entrada validada. Obliga a inventar si se omiten, se enlazan sin validar o se replica el ejemplo.
2. «Enlazar repos conocidos por identidad/origen y su entrada existente» no cubre repos sin entrada existente; junto con «Escribir una entrada dentro de otro repo requiere su tarea y acuerdo de alcance», no se sabe si quedan fuera del mapa, se enlazan a su root o se bloquea. Obliga a inventar el criterio.
3. «commit por `deskops closeout commit`» usa un canal de cierre, pero `requires` no incluye G_CLOSEOUT, que cobertura.md asocia a commits de promoción/cierre. No se sabe si el commit de publicación queda autorizado solo con G_WRITE_CONTRACT o requiere ese gate. Obliga a decidir commit o bloqueo.
