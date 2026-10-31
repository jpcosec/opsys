### WS25.2 [3]
1. «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)»: no fija si toda captura debe tener origen ni qué origen corresponde cuando no nace de una ruta o un mensaje. Obliga a inventar obligatoriedad y caso sin origen.

2. «los orígenes ruta y mensaje se registran y se muestran tras recargar»: no aclara si el origen «mensaje» exige la UI de mensaje/ack de WS25.1, que no figura en `depends_on`. Obliga a inventar si falta una dependencia o si puede capturarse sin selección de mensaje.

3. «una captura persiste tras recargar» frente a «cada destino se prueba por separado»: no dice si la aceptación exige cerrar con ambos destinos o basta uno. Obliga a inventar el criterio de cierre.

### WS26.1 [3]
1. **“el candidato queda autorado con evidencia declarada”**: no se define qué constituye evidencia, quién la declara ni cómo se comprueba su validez. Obliga al ejecutor a inventar campos, formato y criterio de aceptación de la evidencia. G_CLOSEOUT habla de evidencia de closeout, no necesariamente de la evidencia de autoría.
2. **“dependencias y binding de contexto/pills”**: no se aclara si “dependencias” son las `depends_on` del TaskDoc, contra qué fuente se validan ni qué “contexto” debe vincularse. Obliga a inventar el modelo de relación y su validación. (Los “pills” quedan fuera por la guía; el “contexto” no está definido en el glosario.)
3. **“visibles tras recargar”**: no se especifica si la recarga es de la vista, del desk o del TaskDoc, ni qué debe persistir exactamente. Obliga a inventar el alcance de la comprobación de persistencia.

### WS26.2 [2]
1. «la UI la distingue de una tarea en ejecución»: el input no define qué estado o campo de deskops/lifecycle significa “en ejecución” ni cómo se relaciona con “enrutada”. Obligaría a inventar el mapeo estado→representación y el criterio de distinción visual.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc»: no se aclara si el solapamiento se evalúa solo dentro del repo receptor, entre repos, o por prefijo/ruta exacta. Obligaría a inventar la semántica de comparación y el alcance del cálculo.

### WS27.1 [3]
1. «sección por cada repo alcanzado por TaskDoc.files, con el repo declarado». No se especifica qué campo o formato declara el repo de cada ruta ni cómo resolver una ruta sin repo declarado. Obligaría a inventar la asociación ruta→repo.
2. «Diff real e historial read-only acotados al repo y tarea». «Historial» no delimita qué historia se muestra: log de commits referenciados, historial por archivo o rango. Obligaría a inventar el conjunto de eventos y su presentación.
3. «Diff Git e historial read-only junto a la TaskDoc». No se nombra la vista o componente TaskDoc ni un nodo que lo produzca. Obligaría a inventar si se crea el contenedor o se integra en uno existente.

### WS27.2 [3]
1. «declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos»: no se define cómo emparejar cada evidencia declarada con un artefacto encontrado. Obligaría a inventar la regla de identidad (ruta normalizada, hash, id u otra).
2. «verificada = resultado de `deskops closeout verify`»: no se especifica si el veredicto es por evidencia o por TaskDoc completa, ni cómo se asigna a cada evidencia. Obligaría a inventar agregación y mapeo.
3. «Evidencia junto a la TaskDoc»: no se indica cómo se selecciona la TaskDoc mostrada ni de qué contexto procede. Obligaría a inventar la fuente de selección.

### WS28 [2]
1. «output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/» — no se especifica qué endpoints ni con qué efectos. Obliga a inventar si WS28 expone un endpoint de verificación, de handoff o incluso de cierre, lo que podría contradecir «No commit/close desde HTTP en baseline».

2. «G_HUMAN_READ aplica porque es una acción de escritura del baseline» — el `scope` describe verificación, diagnóstico y handoff, no una escritura ejecutada por el nodo. Obliga a inventar si WS28 debe implementar un control de escritura o solo preparar la acción externa; de ello depende qué se prueba y qué gate aplica realmente.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en depends_on y su guion no se suministra: el ejecutor tendría que inventar escenarios y el criterio de navegación por teclado, o decidir bloquear. La regla de alcance sobre huecos no fija el orden en el DAG.
2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó». Si la causa recae en WS25/WS26 (aggregate no ejecutables, sin hijos en el input) o cruza varios nodos, el destinatario de la tarea es indeterminado; obliga a inventar dónde registrarla.

### WS31 [3]
1. «por cada contrato en contratos/ (navegacion.md, operaciones.md u otros de WS11/WS12)»: el conjunto «u otros» es abierto y `contratos/` no indica repo ni ruta base; obliga a inventar qué contratos existen y dónde leerlos.
2. «un átomo por acuerdo durable ya aceptado por humano en decisiones.md»: «acuerdo durable» no está definido y `decisiones.md` no registra aceptaciones; obliga a decidir qué acuerdos cuentan y cuáles no.
3. «comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta»: «comprobar WS29» no fija criterio (¿inicio, cierre, acta?) para pasar de propuesta a verificado; obliga a inventar la condición de comprobación.

### WS42 [2]
1. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea»: no se identifica qué modelo o versión es ni quién lo registra en el store. WS24 cita `MaterializationContractDoc` y `deskops/models/materialization.py`, pero no aclara si ese es “el registrado en el store de la tarea”. El ejecutor tendría que inventar la identidad del modelo y el criterio exacto de validación.
2. «confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar»: no se define qué datos componen “alcance” ni “procedencia”, ni cómo se registra que la confirmación mostró ambos. El ejecutor tendría que inventar campos y evidencia. Aunque el texto exacto de pantalla quede al TaskDoc, aquí falta el contenido semántico que la aceptación exige.

### WS43 [3]
1. «átomos de acuerdos durables» (output_scope) frente a un acceptance que no menciona átomos: no se define qué acuerdos son durables, de qué fuente salen (P09, `contratos/navegacion.md`, acta de WS30) ni si su ausencia bloquea la aceptación. El ejecutor tendría que inventar el conjunto y el criterio de verificación.
2. «Aplicar entradas/índices authored validados en Taller al deskops real»: el acceptance exige recorrer Markdown/UI y comprobar links/roots, pero no exige comparar que el mapa/índices publicados sean exactamente los validados en Taller; «no publicar solo ejemplo» no cubre una publicación divergente. Obligaría a inventar el criterio de equivalencia.
3. «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: «proyecto adicional» no se define frente a «todos los de `deskops list repositories`» y «repos hermanos». El ejecutor debe decidir si un repo enlazado es adicional y si enlazarlo o detenerse.
