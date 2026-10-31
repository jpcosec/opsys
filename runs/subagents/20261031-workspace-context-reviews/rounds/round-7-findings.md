### PK01 [0]
Ninguna.

La aceptación define el resultado como estado verificable de las revisiones de los hijos directos, delimita qué cuenta como bloqueo admisible —causa externa, responsable y dependencia registrada en `disposition.md`— y remite a un comando concreto para comprobarlo. No obliga al ejecutor de PK01 a inventar entregable, criterio de aceptación, repo de comprobación, responsable ni límite de alcance.

### PK02 [0]
Ninguna. La aceptación remite a una comprobación concreta (`context_review.py status`), define revisión vigente por coincidencia de hashes y disposition.md, y distingue bloqueo externo con responsable. No exige inventar resultado, actor ni repo.

### PK03 [2]
1. Cita: «bloqueo explícito: `context_review.status=blocked` por causa externa (ajena al encargo del propio hijo)». No se fija cómo distinguir una ambigüedad propia de un bloqueo externo cuando falta un contrato o API; obligaría a inventar el criterio de clasificación.  
2. Cita: «y dependencia en esa `disposition.md`». No se define el campo ni la forma de registrar esa dependencia; obligaría a inventar el esquema de `disposition.md` si no lo impone la herramienta.

### PK04 [3]
1. «cuyo hash de input y de contrato coinciden con los actuales»: no se define qué artefacto es el «contrato» —¿el bloque del hijo en `dag.yaml`, su `acceptance`, otro documento?— ni cómo se calcula su hash. Obliga a inventar la fuente y el algoritmo para declarar vigente una revisión.

2. «bloqueo explícito: `context_review.status=blocked` por causa externa (ajena al encargo del propio hijo)»: no hay criterio para separar una causa externa de una ambigüedad propia del hijo. Obliga a inventar la frontera y podría admitir como bloqueo lo que en realidad es un defecto del encargo.

3. «y dependencia en esa disposition.md»: no precisa qué dependencia debe registrarse —la del hijo bloqueado, la del responsable externo u otra— ni su formato mínimo. Obliga a inventar el contenido válido del registro.

### PK05 [0]
ninguna

### PK06 [0]
ninguna.

### PK07 [3]
1. «sin ambigüedad de encargo o bloqueo explícito con responsable» y «por causa externa (ajena al encargo del propio hijo)» no fijan criterio para distinguir una causa externa de una ambigüedad propia del hijo. Obligaría a inventar esa clasificación y podría cambiar el veredicto de PK07.
2. «dependencia en esa disposition.md» no define campo, formato ni vínculo con el responsable. Obligaría a inventar cómo se registra y comprueba esa dependencia.
3. «sin bloquear lector ni manual básico» no delimita qué capítulos forman el «manual básico», en particular si el capítulo 15 de WS39 queda dentro. Obligaría a decidir si `G_HUMAN_MODEL` contradice ese límite.

### PK08 [0]
Ninguna. La aceptación identifica el universo de hijos, el criterio de revisión vigente, la fuente de verdad (`context_review.py status`), el tratamiento de ambigüedad propia y la excepción de bloqueo externo con responsable registrado.

### WS02 [0]
Ninguna. La definición de superficie, las categorías, la aceptación comprobable y el repo están acotados; la falta de un contrato se rige por `alcance.md` y la promoción/TaskDoc queda fuera de este nodo.

### WS03 [0]
Ninguna.

### WS04 [4]
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui»: no define qué significa “tocar” (owner_repo, mención textual, archivos afectados). Obliga a inventar el universo de nodos incluidos.  
2. «Cada tarea externa con path, estado observado, hash y alcance» y «Hash = SHA256 del archivo de tarea»: una «entrada del Board» puede no tener archivo de tarea; obliga a inventar un path/hash o una regla de exclusión.  
3. «archivos reclamados por dos sesiones»: no define cómo se registra una reclamación ni cómo atribuir cambios de `git status` o herdr a una sesión; obliga a inventar evidencia de autoría.  
4. «reconciliar también el SPEC externo … frente a este plan»: no fija granularidad ni si “plan” comprende brief, alcance, dag y demás documentos; obliga a inventar la matriz de comparación.

### WS05 [3]
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input (solo WS32, WS32.1, WS32.2). El ejecutor tendría que inventar qué nodo es WS33 y qué capacidades necesita para poder marcarlas.
2. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco» frente a la aceptación de WS05, que obliga a «marca qué capabilities requieren WS32 y WS33». El ejecutor debe inventar si el mapeo por nodo es obligatorio para cerrar WS05 o si su ausencia es admisible y solo bloquea aguas abajo.
3. «Lee código y documentación en deskops y en el repo scion (../scion)». No consta en el input responsable ni autorización de lectura de ese repo; el ejecutor tendría que asumir acceso y que esa ruta es la fuente autoritativa frente a copias vendorizadas.

### WS06 [0]
ninguna

### WS07 [3]
1. «Designar con identidad explícita a responsable de graph_ui, sldb y spec2viz» y «con identidad registrada por el solicitante en P01». No se define qué dato constituye identidad suficiente ni cómo consta la aceptación del designado. Obligaría a inventar el formato y el criterio de designación válida.

2. «registrar qué acceso read-only tiene» el operador Scion. No se delimita el objeto del acceso —API, Hub, configuración, logs— ni su granularidad. El ejecutor tendría que inventar qué alcance consignar para que WS44 pueda probar sin ambigüedad.

3. «El humano dueño del producto confirma o corrige P01–P09» frente a «solicitante humano de esta sesión o persona que designe explícitamente» en `decisiones.md`. No se aclara si «dueño del producto» es el solicitante u otro rol; obligaría a decidir por cuenta propia quién puede firmar cada Pxx.

### WS08 [1]
1. «cubrir manual» junto con `output_scope: borradores/user-flows.md`. Obligaría a inventar qué “manual” debe cubrirse, si es un artefacto separado del user-flow, dónde se entrega y si WS08 puede escribir fuera de su `output_scope`. No hay nodo ni archivo de manual en el input.

### WS09 [2]
1. «Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes» frente a «Aplica a cada fila de las tablas de vistas.md». Obliga a decidir si el alcance se limita a las filas ya escritas o si deben añadirse filas para «vistas existentes» y categorías no listadas; sin criterio de cierre, el ejecutor inventa el conjunto inventariado.
2. «completa la ficha por fila», cuya ficha incluye «aceptación mediante user-flow», mientras la aceptación solo exige «origen, contrato..., renderer, acción/dueño, error y estado». Obliga a inventar la aceptación/user-flow de filas sin UF asociada o a decidir si ese campo queda vacío; no está definido qué campos son exigibles.

### WS10 [0]
ninguna

### WS11 [3]
1. “Resolver cada hueco como instancia/vínculo/consulta/API/renderer” y “Clasificar huecos sin modelos hipotéticos”: el input no enumera los huecos ni indica explícitamente qué artefacto de WS09/WS08 los aporta. Obligaría a inventar el inventario de huecos o a asumir una fuente no fijada.
2. “actas de aceptación de G_UI_READ y G_SPEC_VIEW en el repo receptor” frente a “owner_repo: deskops”: no queda claro si WS11 redacta/registra las actas en graph_ui/spec2viz, solo obtiene la aceptación, o las guarda en deskops. Obligaría a inventar autoría y ubicación del artefacto.
3. “graph/code admiten otros nodos con origen”: no se precisa el alcance de esa admisión para Code, mientras alcance.md limita “Code local a 1–2 hops”. Obligaría a decidir si Code navega nodos no documento o solo el ámbito local.

### WS12 [0]
Ninguna.

### WS13 [0]
Ninguna. El agregado tiene aceptación comprobable por hijos, repo dueño, alcance acotado y dependencias explícitas. `G_UI_READ` pendiente es intencional y no defecto. La elección entre implementación nueva y delta sobre el ticket en draft queda delegada a WS11 y a su acta, que el propio nodo nombra como contrato; si faltara, aplica la regla común de alcance (detenerse y registrar el hueco), sin obligar a inventar.

### WS13.1 [2]
1. «Markdown sin modelo legible»: no define qué evidencia demuestra “legible” ni la representación mínima exigida. Obligaría a inventar el criterio de aceptación y la prueba.
2. «La selección por documento/nodo fija el foco del documento abierto»: no precisa qué foco resulta al seleccionar el documento completo —frente a un nodo— ni cómo se refleja en texto/graph/code. Obligaría a inventar la semántica de foco a nivel documento.

### WS13.2 [1]
1. «al añadir un documento al store temporal de prueba, aparece sin cambiar código»
   No fija si «aparece» significa en el árbol ya abierto, tras recarga manual o por refresco automático, ni si el mismo criterio aplica a Markdown no modelado del desk. El ejecutor tendría que inventar la semántica de actualización y el alcance de esa comprobación.

### WS13.3 [4]
1. «Abrir, cambiar y cerrar pestañas» — no se define qué documento queda activo al cerrar la pestaña activa ni cómo se ajustan foco e historia. Obliga a inventar la semántica de cierre.
2. «Volver restaura documento, foco y origen. Volver sigue el orden inverso de navegación.» — no se especifica qué acciones crean entrada de historia (cambio de pestaña, apertura en división, seguir enlace) ni cómo tratar duplicados. Obliga a inventar el modelo de historia.
3. «Pestañas, dos documentos lado a lado» y «abrir dos documentos en divisiones» — no se fija si el máximo son dos divisiones o si pueden abrirse más. Obliga a inventar el límite de disposición.
4. «Disposición por sesión de navegador; no se exige persistir tras recargar.» — no aclara si el estado es en memoria o en almacenamiento de sesión, que sí sobrevive a recarga. Obliga a inventar la implementación del estado local.

### WS17 [2]
1. **No se define qué entradas/índices ni qué huecos de navegación cubrir.** Cita: «Escribir solo entradas/índices authored como plantillas versionadas bajo el paquete del plan» y «recorrer links Markdown sin UI». La aceptación solo comprueba que los links resuelven, no qué navegación debe existir; un conjunto mínimo pasaría. Obliga a inventar el contenido y la cobertura, salvo que se delegue explícitamente al TaskDoc.

2. **No se define cómo una plantilla referencia el root/store materializado.** Cita: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» y «el generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se fija si son rutas relativas al layout de WS40, marcadores sustituibles u otra convención. Obliga a inventar el mecanismo de vinculación; si no coincide con WS40, exigiría un cambio fuera de WS17.

### WS18 [0]
Ninguna. La condición «para selecciones y notación ya soportadas por spec2viz» acota el resultado sin exigir inventar un catálogo nuevo; el «store real» queda resuelto por las reglas comunes de alcance (store temporal real o corpus WS40). El gate pendiente es intencional.

### WS19 [0]
ninguna.

### WS19.1 [0]
ninguna.

### WS19.2 [0]
ninguna.

### WS20 [4]
1. Cita: «Si la capacidad existe, esos tests bastan» frente a `requires: G_SLDB_WRITE`. Obligaría a inventar si la rama de solo verificación puede cerrar sin acta de alcance sldb o si el gate es previo a cualquier trabajo. La aceptación lo exime; el nodo lo exige.

2. Cita: «Si falta, se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE». Obligaría a inventar si WS20 ejecuta la implementación o solo registra/entrega esa tarea a otro ejecutor; cambia el resultado y los cambios previstos.

3. Cita: «recuperación tras fallo». Obligaría a inventar qué fallos cubre (conflicto, validación, caída, escritura parcial) y qué evidencia demuestra recuperación; sin elegirlo, la aceptación no es comprobable.

4. Cita: «conserva campos y secciones sin pérdida». Obligaría a inventar si exige roundtrip byte-idéntico o solo semántico (orden, comentarios, formato); determina qué pruebas demuestran reversibilidad.

### WS22 [0]
Ninguna.

### WS23 [0]
ninguna. Las frases «RitualDoc/StepDoc/lifecycle sobre referencias reales», «pasos y fuentes navegables» y «transiciones solo representadas, no accionables» quedan acotadas por el glosario, WS09 y la aceptación; archivos, textos y escenarios detallados corresponden al TaskDoc de promoción.

### WS24 [2]
1. «Vecindad = hasta 2 hops.» No fija dirección ni si incluye backlinks. Obliga a inventar el conjunto exacto de nodos/relaciones que se muestra y se prueba.
2. «preservar Code local del ticket workspace en draft que identifique el acta WS11» no aparece en `acceptance` ni define cómo comprobar esa preservación o la identificación del acta. Obliga a inventar criterio y artefacto de verificación.

### WS25 [0]
Ninguna.

Las posibles dudas quedan cubiertas por el propio input: la aceptación del agregado está definida; el repo y los límites son explícitos; la ausencia de una operación de respuesta se resuelve declarándola no disponible; y las decisiones Pxx pendientes tienen actor humano y no se aprueban aquí. La repetición de los hijos en `depends_on` es coherente con la semántica de agregado y no obliga a inventar nada.

### WS25.1 [0]
ninguna.

### WS25.2 [2]
1. **Origen obligatorio frente a protoátomo libre.** Cita: «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)» y, en brief.md, «Protoátomo: átomo libre con título y contenido». Obliga a inventar si un protoátomo puede capturarse sin soporte de origen, qué origen mostrar en ese caso o si debe rechazarse; la aceptación exige «con origen» sin excepción.
2. **Elección del destino.** Cita: «destino elegido explícitamente por la persona usuaria» y «persiste tras recargar en el destino elegido». No define cómo se elige ni qué ocurre si no hay elección (¿bloquear guardado, destino por defecto, recordar último?). El ejecutor tendría que inventar el comportamiento, que afecta a la aceptación.

### WS26 [0]
Ninguna. El nodo es agregado no ejecutable, su aceptación remite a hijos identificados y las operaciones sin contrato tienen regla explícita en `alcance.md`. Los gates `G_CLOSEOUT`, `G_UI_WRITE`, `G_HUMAN_READ` y `G_WRITE_CONTRACT` están pendientes de forma intencional, no son defecto.

### WS26.1 [0]
ninguna.

### WS26.2 [2]
1. **Criterio de solapamiento de archivos.** Cita: «sin archivos solapados según los `files` declarados en cada TaskDoc y el ritual de fase». No se define si «solapados» significa coincidencia exacta de ruta, misma carpeta, prefijo o glob. El ejecutor tendría que inventar el algoritmo de comparación, y con él qué tareas aparecen como no listas.
2. **Verificación de la promoción.** Cita: «el canal de promoción respeta commits previos y estado real». No se especifica qué commits previos, qué estado real ni cómo se comprueba en este nodo; la aceptación solo detalla el enrutado y la capa lista. El ejecutor tendría que inventar el comportamiento de promoción y su prueba, o declararlo fuera sin base explícita.

### WS27 [0]
Ninguna.

### WS27.1 [3]
1. «Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado.» No se indica dónde ni quién declara el repo, ni cómo derivarlo de las rutas. Obligaría a inventar el campo, formato y criterio de agrupación.
2. «commits listados en TaskDoc.references» no precisa cómo distinguir commits de otras referencias ni el formato esperado (hash, repo, tipo). Obligaría a inventar el criterio de selección y validación de referencias.
3. «Diff Git e historial read-only» y «sin commits, working tree contra HEAD limitado a esas rutas» no fijan el alcance del historial sin commits ni si incluye solo las rutas o todos los commits referenciados. Obligaría a inventar el rango y contenido del historial.

### WS27.2 [2]
1. **Estado de verificación no ejecutada.** Cita: «verificada = resultado de `deskops closeout verify`» y «verificación fallida se muestran como estados distintos». Obliga a inventar qué se muestra cuando la verificación no se ha ejecutado: ¿cuarto estado, asimilación a “fallida”, o ausencia de estado? También si el estado es por evidencia individual o por TaskDoc.

2. **Unidad de representación con evidencias mixtas.** Cita: «declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos, sin colapsarlos». No define si una TaskDoc con varias evidencias en estados distintos se representa por lista, por estado agregado o por contadores; obliga a inventar la unidad de estado y su agregación.

### WS28 [1]
1. «G_HUMAN_READ aplica porque es una acción de escritura del baseline.» El gate G_HUMAN_READ está definido como «Persona aprueba recorrido de lectura», con evidencia de acta de lectura producida por WS16. Aplicarlo a un handoff de cierre obligaría a inventar si el acta de lectura satisface una aprobación de escritura/cierre o si WS28 necesita otra aprobación humana distinta, y cómo conciliar ambas definiciones.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08» — WS08 no figura en `depends_on` ni se suministra su guion. Obligaría a inventar esos escenarios o a asumir un artefacto no disponible. Es una dependencia que falta.

2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó» — no se define canal, actor ni repo para abrir esa tarea, y `output_scope` solo cubre `runs/subagents/workspace-documental-acceptance/manual/`. Obligaría a inventar la operación de creación y su destino, o a exceder el alcance declarado.

### WS31 [0]
Ninguna.

### WS32 [1]
1. «Refinar el ticket de external_references.scion, sin segundo pipeline» frente a «Agregado: salidas de WS32.1, WS32.2». No se identifica ruta, ID ni ubicación del ticket, ni se aclara si el entregable aceptado es ese ticket refinado o el código agregado de los hijos. Obliga a inventar el artefacto concreto y su ubicación. La aceptación remite a los hijos, pero no acredita el ticket citado.
No se detectan otras ambigüedades en el bloque WS32: repo, propósito, dependencias, límites y aceptación agregada están expresados.

### WS32.1 [1]
1. «un dispatch fallido (rechazo de la API o timeout, que deja confirmed desconocido hasta reconciliar)»: no se define qué es reconciliar, quién lo ejecuta, con qué evidencia ni cuándo el estado deja de ser desconocido. Obligaría a inventar el mecanismo, el actor y el criterio comprobable; también si un rechazo explícito debe quedar desconocido o como fallo confirmado.

### WS32.2 [0]
ninguna.

### WS33 [1]
1. La dependencia WS11 no se refleja en alcance, salidas ni aceptación. Cita: «depends_on: - WS32 - WS11 - WS33.1 - WS33.2» y «se cumple cuando todos sus hijos cumplen su aceptación». Aunque `integration_mode` dice «matriz WS06 llega de forma transitiva por WS11/WS12», no fija qué salida de WS11 consume WS33 ni cómo se comprueba. Obliga a inventar si WS11 condiciona el cierre del agregado o si la arista sobra; según la guía, un agregado termina con sus hijos.

### WS33.1 [2]
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, con la misma regla de deduplicación y procedencia.» La clave declarada es «Hub + proyecto + conversación + id de mensaje», campos que un resultado puede no tener. Aunque se nombra WS05/WS44 para comprobar el identificador, no se define cómo se compone la clave de resultados ni su ámbito de unicidad. Obligaría a inventar la tupla de deduplicación de resultados y si dos resultados con el mismo id de fuente en conversaciones distintas son el mismo.
2. «un mensaje con varios intentos o sin intento resoluble no se vincula»: no se fija cómo decidir que hay «varios intentos» ni el criterio de «resoluble». Obligaría a inventar la regla de resolución/desambiguación y si esos mensajes también quedan como hueco.

### WS33.2 [0]
Ninguna.

### WS34 [0]
Ninguna.

WS34 delega el detalle operativo en sus hijos, que ya fijan confirmación, timeout, identidad de intento y aceptación comprobable. Las dependencias futuras (WS12 y WS44) tienen productor nombrado; WS33 aporta el vínculo mensaje/intento/decisión. No hay contradicción con las fuentes suministradas ni límite que permita exceder alcance: “No shell arbitrario ni duplicar transporte” acota el adaptador.

### WS34.1 [0]
ninguna.

### WS34.2 [0]
Ninguna.

### WS39 [1]
1. «Hacer navegables Schema/editar clases ya disponibles desde documento/contexto». «Contexto» no está definido en el glosario ni se concreta si son dos entradas —documento y contexto— o una; obligaría a inventar el punto de entrada y qué superficie existente se reutiliza.

### WS40 [4]
1. **«los CLI reales de deskops/sldb verificados en WS02/WS03»**: el nodo solo declara `depends_on: WS11, WS08`; si WS02/WS03 no son ancestros, falta dependencia y el ejecutor tendría que inventar que esos CLI ya están verificados.
2. **«hace commits git reales en los repos temporales»**: no fija autor, email ni configuración git; obligaría a inventar identidad de commit o asumir una configuración global no declarada.
3. **«dos repos temporales bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)»** frente a **«Incluir un tercer repo temporal sin desk»**: no dice si el tercero vive bajo el mismo root ni cómo se limpian; obligaría a inventar ubicación y política de recreación.
4. **«bajo graph_ui:.tmp/...»**: no define exclusión git ni efecto sobre el worktree de `graph_ui`; obligaría a inventar si añadir `.gitignore` o asumir que los repos anidados no contaminan el repo real.

### WS41 [2]
1. **Dependencias contradictorias con cobertura.** El nodo declara `depends_on: WS13, WS11, WS40`, pero cobertura dice: «WS41 lectura multidesk, con WS13/14/15». Obliga a inventar si WS14 y WS15 son prerrequisitos reales —especialmente para búsqueda y errores honestos— o si sus funciones quedan fuera de la aceptación de WS41.
2. **Solapamiento de `tests/`.** WS41 incluye en su alcance «views/workspace/; tests/», mientras WS40 declara «tests/fixtures/workspace_documental/; script de seed; tests/». Obliga a decidir si WS41 puede modificar fixtures o el script de WS40, o solo añadir pruebas propias; es un límite que permite exceder el alcance del corpus ajeno.

### WS42 [2]
1. «modelo SLDB registrado en el store de la tarea»: no se define cuál es ese modelo/registro, dónde reside ni quién o con qué criterio valida una materialización. Obligaría a inventar la fuente de verdad, la ubicación del registro y la regla de validación.  
2. «confirmación … que ve el origen y el efecto de la operación» / «tras confirmación que muestra el origen y el efecto»: no se concreta qué compone el “efecto” —destino, relaciones, resultado del split/merge/typing— ni su representación mínima verificable. Obligaría a inventar el contenido de la confirmación y su comprobación.

### WS43 [0]
Ninguna. Las referencias a P08/P09, contratos pendientes y ubicación/modelo exacto quedan cubiertas por gates, dependencias transitivas, reglas comunes y promoción; no obligan a inventar resultado ni aceptación.

### WS44 [3]
1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» — no se define cómo comprobar de forma read-only la capacidad de mensajes si enviar mensajes está prohibido. Obligaría a inventar si basta con consultar un endpoint de capacidades, documentación o un listado, y qué respuesta cuenta como prueba.
2. «El operador indica el Hub desde la configuración existente» — no se identifica qué configuración ni quién la localiza/registra. Obligaría a inventar la ruta/fuente del Hub y si WS05 debe dejarlo inventariado o si el operador lo aporta por conocimiento propio.
3. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene» — no queda claro si un mapeo parcial también detiene el probe o si basta con las capabilities que sí aparezcan. Obligaría a decidir entre bloquear todo o probar un subconjunto.
