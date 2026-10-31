### ROOT [0]
Ninguna.

La aceptación identifica el resultado —revisión vigente de cada hijo directo—, el actor que registra bloqueos —la sesión de coordinación—, la evidencia —`disposition.md` asociada a hashes— y las validaciones —`context_review.py status` y `validate_plan.py --check`. El repo y el límite de no implementar también están explícitos. Las referencias a `publicación básica` o al ramal Scion quedan acotadas por PK06 y PK08, sin forzar al ejecutor de ROOT a definir su contenido.

### PK01 [0]
Ninguna.

### PK02 [0]
Ninguna. La aceptación fija la condición —revisión vigente por hijo o bloqueo externo con responsable—, nombra la fuente (`dag.yaml`), el artefacto (`disposition.md`) y el comando de comprobación (`context_review.py status`). Las expresiones «causa externa (ajena al encargo del propio hijo)» y «responsable (actor o repo que debe resolverla)» quedan acotadas por el registro exigido en `disposition.md`.

### PK03 [0]
ninguna

### PK04 [0]
Ninguna. La aceptación define resultado, comprobación y excepción de bloqueo; el actor que verifica es «la sesión de coordinación que ejecuta context_review.py»; el repo queda identificado por la ruta del script; y la vigencia se delega explícitamente en `context_review.py status`, no en cálculo manual del revisor. La ausencia de `owner_repo`/`kind` no obliga a inventar porque PK04 no se ejecuta como entrega.

### PK05 [0]
Ninguna.

### PK06 [1]
1. **“hash de input y de contrato”** — cita: «cuyo hash de input y de contrato coinciden con los actuales». No se define qué constituye el “contrato” cuyo hash se compara (¿bloque edge del hijo?, ¿TaskDoc?, ¿parámetros?). El ejecutor de la comprobación tendría que inventar el objeto hasheado; sin embargo, el propio input indica que `context_review.py status` lo comprueba, por lo que la invención queda delegada a la herramienta. No obliga a inventar al revisor de PK06.

Ninguna otra: hijos enumerados (WS31, WS43), criterio de verdadero/falso y tratamiento de bloqueo externo con responsable están definidos; el aggregate no requiere repo ni aceptación de producto propia.

### PK07 [0]
ninguna.

### PK08 [0]
Ninguna. La aceptación define el criterio (revisión `context_review` vigente por hash de input y contrato; disposition guardada en el intento correspondiente; bloqueo externo con responsable y dependencia), nombra la herramienta de comprobación y distingue bloqueo propio de externo. El scope enumera las materias de los ocho hijos y coincide con ellos.

### WS01 [2]
1. «cada propuesta del registro Pxx remite a decisiones.md» — el brief solo dice «Ver decisiones.md». Obliga a inventar si basta una referencia global o se exige remisión individual por Pxx, y qué propuestas quedan cubiertas.
2. Título «Fijar brief y glosario autosuficientes» frente a aceptación «Un review barato sin historial reformula el producto solo con brief.md» — no hay criterio comprobable para declarar suficiente el glosario ni para verificar las distinciones enumeradas en el scope. Obliga a inventar cómo se prueba esa parte.

### WS02 [3]
1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» + «inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs».
La enumeración mezcla áreas de almacenamiento, conceptos y artefactos sin decir qué cuenta como «archivo» de cada categoría. Obliga a inventar la unidad de fila (¿un archivo por pill?, ¿todo `desk/drawer/`?, ¿un ítem por «rol» o «run»?).

2. «Modelos y Markdown no modelado» frente a «Modelado = tiene modelo registrado en el store».
No queda claro si el Markdown no modelado es superficie inventariable (y con qué ubicación/operación) o solo una clasificación de estado. Obliga a decidir si cada `.md` del desk genera fila o solo los que tienen contrato.

3. «firmas públicas, efectos Git y cierre» frente a «la operación expuesta (comando o método que la lee o muta, o «dato pasivo»)».
No se especifica si cada firma pública (CLI/`DeskopsOperations`) es fila propia o atributo de la superficie que opera. Obliga a fijar granularidad y evita saber cuándo el inventario está completo.

### WS03 [4]
1. «referencias documentales, búsquedas (índices o consultas expuestas)»: no delimita qué referencias ni qué búsquedas inventariar, ni qué hace «expuesta» a una consulta. Obliga a inventar categorías y umbral de comprobación.
2. Título «Inventariar persistencia, consultas y notaciones» frente a scope «alcance real ViewDoc»: no aclara si «notaciones» equivale solo a notación/layout de ViewDoc o incluye otras. Obliga a inventar el universo auditado y el criterio de «real».
3. «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco»: no define la frontera entre ausencia y hueco ni la evidencia mínima. Obliga a inventar una clasificación.
4. «lectura citada del estado actual»: no fija revisión, snapshot o fuente de estado para cada repo objetivo. Obliga a elegir qué estado citar.

### WS04 [2]
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui (...) registrando la correspondencia en auditoria/ui.md». La aceptación exige tareas externas, solapamientos, SPEC y encargo, pero no una entrada por nodo del plan ni cómo marcar “sin delta”. Obligaría a inventar el criterio y la evidencia de completitud del mapeo.
2. «y cualquier encargo aportado al ejecutar». Define cuándo no hay encargo, pero no qué comparar ni con qué categorías si existe. Obligaría a inventar su tratamiento y salida.

### WS05 [4]
1. «endpoints/SDK documentados o exportados; no tablas ni funciones internas» — no fija qué fuente manda si documentación y exports discrepan, ni qué cuenta como «exportado» frente a interno. Obliga a inventar el criterio de admisibilidad, del que depende la aceptación («los campos internos que no figuren en la API pública definida en el scope»).
2. «marca qué capabilities requieren WS32 y WS33» — WS33 no aparece definido en las fuentes suministradas (solo WS32 y sus hijos). Obliga a inventar qué consume WS33 para clasificar cada capability.
3. «puede leer configuración sin secretos y no muestra tokens» — no indica rutas de configuración admisibles, qué claves son secretas ni cómo se evidencia la redacción. Obliga a inventar política de redacción y su prueba; sin ella el límite permite arrastrar credenciales al inventario.
4. «separar slug/agente/intento/dispatch/mensaje/conversación» — «conversación» no está en el glosario del brief, a diferencia de intento/RunDoc/manifiesto. Obliga a inventar su frontera respecto a mensaje.

### WS06 [3]
1. «ya cubierto (capacidad observable en código o en el Board, con referencia), extender ticket existente o nuevo delta»: no fija criterio para elegir entre las tres categorías. Obliga a inventar el umbral que separa «ya cubierto» de «extender» y de «nuevo delta».
2. «capacidad observable en código o en el Board»: no establece qué prevalece si código y Board discrepan. Obliga a inventar la autoridad de observación.
3. «Matriz con una fila por delta o capacidad propuesta»: no define granularidad de «delta» ni de «capacidad». Obliga a inventar la unidad de descomposición de las filas.

### WS07 [2]
1. «`baseline_proposal` de dag.yaml (propuesta de línea base, no aprobación del plan completo)» y output_scope «`baseline_proposal` ... en dag.yaml». No se define qué contiene ni qué debe registrarse o corregirse en esa salida. Obliga a inventar su estructura, contenido y criterio de aceptación.
2. «reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí». No dice dónde ni cómo se materializa esa reconsideración, ni qué la hace comprobable. Obliga a inventar el artefacto y su validación.

### WS08 [4]
1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: usa singular, pero cobertura.md asigna a UF01 varios nodos y gates (WS16 y WS43). Obliga a inventar si se elige un nodo/gate o se listan todos, y cuál prevalece.
2. «cubrir manual, captura, revisión...»: «manual» no es una UF de user-flows.md. Obliga a inventar si se añade una UF, una sección no-UF o se reduce a UF05/UF10, y cómo se le aplica la aceptación.
3. La lista de scope omite UF06 (delegar/intervenir), que sí existe en user-flows.md. Obliga a inventar si WS08 debe mapearla con operaciones Scion no disponibles o excluirla y remitirla a WS32–36/WS37.
4. «modo degradado (UF07, fallo de backend/dependencia)»: no aclara si es tratamiento transversal por UF o solo parte de UF07. Obliga a inventar una variante degradada por flujo o una UF separada y qué fallos cubre.

### WS09 [2]
1. «error = fallo visible esperado para esa fila» (`dag.yaml#node:WS09`): no hay fuente que enumere fallos esperados por fila; WS04 aporta disponibilidad y WS10 etiquetas, no errores. El ejecutor tendría que inventar el fallo esperado de cada fila.
2. «aceptación mediante user-flow» (`vistas.md`, ficha por vista) junto a «completa la ficha por fila» (`dag.yaml#node:WS09`): WS09 no depende de WS08, que refina el guion de user-flows, y `cobertura.md` asigna flujos a nodos, no a filas del catálogo. Se inventaría el vínculo fila→UF o faltaría una dependencia.

### WS10 [1]
1. Cita: «Definiciones verificables de disponible/propuesto/bloqueado» y «etiqueta de disponibilidad». No se fija qué evidencia o criterio hace verificable cada etiqueta —auditoría WS02–WS04, gate pendiente, capacidad no implementada— ni si deben aplicarse por capítulo o por capacidad. El ejecutor tendría que inventar la regla de clasificación y su comprobación.

### WS11 [1]
1. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer» y «Clasificar huecos sin modelos hipotéticos». No se define el universo de huecos ni el criterio de completitud: WS08/WS09 aportan flujos y catálogo, pero no se exige que el contrato enumere todos los huecos derivados de ellos. El ejecutor tendría que inventar el inventario de huecos y cuándo queda “resuelto” cada uno.

### WS12 [0]
Ninguna.

### WS13 [0]
Ninguna.

WS13 declara propósito, repo dueño, alcance, agregación, dependencias y aceptación comprobable. La aparente dualidad “Implementación o delta conciliado sobre ticket workspace en draft” queda acotada por `integration_mode: delta_or_existing_ticket; never_parallel_duplicate` y por WS13.1, que remite al acta de WS11. La inclusión de sus hijos en `depends_on` es coherente con la guía para agregados, no una dependencia sobrante. Las rutas exactas, TaskDoc y pills se delegan a promoción, y el gate pendiente no es defecto.

### WS13.1 [0]
Ninguna.

Las condiciones abiertas —representaciones soportadas, relaciones, rutas, foco y elección entre delta o ticket draft— remiten a WS11 o al catálogo WS09, que el propio nodo nombra. La ausencia de contrato se cubre con las reglas comunes de alcance, y los detalles de archivos, pruebas y textos quedan para el TaskDoc de promoción.

### WS13.2 [0]
Ninguna. La fuente del árbol y la resolución store/desk se delegan explícitamente a WS11; el uso de un store temporal real está cubierto por `alcance.md`; los archivos, pruebas y textos exactos quedan al TaskDoc de promoción.

### WS13.3 [3]
1. «Volver sigue el orden inverso de navegación.» No define qué acciones crean entrada de historia: ¿abrir documento, cambiar de pestaña, activar una división o varias? Obliga a inventar qué apila y desapila “volver”, y por tanto el criterio comprobable de historia.
2. «Pestañas, dos documentos lado a lado» no aclara si cada división tiene su propio conjunto de pestañas o si hay uno global. Obliga a inventar el modelo de disposición y cómo se abren/cierran pestañas entre divisiones.
3. «Abrir, cambiar y cerrar pestañas» no define qué documento queda activo al cerrar la pestaña activa ni si se permite cerrar la última. Obliga a inventar una transición de estado que la aceptación no cubre.

### WS14 [2]
1. Contradicción entre scope y acceptance. Cita: «Sin resultados/error/degradación diferenciados.» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». Obliga a inventar si el ejecutor debe diferenciar esos estados o, por el contrario, no hacerlo.  
2. Criterio de aceptación no comprobable. Cita: «no cargar todo grafo en cada tecla». Obliga a inventar qué cuenta como «todo grafo», cómo se observa y qué umbral o instrumentación valida el cumplimiento.

### WS15 [0]
ninguna.

### WS16 [1]
1. «Fallos abren tarea de corrección en el repo dueño»: no se identifica el repo dueño por tipo de fallo ni quién crea la tarea. Obliga a inventar si la corrección corresponde a `graph_ui`, `deskops` o `sldb/pron`, y si WS16 debe abrirla pese a `promotion: not_authorized`.

### WS17 [3]
1. **Alcance del contenido y cobertura de repos.** El título dice «entradas e índices del desk ejemplo» (singular), la aceptación exige resolver «los dos desks del manifiesto WS40» y cobertura.md asigna a WS17 índices para UF10, cuyo corpus incluye «un tercer repo temporal sin desk». Obliga a inventar si las plantillas cubren uno, dos o tres repos y qué índices mínimos son exigibles.
2. **Criterio de éxito ante la referencia rota deliberada.** La aceptación pide «recorrer links Markdown sin UI», mientras WS40 incluye «referencia rota» como parte del corpus. Obliga a inventar si esa referencia debe quedar rota, excluirse del recorrido o documentarse como error esperado; sin ello, «recorrer links» no fija aceptación comprobable.
3. **Soporte de la procedencia.** «Mostrar el root/store de procedencia al resolver los dos desks» no dice si se muestra en las propias plantillas, en un acta o en la salida del generador. Obliga a inventar dónde y cómo se materializa ese requisito.

### WS18 [2]
1. **«Vista portable renderiza sobre un store real»**: no hay definición de “portable” en brief, alcance ni glosario. Obliga a inventar el criterio de portabilidad —entre stores, hosts o formatos— y, por tanto, cuándo la aceptación se cumple.
2. **«para selecciones y notación ya soportadas»**: no se indica dónde queda fijado qué selecciones y notaciones están soportadas. WS09 inventaría renderizaciones y advierte que «ViewDoc es grafo, no contrato universal de UI»; WS11 cierra navegación e identidad, no un catálogo de notación. Obliga a inventar el conjunto exacto y el alcance de lo declarable.

### WS19 [0]
Ninguna. Lo que el nodo delega —ticket concreto, archivos, pruebas, textos— queda cubierto por `promotion`/TaskDoc o por WS04/WS06, y el contrato de operaciones lo produce WS12 con regla explícita en alcance.md para su ausencia. No hay resultado indefinido ni aceptación no comprobable en el agregado: “se cumple cuando todos sus hijos cumplen su aceptación”.

### WS19.1 [0]
ninguna.

### WS19.2 [0]
Ninguna.

### WS20 [0]
Ninguna.

### WS22 [1]
1. «estados y gates leídos de deskops (Board, lifecycle)». Las fuentes no definen qué es un “gate” de deskops ni qué operación de Board/lifecycle lo expone; “gates” solo aparece como G_* de `dag.yaml`, que la propia frase excluye. Obligaría a inventar la fuente y la semántica de los gates mostrados.

### WS23 [0]
ninguna.

### WS24 [3]
1. **Cobertura de aceptación incompleta.** El scope exige «clasificación y vecindad» y define «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops», pero la aceptación solo exige «Navegación ida/vuelta por fuentes y backlinks derivados» y el caso Markdown no modelado. Obliga a inventar si clasificación y vecindad deben probarse o solo mostrarse.
2. **«crossroads» sin definición suministrada.** Aparece en «átomos/protoátomos/crossroads (inventariados en WS02 y catalogados en WS09)», pero no está definido en brief ni glosario. Aunque WS09 lo catalogue, el nodo no fija qué entidad es ni qué representación mínima debe tener; el ejecutor tendría que inventarlo antes de esa dependencia.
3. **Alcance del Code local impreciso.** «preservar Code local del ticket workspace en draft que identifique el acta WS11» no fija si el nodo debe implementar Code o solo conservarlo; obliga a decidir el límite de cambios en esa proyección.

### WS25 [0]
Ninguna.

### WS25.1 [0]
ninguna.

### WS25.2 [3]
1. «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)»: no fija si toda captura debe tener origen ni qué origen corresponde cuando no nace de una ruta o un mensaje. Obliga a inventar obligatoriedad y caso sin origen.

2. «los orígenes ruta y mensaje se registran y se muestran tras recargar»: no aclara si el origen «mensaje» exige la UI de mensaje/ack de WS25.1, que no figura en `depends_on`. Obliga a inventar si falta una dependencia o si puede capturarse sin selección de mensaje.

3. «una captura persiste tras recargar» frente a «cada destino se prueba por separado»: no dice si la aceptación exige cerrar con ambos destinos o basta uno. Obliga a inventar el criterio de cierre.

### WS26 [0]
Ninguna.

### WS26.1 [3]
1. **“el candidato queda autorado con evidencia declarada”**: no se define qué constituye evidencia, quién la declara ni cómo se comprueba su validez. Obliga al ejecutor a inventar campos, formato y criterio de aceptación de la evidencia. G_CLOSEOUT habla de evidencia de closeout, no necesariamente de la evidencia de autoría.
2. **“dependencias y binding de contexto/pills”**: no se aclara si “dependencias” son las `depends_on` del TaskDoc, contra qué fuente se validan ni qué “contexto” debe vincularse. Obliga a inventar el modelo de relación y su validación. (Los “pills” quedan fuera por la guía; el “contexto” no está definido en el glosario.)
3. **“visibles tras recargar”**: no se especifica si la recarga es de la vista, del desk o del TaskDoc, ni qué debe persistir exactamente. Obliga a inventar el alcance de la comprobación de persistencia.

### WS26.2 [2]
1. «la UI la distingue de una tarea en ejecución»: el input no define qué estado o campo de deskops/lifecycle significa “en ejecución” ni cómo se relaciona con “enrutada”. Obligaría a inventar el mapeo estado→representación y el criterio de distinción visual.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc»: no se aclara si el solapamiento se evalúa solo dentro del repo receptor, entre repos, o por prefijo/ruta exacta. Obligaría a inventar la semántica de comparación y el alcance del cálculo.

### WS27 [0]
ninguna.

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

### WS29 [0]
Ninguna. El nodo nombra repo, salida, comandos, dependencias, gate y aceptación comprobable. La ausencia de contrato WS11 o de hallazgos queda cubierta por las reglas comunes de ejecución; el detalle de archivos y escenarios corresponde al TaskDoc de promoción. El desfase aparente entre 1 hop de WS29 y 2 hops de WS24 no obliga a inventar: cada nodo define su alcance de vista.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en depends_on y su guion no se suministra: el ejecutor tendría que inventar escenarios y el criterio de navegación por teclado, o decidir bloquear. La regla de alcance sobre huecos no fija el orden en el DAG.
2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó». Si la causa recae en WS25/WS26 (aggregate no ejecutables, sin hijos en el input) o cruza varios nodos, el destinatario de la tarea es indeterminado; obliga a inventar dónde registrarla.

### WS31 [3]
1. «por cada contrato en contratos/ (navegacion.md, operaciones.md u otros de WS11/WS12)»: el conjunto «u otros» es abierto y `contratos/` no indica repo ni ruta base; obliga a inventar qué contratos existen y dónde leerlos.
2. «un átomo por acuerdo durable ya aceptado por humano en decisiones.md»: «acuerdo durable» no está definido y `decisiones.md` no registra aceptaciones; obliga a decidir qué acuerdos cuentan y cuáles no.
3. «comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta»: «comprobar WS29» no fija criterio (¿inicio, cierre, acta?) para pasar de propuesta a verificado; obliga a inventar la condición de comprobación.

### WS32 [0]
Ninguna. La referencia a “external_references.scion” no obliga a inventar: el resultado y la aceptación quedan definidos por WS32.1/WS32.2, y el nodo es agregado. Los gates pendientes son intencionales.

### WS32.1 [4]
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc». «del RunDoc» admite leer “separados de” o “hechos del”. Obliga a inventar si viven fuera del RunDoc o como campos nuevos dentro.
2. «evidenciadas por ids de intento propios». No dice quién genera el id de intento ni con qué forma o garantía; `confirmed` remite a la identidad de la API, pero `intent` no. Obliga a inventar autoridad y generación del id (local/API/derivado).
3. «un dispatch fallido (rechazo o timeout de la API)». Un timeout no equivale a rechazo: la API pudo aceptar sin respuesta. Obliga a inventar si `confirmed` queda falso, desconocido o se reconcilia después.
4. «cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc». No define evidencia ni criterio observable de “no ad hoc”. Obliga a inventar cómo se demuestra en aceptación.

### WS32.2 [2]
1. «hash de sesión» aparece como campo mínimo y criterio de coincidencia en la aceptación, pero no se define en el input cómo obtenerlo, calcularlo ni compararlo. El ejecutor tendría que inventar su fuente y semántica de igualdad; si depende de Scion, debería indicarlo un contrato o el inventario de WS05.
2. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos» no fija qué ocurre si la repetición trae evidencia o hash distintos: conservar, rechazar o diagnosticar. El ejecutor tendría que inventar la política de conflicto.

### WS33 [0]
Ninguna.

### WS33.1 [2]
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «mismo Hub/proyecto y conversación». Obligaría a inventar si «conversación» forma parte de la identidad o es solo contexto; con ids de mensaje repetidos entre conversaciones, el ejecutor elegiría clave y podría deduplicar de más o de menos.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente […] con la misma regla de deduplicación». Obligaría a inventar la clave exacta de resultados: si «misma regla» conserva Hub+proyecto y sustituye id de mensaje por id de resultado, o añade intento; afecta deduplicación y procedencia.

### WS33.2 [2]
1. «asociada al intento y, por él, a su tarea»  
   Ningún contrato suministrado define explícitamente cómo se resuelve la tarea desde el intento; la aceptación solo exige «referencia al intento», no a la tarea. El ejecutor tendría que inventar el campo, relación o consulta intento→tarea, o decidir que basta el intento.

2. «depends_on: - WS32 - WS11 - WS33.1»  
   WS11 entrega un contrato de navegación e identidad documental, pero WS33.2 no indica qué artefacto de WS11 consume para registrar decisiones, intentos o tareas. Obliga a inventar el vínculo o a aceptar una dependencia que solo bloquea.

### WS34 [0]
Ninguna. Los elementos que podrían parecer huecos están cubiertos por fuentes suministradas:
- La autoridad del coordinador se delega explícitamente: «Autoridad del coordinador según contrato WS12».
- El contrato de operaciones tiene productor: WS12 (`G_WRITE_CONTRACT`, `produced_by: WS12`).
- La accesibilidad de Scion tiene productor: «resolver: WS44 por operador Scion designado en WS07».
- La aceptación del agregado es comprobable por composición: «se cumple cuando todos sus hijos cumplen su aceptación».
- Archivos, rutas finas y pruebas concretas quedan para promoción/TaskDoc, excluido por guía.

### WS34.1 [0]
Ninguna.

### WS34.2 [0]
Ninguna. El nodo nombra repo, resultado, aceptación comprobable, dependencias y gates. El umbral de timeout y la autoridad del coordinador se remiten al contrato de WS12; si faltara, aplican las reglas comunes de `alcance.md` (detenerse y registrar hueco), sin obligar a inventar.

### WS35 [2]
1. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea»: no define qué hacer con mensajes o resultados sin intento/tarea vinculada. Obligaría a inventar si se ocultan, se agrupan aparte o se muestran como error.
2. «la evidencia abre en el lector (WS13)»: no define el comportamiento si la evidencia no es un documento legible por WS13 (por ejemplo, un diff o artefacto). Obligaría a inventar una representación o fallback no previsto.

### WS36 [0]
Ninguna.

Las referencias a WS34, WS33.1, WS33.2 y al contrato WS12 tienen productor nombrado y heredan la regla común de detenerse y registrar el hueco si faltan. La ruta exacta, los textos de pantalla y los escenarios concretos quedan delegados al TaskDoc de promoción dentro de la aceptación. Los gates pendientes son intencionales según la guía.

### WS38 [1]
1. «output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados» — no se fija qué átomos crear ni con qué criterio quedan «vinculados»; la aceptación no menciona átomos. Obligaría al ejecutor a inventar la lista y el criterio de enlace, y a decidir si basta un átomo por capítulo o por acuerdo. Podría resolverse en la promoción si esta fija archivos, pero no se declara que los átomos sean detalle delegado.

### WS39 [0]
ninguna.

### WS40 [1]
1. **Esquema del manifiesto**: «imprime un manifiesto JSON con roots, stores, commits y documentos clave». No se fijan nombres de campos, tipos, rutas relativas/absolutas ni qué documentos son «clave». El ejecutor tendría que inventar un contrato de facto que WS16/WS30/WS17 consumirán; la aceptación solo enumera categorías, no una estructura verificable de intercambio.

### WS41 [0]
ninguna.

### WS42 [2]
1. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea»: no se identifica qué modelo o versión es ni quién lo registra en el store. WS24 cita `MaterializationContractDoc` y `deskops/models/materialization.py`, pero no aclara si ese es “el registrado en el store de la tarea”. El ejecutor tendría que inventar la identidad del modelo y el criterio exacto de validación.
2. «confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar»: no se define qué datos componen “alcance” ni “procedencia”, ni cómo se registra que la confirmación mostró ambos. El ejecutor tendría que inventar campos y evidencia. Aunque el texto exacto de pantalla quede al TaskDoc, aquí falta el contenido semántico que la aceptación exige.

### WS43 [3]
1. «átomos de acuerdos durables» (output_scope) frente a un acceptance que no menciona átomos: no se define qué acuerdos son durables, de qué fuente salen (P09, `contratos/navegacion.md`, acta de WS30) ni si su ausencia bloquea la aceptación. El ejecutor tendría que inventar el conjunto y el criterio de verificación.
2. «Aplicar entradas/índices authored validados en Taller al deskops real»: el acceptance exige recorrer Markdown/UI y comprobar links/roots, pero no exige comparar que el mapa/índices publicados sean exactamente los validados en Taller; «no publicar solo ejemplo» no cubre una publicación divergente. Obligaría a inventar el criterio de equivalencia.
3. «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: «proyecto adicional» no se define frente a «todos los de `deskops list repositories`» y «repos hermanos». El ejecutor debe decidir si un repo enlazado es adicional y si enlazarlo o detenerse.

### WS44 [2]
1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» y «capabilities… registrados»: no se define cómo se comprueba una capability de escritura (dispatch/mensaje) sin ejecutarla —¿endpoint de introspección, catálogo documentado o llamada real?—. Obligaría a inventar el método y podría chocar con el límite de no enviar mensajes.

2. «El operador indica el Hub desde la configuración existente»: no se indica ubicación, formato ni qué hacer si existen varios Hubs. Obligaría a inventar la fuente autoritativa del Hub.
