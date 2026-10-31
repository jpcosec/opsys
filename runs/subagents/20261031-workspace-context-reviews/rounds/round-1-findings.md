### ROOT [3]
1. «según `context_review.py status`» y «`validate_plan.py --check` en PASS»: no se indica ruta, repo ni forma de invocación de esas herramientas. Obliga a inventar dónde están y cómo se ejecutan.
2. «input y contrato actuales»: no define cuándo una revisión deja de ser vigente (hash, fecha, cambio de dag o de fuentes). Obliga a inventar el criterio de frescura.
3. «sin ambigüedad de encargo o bloqueo explícito con responsable»: no define qué disposición corresponde a ROOT si un hijo queda con ambigüedad pero sin `blocked`; obliga a inventar si ROOT falla, se bloquea o escala, y quién sería el responsable.

### PK01 [0]
Ninguna.

### PK02 [0]
ninguna.

### PK03 [2]
1. «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable.» — «sin ambigüedad de encargo» no fija umbral respecto de `context_review.status`: no se sabe si basta con que la disposición guardada no sea `blocked` o si se exige un juicio adicional del revisor. Obligaría a inventar cuándo una ambigüedad residual invalida el cierre del agregado.
2. «`context_review.status=blocked` con responsable y dependencia en su disposición» — no se nombra quién registra el bloqueo ni el soporte de esa «disposición». Obligaría a inventar el actor responsable y el lugar de registro para poder acreditar el cierre de PK03.

### PK04 [3]
1. «input y contrato actuales»: no define qué es el “contrato” de un hijo ni qué versión lo hace actual. Obligaría a inventar si se compara contra `dag.yaml`, el input de review o la aceptación del hijo, y cuándo una revisión queda obsoleta.
2. «según `context_review.py status`»: no indica repo, ruta, propietario ni esquema de salida de la herramienta. Obligaría a inventar desde dónde ejecutarla y cómo interpretar sus estados.
3. «disposición guardada»: no fija ubicación, formato ni quién la guarda. Obligaría a inventar el registro de disposición y su criterio de vigencia.

### PK05 [0]
ninguna.

### PK06 [0]
ninguna.

### PK07 [3]
1. «con input y contrato actuales y disposición guardada, según `context_review.py status`»: el input no indica repo/ruta del script, ni dónde ni con qué esquema se guarda la «disposición». Obligaría a inventar la ubicación de la herramienta y el formato de almacenamiento.

2. «con input y contrato actuales»: no se define el criterio de vigencia (¿coincidencia de hash?, ¿fecha?, ¿comparación con el `dag.yaml` vigente?). El ejecutor tendría que inventar cómo decidir si una revisión está «vigente».

3. «bloqueo explícito con responsable y dependencia en su disposición»: no se especifica el campo o formato donde constan responsable y dependencia. Obligaría a inventar el esquema de la disposición.

### PK08 [0]
Ninguna. La aceptación remite a `context_review.py status`, a input/contrato actuales y a disposición guardada; los gates pendientes son intencionales según la guía. PK08 no requiere `owner_repo` propio por ser agrupación de revisión.

### WS01 [2]
1. **Aceptación no comprobable.** Cita: «Leer brief y reformular producto sin historial; acuerdos separados de propuestas.» No define qué evidencia demuestra que la reformulación es posible sin historial ni cómo se comprueba que acuerdos y propuestas quedaron separados. Obligaría a inventar un formato, una sección o un criterio de revisión.
2. **Alcance editorial de «fijar».** Cita: «Fijar brief y glosario autosuficientes», junto a `output_scope: brief.md`. No aclara si el ejecutor debe reescribir el brief, añadir secciones, conservar el texto actual y verificar, o producir una reformulación separada. Obligaría a inventar el artefacto y el grado de edición permitido.

### WS02 [3]
1. «Cada fila incluye archivo/código/operación y estado comprobado; no inferir modelo por carpeta.»  
   Obliga a inventar **qué evidencia cuenta como “estado comprobado”**: inspección estática, ejecución de prueba, fuente runtime o ausencia declarada. Sin ese criterio, el ejecutor no sabe cuándo una fila es aceptable.

2. «Modelos y Markdown no modelado» y «no inferir modelo por carpeta».  
   Obliga a inventar **qué entidad cuenta como “modelo”** y **cómo distinguir Markdown modelado de no modelado** sin usar la carpeta como criterio. El nodo no da taxonomía ni fuente de identidad.

3. «firmas públicas, efectos Git y cierre».  
   Obliga a inventar **qué firmas públicas** se inventarían (API, CLI, funciones exportadas, contratos) y **qué operaciones de cierre** entran, dado que “cierre” no se define en el nodo.

### WS03 [0]
Ninguna.

### WS04 [4]
1. «reconciliar también SPEC externo» — ninguna fuente suministrada define qué es el "SPEC externo", su repo, ruta o autoridad. Obligaría al ejecutor a inventar el objeto y su ubicación.
2. «cualquier encargo aportado al ejecutar» — no se nombra emisor, canal ni criterio de inclusión. El conjunto es indefinido y la aceptación no resulta comprobable de antemano.
3. «Cada tarea externa con path, estado observado, hash y alcance» — no se especifica qué se hashea (commit, archivo, entrada de Board) ni el formato del estado. Obligaría a inventar la unidad de evidencia.
4. «identificar sesiones y solapamientos» — "sesión" no se define (conversación, rama, ticket, tarea draft). Obligaría a inventar la unidad de observación.

### WS05 [2]
1. «Puede registrar observaciones de API ya disponibles sin crear un segundo recibo». No define si «ya disponibles» significa documentación/código o un endpoint vivo consultable, ni si WS05 puede usar credenciales existentes para lecturas. Obliga a inventar si se contacta la API o solo se lee fuente, y qué observación es admisible sin convertirse en probe.
2. «Leer runtime/templates/RunDoc y API pública de Scion». No identifica el repo que contiene esos artefactos ni si están en `deskops`; el operador Scion se designa en WS07. Obliga a inventar la ubicación de lectura y si se requiere autorización de acceso.

### WS06 [2]
1. **“Registrar acuerdos de alcance con repos dueños”** frente a **“Matriz propuesta con correspondencia ticket/delta y responsable por designar; no produce gates de aceptación ni aprueba deltas que aún no están definidos.”**  
   Queda indefinido si el nodo debe obtener/registrar acuerdos reales con los repos o solo proponer una matriz. Obliga a inventar si existe consentimiento del repo dueño y si el output debe contener acuerdos o propuestas.

2. **“Proponer atomización a dueño graph_ui sin despachar ni modificar su Board.”**  
   No se identifica al dueño de `graph_ui`; P01 sigue pendiente y WS07 —que depende de WS06— es quien debe designarlo. Obliga a inventar el destinatario o a decidir si basta dejar constancia en `reconciliacion.md` sin notificar a nadie.

### WS07 [3]
1. **Salida limitada a `decisiones.md` frente a edición del DAG.** El nodo dice “Registrar source_mode=editable o read_only en parámetros del DAG”, pero `output_scope: decisiones.md`. Obliga a inventar si WS07 puede escribir `dag.yaml` o solo declararlo en `decisiones.md` para otro nodo.
2. **Alcance de decisiones frente a G_PRODUCT.** `scope` enumera “baseline, host, fuente/edición, escritura/Git/coordinador y cierre”, mientras G_PRODUCT exige P01/P02/P07/P08/P09 y P04 como `source_mode`. P08 (uso humano y alcance) y P09 (ubicación de entradas reales) no aparecen nombradas en `scope`; obliga a inventar si WS07 debe redactarlas/registrarlas o solo esperar.
3. **“Baseline” sin referente único.** “confirma o corrige baseline” no identifica qué baseline (¿Entrega L/M/E?, ¿P03?). Obliga a inventar el conjunto de afirmaciones que el humano debe aceptar.

### WS08 [4]
1. «Mapear UF a operaciones de WS02/03/04»: WS08 solo declara `depends_on: WS07`; no se suministran las operaciones de WS02/03/04 ni qué hacer si no existen. Obliga a inventar el catálogo de operaciones o su correspondencia.
2. «cubrir manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado»: «modo degradado» no está definido en brief, alcance ni user-flows. Obliga a inventar qué estados cubre (backend ausente, link roto, CDN, etc.) y su comportamiento esperado.
3. «ack local disponible según contrato»: no identifica qué contrato ni qué nodo lo produce. Obliga a inventar si el ack existe y qué operación lo respalda.
4. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: «nodo» no distingue nodo del DAG, nodo de operación o nodo documental. Obliga a inventar la columna y su granularidad.

### WS09 [3]
1. **Alcance de "cada fila"**. Cita: «Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado» frente a «Ficha de cada vista (pendiente de completar)». `vistas.md` tiene tres tablas (catálogo, «Filas que faltaban», ficha) y filas-categoría («Cualquier documento del desk») que no son vistas. Obliga a inventar si la aceptación se aplica a todas las tablas, solo al catálogo, y si la granularidad es fila o vista.
2. **Taxonomía de "error" y "estado"**. Cita: «error y estado». No se define qué valores son válidos (¿error de resolución de origen, de renderer, de contrato?; ¿disponible/planificado/inexistente?). Obliga a inventar el vocabulario con el que se comprueba la aceptación.
3. **Fuente del inventario de "vistas existentes"**. Cita: «Inventariar ... y vistas existentes» y «disponibilidad actual» en la ficha. El nodo no nombra quién aporta el inventario de renderizadores de graph_ui/spec2viz ni qué hacer si no hay acceso; con `owner_repo: deskops` obliga a inventar el "estado" de disponibilidad o a leer código no designado.

### WS10 [1]
1. Base de evidencia para “disponible”. Cita: «Las afirmaciones de capacidades se contrastan con WS02–WS04». El nodo solo declara `depends_on: WS02, WS07`; WS04 no está. Para cumplir «Definiciones verificables de disponible/propuesto/bloqueado», el ejecutor tendría que inventar si basta WS02 o si debe esperar/incorporar WS04. Es dependencia que falta y contradicción con la fuente suministrada.

### WS11 [1]
1. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer»: no se definen “instancia” ni “vínculo”, ni el criterio para asignar un hueco a cada categoría. Obligaría al ejecutor a inventar una taxonomía de clasificación y sus reglas de uso. El glosario define “consulta” y “renderización”, pero no esos dos términos.

### WS12 [2]
1. «registrar capability exacta para cada acción». No se enumera el universo de «acciones» ni su granularidad: ¿campo, relación, endpoint, comando o flujo? El ejecutor tendría que inventar el catálogo y el nivel de detalle, con riesgo de omitir operaciones de WS19/25/26/28/32/34/39/42 o exceder el contrato.
2. «adapter CLI/API público». No se identifica si es un adaptador ya existente de `deskops`, una API pública verificada de otro repo o un componente nuevo. El ejecutor tendría que inventar si WS12 documenta canales existentes o diseña nombres/endpoints nuevos, y de quién es la autoridad del adapter.

### WS13 [2]
1. **Dependencia faltante de WS06.** Cita: `integration_mode: delta_or_existing_ticket_only_after_WS06` y `depends_on: WS11, WS13.1, WS13.2, WS13.3`. WS13 exige esperar a WS06, pero no lo declara como dependencia. Obligaría a inventar si la matriz de WS06 ya está disponible, si condiciona el alcance del delta o si basta el acta de WS11.

2. **Alcance del “registro de renderer”.** Cita: `Registro de renderer en código permitido; organización de contenido procede de documentos/consultas.` No aclara si se reutiliza un registro existente o se crea uno nuevo. Obligaría a decidir una arquitectura no fijada por el nodo; si se interpreta como permiso amplio, podría exceder el delta de lector.

### WS13.1 [2]
1. «seguir un enlace y cambiar texto/graph/code … preserva origen»: «cambiar» admite dos lecturas — alternar entre representaciones o modificar el contenido. La segunda contradice «Documento/fuente solo lectura» y obligaría a inventar si el nodo incluye edición.
2. «el panel de contexto muestra identidad, relaciones y origen reales»: no se enuncia qué relaciones ni con qué fuente se obtienen. WS11 cubre identidad/resolución y clasificación de huecos, pero no se declara allí el inventario del panel; el ejecutor tendría que inventar el conjunto de relaciones y el significado operativo de «origen».

### WS13.2 [4]
1. «La organización del contenido procede de documentos/consultas» — no se identifica qué documentos/consultas ni si existe infraestructura de consulta. WS11 aporta rutas de lectura, no necesariamente el mecanismo de listado. Obligaría a inventar el origen del árbol.
2. «el listado no es inventario hardcodeado» — no define cómo comprobarlo. Obligaría a inventar el criterio y la prueba de aceptación (por ejemplo, alta/baja de un documento).
3. «Explorador sobre documentos reales del store y Markdown no modelado del desk» — no nombra corpus, ruta concreta ni dependencia de WS40; la aceptación exige abrir ambos tipos. Obligaría a inventar fixtures.
4. `integration_mode: "delta_or_existing_ticket_only_after_WS06; never_parallel_duplicate"` — WS06 no figura en `depends_on`. Obligaría a decidir si es prerrequisito efectivo o solo referencia.

### WS13.3 [4]
1. «alternar foco y volver conservando origen e historia» — no define qué evidencia prueba "conservar historia": ¿orden del stack de vuelta, profundidad, persistencia tras recarga? Obliga a inventar el criterio de aceptación comprobable.
2. «Pestañas, dos documentos lado a lado, foco e historia de navegación» frente al glosario («Foco: elemento seleccionado por una persona, compartido entre representaciones del mismo documento») — no aclara si cambiar de pestaña cambia el foco del documento o solo la vista activa. Obliga a inventar la semántica de foco entre divisiones.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06» — WS06 no figura en `depends_on` ni en `requires` del nodo. Obliga a inventar si WS13.3 puede ejecutarse antes de que exista el resultado de WS06.
4. «disposición como estado local según P07» — no precisa si "local" es por sesión o persistido en el navegador. Obliga a inventar el comportamiento (y su prueba) de la disposición al reabrir.

### WS14 [3]
1. «Usar find público, no parser propio».
   No se identifica qué API `find` concreta debe usarse, quién la produce ni qué hacer si no existe. Obliga a inventar el contrato, sus parámetros y su semántica de resultados.

2. «Teclado y abrir/volver conservan consulta y foco».
   No define qué recorridos ni qué límites de persistencia cuentan para aceptar la conservación. Obliga a inventar los escenarios comprobables y el criterio de éxito.

3. «Búsqueda vacía/error/degradación diferenciados».
   No delimita qué condiciones producen cada estado ni qué diferencia observable se exige. Obliga a inventar estados de UI y criterios de comprobación.

### WS15 [2]
1. «proyecto sin desk muestra orientación, destino explícito e init CLI» y «muestra orientación y destino sin mutar nada». No se define qué es “destino”: ruta del desk, URL, comando o documento de handoff. Obliga a inventar el contenido mostrado y el criterio para comprobar que el destino es explícito.
2. «modelo no importable, backend caído» no identifica qué modelo ni cómo distinguir ambos fallos. Obliga a inventar la taxonomía de errores y la detección que decide cuál se muestra.

### WS15.1 [5]
1. «error localizado sin borrar historial ni fingir vacío» (scope). Obliga a inventar el grano del error: ¿por panel, por documento, inline o global? «Localizado» también podría leerse como traducción i18n.
2. «recuperar conexión sin perder contexto» (acceptance). No define mecanismo (reintento manual, automático, backoff) ni qué contexto debe preservarse; no es comprobable sin inventar estados y criterio de éxito.
3. «CDN actual diagnosticado» (acceptance). No indica dónde se registra el diagnóstico ni qué evidencia lo demuestra; `output_scope` no incluye artefacto de evidencia, obligando a inventarlo.
4. «Leer Markdown existente cuando el soporte lo permita, informar límites reales» (acceptance). La lectura corresponde a WS13; «límites reales» no enumera cuáles ni con qué mensaje, obligando a inventar el catálogo de errores y su verificabilidad.
5. «modelo no importable, backend caído» (scope). No se especifica taxonomía ni distinción observable entre ambos; el ejecutor debe inventar detección y mensajes.

### WS15.2 [2]
1. «destino explícito» / «muestra orientación y destino». No se define qué es “destino”: ruta del proyecto, ubicación donde ejecutar init, comando, URL o siguiente paso. Obliga a inventar el contenido mostrado y el criterio de aceptación de ese elemento.  
2. «init CLI». No se indica comando, argumentos ni desde dónde ejecutarlo; el nodo tampoco declara de qué nodo/artefacto toma esa instrucción ni qué hacer si falta. Obliga a inventar la instrucción que la UI debe mostrar.

### WS16 [2]
1. **Alcance del corpus/ejemplo.** Cita: «desk ejemplo y protocolo en validacion-humana.md» y «Preparar corpus por WS40». La primera frase puede leerse como que WS16 prepara el desk de ejemplo; la segunda y validacion-humana.md asignan a WS40 el rol de «productor único». Obliga a inventar si WS16 crea/edita el corpus o solo consume su manifiesto.
2. **Mediciones aplicables.** Cita: «Reportar tiempos y pruebas técnicas por separado» junto a «Medir al menos 20 aperturas, 10 búsquedas y 10 guardados». WS16 es lectura y no puede mutar antes de `G_HUMAN_READ`; obliga a inventar si debe medir guardados, omitirlos o registrar “N/A”.

### WS17 [0]
ninguna.

### WS18 [0]
ninguna

### WS19 [0]
ninguna

### WS19.1 [2]
1. **“modo manual coordinado” contradice P03.** WS19.1: *“Mutación restringida a desk en modo manual coordinado; otros modos read-only hasta contrato.”* P03: *“Baseline editable solo en desk en modo manual exclusivo; con coordinador escritor activo, UI read-only/handoff hasta canal autorizado real.”* El ejecutor tendría que inventar si “coordinado” implica coordinador activo y, por tanto, si puede escribir o debe quedar read-only.
2. **“revisión esperada y conflicto visible” no define resultado ni aceptación comprobable.** WS19.1: *“con revisión esperada y conflicto visible”*; la aceptación solo añade *“una escritura obsoleta no pierde texto local”*. No se define si “revisión” es CAS, revisión humana u otra, ni qué hace “visible” al conflicto. El ejecutor tendría que inventar comportamiento y criterio de verificación.

### WS19.2 [2]
1. «usando API real y before-image»  
   No se define qué es la before-image, quién la produce, su formato, persistencia ni qué ocurre si no está disponible. WS12 cubre contrato de operaciones, CAS/locks y fallos parciales, pero el nodo no declara explícitamente que la before-image forme parte de ese contrato. El ejecutor tendría que inventar su modelo y ciclo de vida.

2. «endpoints autorizados por el contrato WS12»  
   El nodo nombra a WS12 como productor, pero no indica qué hacer si el contrato no incluye endpoints de alta/baja de relaciones. Sin un fallback explícito en el encargo (detener, handoff o registrar hueco), el ejecutor debe decidir por su cuenta.

### WS20 [4]
1. «Si falta: intake/tarea sldb propia y roundtrip, conflicto y recuperación reales antes de cerrar G_SOURCE.» No queda claro si WS20 debe implementar la capacidad faltante o solo abrir intake/tarea. Obligaría a inventar el resultado y si el cierre exige código o solo handoff.
2. «Si capacidad existe: evidencia de contrato suficiente, no código duplicado.» “Suficiente” no es comprobable y contrasta con G_SOURCE: «API pública y tests roundtrip/conflicto/campos protegidos». Obligaría a inventar qué evidencia basta y si la rama “existe” también exige esas pruebas.
3. «roundtrip, conflicto y recuperación reales» no define escenarios, resultados esperados ni criterio de recuperación. Obligaría a inventar casos y umbrales de aceptación.
4. «guardado fuente reversible» no concreta qué reversibilidad se prueba (¿roundtrip, conflicto, deshacer?). Obligaría a inventar el criterio; P04 solo dice «API reversible probada».

### WS21 [3]
1. «pending bloquea preparación»: no define si el bloqueo abarca todo el nodo o solo preflight/promoción, ni qué parte read-only podría prepararse; el ejecutor inventaría el alcance del bloqueo. Además, «Cumplir la aceptación específica de la variante P04» carece de rama para `pending`.
2. «Alternar fuente/render con mismo origen, revisión y dirty buffer»: no fija qué ocurre al alternar con cambios sin guardar en modo editable (conservar, descartar, bloquear); solo read_only dice «Conservar buffer/foco». Se inventaría política y prueba.
3. Título «Integrar fuente y renderizado editables» contradice la variante read_only («Fuente explícitamente read-only»); no se sabe cómo nombrar/documentar la entrega en ese modo.

### WS22 [5]
1. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: WS13, WS09`. Falta WS06 como arista o el texto contradice las dependencias; obliga a inventar si WS06 debe resolverse antes de ejecutar o solo informa la integración.

2. «Representar Board real como lista/tablero y dependencias». No queda claro si exige ambas representaciones o una alternativa; la aceptación no distingue, obligando a inventar alcance y criterio de comprobación.

3. «abriendo los mismos TaskDoc/contextos». «Contextos» no está definido: puede ser panel, pill, enlace o selección. Obliga a inventar qué se abre y con qué contrato.

4. «estados/gates reales». No se indica la fuente de verdad ni cómo demostrar «real»; ¿Board de graph_ui, gates de `dag.yaml` o ambos? Obliga a inventar la comprobación.

5. «Selección y links comunes con lector». «Lector» remite a WS13, pero no se define cómo se comparte selección entre tareas del Board y documentos; obliga a inventar el comportamiento de foco/enlaces.

### WS23 [4]
1. «RitualDoc/StepDoc/lifecycle» y «obligaciones, transiciones»: ninguno de estos términos está definido en el glosario ni se indica qué nodo produce su esquema. Obligaría a inventar modelo, estados, obligaciones y transiciones de paso.
2. «sobre referencias reales» y «Un procedimiento abre sus documentos y soporte»: no se nombra corpus, fixture ni resolución concreta, y WS23 no depende de WS40. Obligaría a inventar qué procedimiento real usar y qué cuenta como «soporte» abierto para poder verificar la aceptación.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: [WS13, WS09]`: no existe arista ni gate que garantice WS06. Obligaría a decidir si WS06 es prerrequisito real o solo una condición declarativa.
4. «no auto-marcar pasos como realizados por leerlos»: no se define quién o qué produce el estado «realizado» ni su contrato. Obligaría a inventar el mecanismo de marcado para poder probar la negación.

### WS24 [4]
1. **«backlinks derivados»** — no se indica qué contrato, store o consulta los deriva ni quién los produce. Obliga a inventar la fuente y el criterio de derivación, y la aceptación deja de ser comprobable.
2. **«clasificación y vecindad»** — no se define qué clasificación (¿átomos/protoátomos/crossroads?) ni qué relaciones o profundidad constituyen vecindad. Obliga a inventar semántica funcional.
3. **«soporte no modelado visible»** — no se especifica qué cuenta como no modelado ni qué visibilidad mínima se exige. Obliga a inventar el criterio de aceptación.
4. **«preservar Code local de tarea actual»** — no se identifica la tarea ni qué parte de Code debe preservarse. Obliga a inventar el límite de no regresión.

### WS25 [1]
1. «captura interna de drawer/protoátomo» — “protoátomo” no aparece definido en brief, glosario, alcance ni decisiones, y no se nombra fuente que fije su esquema, campos o ciclo de vida. Obligaría al ejecutor a inventar qué es un protoátomo, cómo se distingue de un drawer y qué datos mínimos debe persistir.

### WS25.1 [2]
1. «registrar ack o respuesta local» / «sin envío interdesk». No define qué es una “respuesta local”: ¿contestación al emisor dentro del desk, nota local o cambio de estado? Tampoco sus campos ni destino, ni el store/API que provee los mensajes del inbox. WS12 se nombra para «endpoints autorizados», no para el modelo del inbox ni la semántica de respuesta; obligaría a inventar resultado y UI.

2. «Ack y respuesta local persisten tras recargar con origen visible». No define qué metadato constituye “origen” —autor, canal, documento, mensaje padre— ni cómo mostrarlo; obligaría a inventar el criterio de aceptación.

### WS25.2 [2]
1. «Captura interna de drawer/protoátomo mediante operaciones permitidas por contrato»: «protoátomo» no está definido en las fuentes suministradas e «interna» no aclara si la captura ocurre dentro del drawer, dentro del protoátomo o en la UI. Obligaría a inventar cuál es el artefacto destino y qué hace «interna».
2. «una captura persiste tras recargar con origen»: «origen» no define campo, valor ni formato comprobable —documento, nodo, usuario u otro—. Obligaría a inventar qué dato debe persistirse y cómo verificarlo en la recarga.

### WS26 [3]
1. «representación de capa lista por dependencias/no solapamiento». No se define qué es «capa lista» ni el criterio de «no solapamiento». Obligaría a inventar si es frontera de dependencias, conjunto de tareas sin archivos comunes u otra vista, y cómo comprobarlo.
2. «Autoría explícita desde candidato». Las fuentes suministradas no definen «candidato» como entidad, origen ni transición. Obligaría a inventar si es tarea borrador, registro de intake, nodo del DAG u otro soporte, y qué operación de autoría se espera.
3. «El canal de promoción debe respetar commits previos y estado real». No concreta qué commits previos ni cómo se verifica «estado real». WS12 es dependencia, pero el nodo no declara explícitamente que ese criterio queda delegado ni qué hacer si el contrato no lo cubre.

### WS26.1 [3]
1. «Autoría explícita desde candidato». «candidato» no está definido en brief, glosario ni cobertura; obligaría a inventar qué entidad/estado es y cómo se convierte en tarea autorada.
2. «UF04 sobre TaskDoc real». UF04 solo figura como «preparar trabajo» en cobertura, sin pasos ni resultado esperado para autoría/evidencia/contexto; obligaría a inventar el guion y el criterio de aceptación.
3. «el gate humano no pasa hasta resolver». El nodo requiere varios gates humanos/contrato; obligaría a inventar cuál bloquea y quién lo resuelve.

### WS26.2 [3]
1. “representación de capa lista por dependencias/no solapamiento” — no se define qué es una “capa lista”, qué la hace estar lista, qué representa visualmente ni qué significa “no solapamiento”. Obliga a inventar definición, criterio y forma de representación.
2. “Enrutamiento explícito en Board” — no se especifica si “enrutamiento” es ruta URL, flujo de estados, relación de dependencias o navegación entre tareas. Obliga a inventar su semántica y comportamiento observable.
3. “Board real refleja el enrutamiento sin confundirlo con ejecución; el canal de promoción respeta commits previos y estado real” — la aceptación no fija evidencia, observable ni quién la certifica. Obliga a inventar la prueba de aceptación.

### WS27 [2]
1. «diferenciar cambios de código de integridad del store» carece de criterio comprobable. Las aceptaciones hijas cubren diff real (WS27.1) y evidencia declarada/encontrada/verificada (WS27.2), pero ninguna define qué representa «integridad del store» ni cómo mostrarla. Obligaría al ejecutor a inventar fuente, indicador y validación.
2. «artefactos de evidencia junto al encargo» no define qué es «el encargo» ni su ubicación. WS27.2 remite a «rutas de lectura definidas por el contrato WS11», pero el input no incluye ese contrato; sin él, el ejecutor debe inventar el contenedor o ubicación. No basta con que WS11 sea productor futuro: el nodo no indica qué hacer si falta.

### WS27.1 [4]
1. «Diff real acotado al repo y tarea»: no se fija el baseline del diff. Obliga a inventar qué se compara —working tree, HEAD, rango de commits— y cómo se selecciona. WS12 menciona política Git, pero el nodo no declara que ese contrato produzca el baseline.
2. «acotado al repo y tarea»: no se define qué identifica la “tarea” ni cómo se relaciona con repo/rutas. Obliga a inventar la fuente del identificador y el filtro. WS35 solo añade «asociación a intento», no la identidad de tarea.
3. «Diff Git e historial read-only» frente a «sin execute/revert genérico»: “genérico” deja abierta la posibilidad de execute/revert dirigidos, contradiciendo el límite read-only. Obliga a inventar si alguna mutación específica está permitida.
4. «diferenciar cambios de código de integridad del store»: no hay criterio, etiquetas ni evidencia esperada para esa clasificación. Obliga a inventar categorías y cómo demostrarlas; además, no aparece en la aceptación.

### WS27.2 [3]
1. «Mostrar declarada/encontrada/verificada y abrir su soporte; una evidencia ausente se ve como ausente.» No se define qué es cada estado, de dónde sale la evidencia, ni cómo se determina «verificada». Obligaría a inventar el modelo de datos, la fuente y el criterio de verificación.
2. «abrir su soporte» no precisa qué debe abrirse —documento fuente, artefacto, ruta o representación— ni el comportamiento esperado. Obligaría a inventar el destino y la interacción de apertura.
3. «Artefactos de evidencia junto al encargo» y «sin inventar CommentDoc antes de contrato»: «encargo» y `CommentDoc` no están definidos, y «contrato» no se identifica. Obligaría a inventar la ubicación/vinculación de artefactos y si los comentarios pueden usarse como soporte.

### WS28 [3]
1. «Verificar con autoridad Deskops» no identifica la API, comando, estado o artefacto concreto que constituye esa autoridad. Obligaría a inventar cómo consultar el resultado real y qué fuente prevalece frente al contrato de WS12.
2. «ofrecer handoff explícito a closeout CLI/coordinador» plantea dos canales alternativos sin criterio de elección ni forma de confirmación. Obligaría a inventar cuál se implementa y qué evidencia demuestra que el cierre externo terminó, pese a que «comando o solicitud no equivalen a cierre».
3. La lista `requires` incluye `G_HUMAN_READ` sin relación declarada con el cierre. Obligaría a inventar por qué la aprobación del recorrido de lectura condiciona la verificación/handoff de WS28.

### WS29 [5]
1. «Mutaciones reales muestran soporte/alcance/errores». «Soporte» y «alcance» no se definen: el ejecutor debería inventar qué evidencia visual/datos demuestra cada uno y qué mutaciones se prueban.
2. «Reparar no es automático: acción documentada o tarea explícita». No se dice quién documenta, dónde ni con qué formato; obligaría a inventar el entregable de reparación.
3. «stores check/doctor/drift y relaciones comprobadas». No se identifican los stores, comandos ni quién produce ese inventario; el ejecutor tendría que suponer API/superficie existente.
4. «integration_mode: delta_or_existing_ticket_only_after_WS06» y `overlap_with: changes`, pero WS06 no figura en `depends_on`. Obliga a decidir si WS06 es prerrequisito real o solo condición de promoción.
5. «output_scope: ... rutas integridad» no nombra rutas ni criterio de pertenencia; aunque los archivos exactos se delegan a promoción, aquí no hay base para saber qué rutas quedan dentro.

### WS30 [2]
1. Cita: «errores, teclado, dos ventanas y conflictos, con historial». Obliga a inventar qué errores, qué interacciones de teclado y qué «historial» —navegación, diff o tarea— deben probarse, y con qué resultado esperado.
2. Cita: «problemas implican tareas de corrección de la misma capa». Obliga a inventar qué cuenta como «problema» frente a observación, qué es «la misma capa» y si toda observación abre tarea o solo el fallo que bloquea el gate.

### WS31 [3]
1. «actualizar índice/capturas/limitaciones» frente a `output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados`: el índice vive en `borradores/manual.md` (WS10) y no aparece en el scope; obligaría a inventar si se edita el archivo de WS10 o se duplica el índice.
2. «Cada instrucción tiene evidencia vigente»: no define vigencia, formato ni ubicación de la evidencia; obligaría a inventar el criterio de aceptación y dónde registrarlo.
3. «desk/atoms/ vinculados» y «atom->doc verificados»: no enumera átomos ni criterio de vinculación; obligaría a inventar qué conocimiento durable crear y cómo mapearlo.

### WS32 [2]
1. «Refinar ticket existente, sin segundo pipeline» — no se nombra el ticket existente (ID, ruta o Board). Obligaría a inventar cuál es el ticket receptor en `deskops`/`scion` y si ya cubre identidad de intento, dispatch, manifiesto y cierre.

2. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: [WS05, WS12, WS32.1, WS32.2]` — WS06 no figura como dependencia. Obligaría a inventar si WS06 debe preceder obligatoriamente o si la frase es solo una restricción de promoción.

### WS32.1 [4]
1. «schema mediante SLDB»: no identifica qué schema, qué operación ni quién lo produce/verifica en sldb; output_scope solo enumera archivos de deskops. Obligaría a inventar el cambio de schema y su repo.
2. «dispatch intent y confirmed separados»: no define qué son intent y confirmed (¿estados, registros, payloads?) ni su relación con «intento»; obligaría a inventar el modelo y los campos.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06»: depends_on solo incluye WS05 y WS12; obligaría a inventar si WS06 es prerrequisito ejecutable y cuándo se satisface la condición.
4. «Refinar ticket existente»: no nombra el ticket, su repo ni su estado; obligaría a inventar cuál es y qué partes se reutilizan o sustituyen.

### WS32.2 [3]
1. «acceptance: G_CLOSEOUT pasa» — G_CLOSEOUT figura a la vez en `requires` y en la aceptación, con `state: blocked` y `resolver: external`. Si debe estar satisfecho para ejecutar, no puede ser criterio de salida del nodo; si el nodo debe hacerlo pasar, contradice al resolver externo. Obliga a inventar si el ejecutor consume o produce evidencia de ese gate.
2. «Manifiesto, RunDoc y cierre consistentes e idempotentes» — «manifiesto» no aparece definido en brief.md, alcance.md, decisiones.md ni en el alcance de WS05. Obliga a inventar qué artefacto es, su contrato y su ubicación.
3. «sobre el intento correcto» y «sin duplicar» — no se define qué identifica el intento correcto para el cierre ni qué constituye duplicación de evidencia. WS32.1 solo exige identidades distintas entre intentos, no una regla de selección. Obliga a inventar la clave de identidad y el criterio de no duplicación.

### WS33 [2]
1. **Dependencia WS06 ausente.** Cita: «`integration_mode: delta_or_existing_ticket_only_after_WS06; never_parallel_duplicate`». WS06 no figura en `depends_on`, que solo lista WS32, WS11 y los hijos. Obligaría al ejecutor a inventar si WS06 es prerrequisito real, si basta una comprobación posterior o si la condición es meramente informativa.

2. **Actor de la revisión humana sin fuente definida.** Cita: «Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita». El nodo exige registrar una decisión humana, pero no nombra quién la emite, cómo se identifica ni qué evidencia la respalda. Obligaría a inventar identidad, autenticación y formato de registro, o a decidir que basta un campo libre.

### WS33.1 [2]
1. «Referencias Hub/proyecto/conversación/mensaje/intento y resultados, con deduplicación y procedencia». No define la clave de deduplicación. Obliga a inventar qué combinación identifica un registro y qué constituye duplicado; la aceptación solo exige que «una importación repetida no duplica», sin fijar el criterio.
2. «una importación repetida no duplica ni atribuye una conversación completa a un intento». No define «conversación completa» ni «resultados». Obliga a inventar si se refiere a todos los mensajes, a un rango o a otro artefacto, y qué resultado cuenta como vinculable; sin ello la aceptación no es plenamente comprobable.

### WS33.2 [3]
1. «distinguir completado, validado, aprobado y cerrado» frente a una aceptación que solo exige «Una decisión humana queda registrada con actor y referencia al intento». No define valores, transiciones ni aceptación para validado/cerrado; obliga a inventar el modelo de estados y sus pruebas. Si «cerrado» implica closeout, además faltan G_CLOSEOUT/WS27–28; si es solo etiqueta, debe precisarse.
2. «Revisión humana explícita» frente a «Una decisión humana queda registrada»: no aclara si se persiste una revisión-eventO o una decisión-resultado. Obliga a inventar la entidad y qué cuenta como decisión.
3. «completed del agente nunca se registra como aprobado»: no indica de dónde se obtiene `completed` ni cómo se identifica. Obliga a inventar el origen y mapeo de ese estado.

### WS34 [0]
ninguna.

### WS34.1 [3]
1. **“con confirmación, identidad de intento, timeout/errores y autoridad del coordinador”** (scope): no se especifica quién confirma ni por qué canal —humano, CLI o coordinador— ni qué autoridad concreta del coordinador debe verificarse. El ejecutor tendría que inventar el actor y el mecanismo; WS12 produce “policy coordinador”, pero el nodo no remite a un contrato concreto.
2. **“agente real demuestra aceptación y fallo”** (acceptance): “fallo” no define escenario ni evidencia exigida —rechazo, timeout, error de transporte—. Sin precisar el caso negativo, la aceptación no es comprobable sin inventar qué fallo demostrar.
3. **“timeout/errores”** (scope): no hay valores, taxonomía ni criterio de aceptación para timeouts/errores; el ejecutor debe inventar umbrales y clases de error.

### WS34.2 [0]
Ninguna.

La identidad del intento remite a WS33; la autoridad del coordinador y la whitelist, a WS12/G_WRITE_CONTRACT; la API pública, a G_SCION/WS44; y la aceptación es comprobable mediante agente real. El timeout y los errores quedan como detalle de implementación, no como resultado indefinido.

### WS35 [4]
1. «Intento correcto, enlaces origen, evidencia legible» — «Intento correcto» no define qué hace correcto a un intento (campos obligatorios, correspondencia con fuente, estados). Obligaría a inventar el criterio de corrección.
2. «enlaces origen» — no especifica destino del enlace (documento, tarea, mensaje, intento, commit). Obligaría a inventar qué se enlaza y desde dónde.
3. «evidencia legible» — no fija formato ni umbral de legibilidad. Obligaría a inventar la comprobación.
4. «Lectura tarea-intento-conversación-resultados-decisión usando fuente dueña» — «tarea» no aparece en el scope de WS33 («Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita») ni en el de WS27 («Diff Git y artefactos de evidencia junto al encargo»); «fuente dueña» tampoco identifica repo/API por entidad. Obligaría a inventar el proveedor de «tarea» y la autoridad de cada lectura.

### WS36 [3]
1. `output_scope: frontends/mindmap/views/workspace/execution/; endpoints; tests/` — "endpoints" no dice qué endpoints, en qué repo ni quién los posee. WS34 declara el adaptador público en `deskops` y el scope de WS36 solo dice "Invocar solo adaptador autorizado". Obligaría a inventar si WS36 crea endpoints en `graph_ui`, excediendo el alcance o duplicando WS34.
2. `scope: Invocar solo adaptador autorizado para dispatch/reply y solicitud de decisión` — la "solicitud de decisión" no aparece en el scope/acceptance de WS34 (que cubre dispatch/reply, confirmación, timeout/errores). Obligaría a inventar el contrato/endpoint de decisión o a decidir por cuenta propia si se muestra como no soportado; falta dependencia o contrato (posible WS33/WS12).
3. `acceptance: ... ausencia de API/permisos visible` — no define dónde/como se comprueba esa visibilidad (estado UI, test, log). Obligaría a inventar el criterio de evidencia para un estado de error.

### WS37 [1]
1. **“cierre vía autoridad, con actor humano”**
   - Cita: *“cierre vía autoridad, con actor humano”*.
   - Qué obligaría a inventar: el canal concreto de cierre —CLI Deskops, coordinador, commit externo— y el artefacto que demuestra el cierre. Las fuentes remiten a handoff externo y a P05/P06, aún pendientes; el nodo no nombra operación ni evidencia específica. No se pide resolver P05/P06; se señala que el guion de WS37 debe decir qué se ejecutará y cómo se comprobará sin decidir la política.

### WS38 [3]
1. **«mantención de contratos y autorización documentadas»**: no identifica qué contratos ni qué autorización deben documentarse —¿la evidencia de `G_HUMAN_DELEGATE`, contratos de API, política de escritura?—. Obligaría a inventar la lista de contratos y el criterio de autorización exigible.
2. **«instrucciones runtime y revisión trazable»**: no concreta qué superficies, operaciones ni artefacto de trazabilidad cubren las instrucciones. Aunque WS37 aporta el acta, el ejecutor tendría que inventar qué operaciones documentar y cómo registrar la trazabilidad.
3. **«con lo que funciona y fallos demostrados»**: no define qué fallos deben publicarse ni su fuente exacta dentro de la evidencia de WS37. Obligaría a inventar el inventario y el nivel de detalle de fallos.

### WS39 [5]
1. **«usar draft/validate/promote del dueño»** — no se identifica qué repo/API es «el dueño» de esas operaciones ni dónde están documentadas. Obligaría a inventar el actor o el canal concreto.

2. **«UF09 inspección y mutación en store temporal»** — no se define qué store temporal, quién lo provee ni dónde vive; `output_scope` no lo incluye. Obligaría a inventar el entorno de prueba.

3. **«G_HUMAN_MODEL debe pasar antes de marcar capítulo disponible»** — «capítulo» no está definido en las fuentes suministradas. Obligaría a inventar qué unidad se declara disponible y con qué criterio.

4. **«confirmar efectos de contrato y errores»** — no precisa qué efectos ni qué errores se comprueban; aunque WS12 produce el contrato, no se delimita la comprobación esperada. Obligaría a inventar el umbral de aceptación técnica.

5. **Evidencia en `runs/.../acta.md` frente a `output_scope: shell/dialogs.js; views/models/; tests/`** — el acta exigida queda fuera del alcance declarado. Obligaría a decidir si se escribe fuera de `output_scope` o si este debe ampliarse.

### WS40 [4]
1. «Aceptar opcionalmente plantillas de navegación WS17.» WS17 depende de WS40 y produce `ejemplo/nav/`. El ejecutor debe inventar si WS40 espera plantillas inexistentes, las ignora o se bloquea; contradice el orden prerrequisito→dependiente.
2. «registra datos/commits/roots». No se define si son commits Git reales en los repos temporales (identidad, mensajes) o metadatos del manifiesto; obliga a inventar el criterio de aceptación.
3. «los paths se devuelven como manifiesto». Falta formato, campos y destino del manifiesto; el ejecutor debe inventar su esquema para que sea comprobable.
4. «entrada mínima ecosistema/proyecto con enlaces al Board/FAQ/conocimiento reales creados». «Reales» puede significar artefactos del corpus temporal o del deskops real; junto con «nunca toca desk real», obliga a decidir el alcance de esos enlaces.

### WS41 [3]
1. «links ida/vuelta»: no define si son enlaces authored entre documentos/desks o retorno de navegación/historia. WS40 solo garantiza segundo desk y manifiesto. Obligaría a inventar si WS41 debe crear enlaces en el corpus —fuera de su `output_scope`— o solo probar la vuelta.
2. «endpoints de lectura por store» frente a «usando APIs públicas de stores»: no aclara si debe crear endpoints nuevos en `graph_ui` o solo consumir APIs existentes. Obligaría a inventar superficie API y alcance de tests.
3. «errores de acceso»: no concreta taxonomía ni presentación esperada. Obligaría a inventar qué casos son error de acceso y cómo se comprueban.

### WS42 [2]
1. **«endpoints whitelist»** (output_scope). No queda claro si WS42 produce una whitelist propia o consume la que define WS12 («WS12 produce la whitelist final»). Obligaría a inventar el artefacto, su autoridad y su relación con el contrato de WS12.

2. **«con confirmación de alcance y procedencia»** (scope). No indica quién confirma —¿persona solicitante, WS12, WS30?— ni qué evidencia o criterio la hace válida. Obligaría a inventar actor y comprobación de aceptación.

### WS43 [4]
1. **Dependencia no declarada.** «mapa de ecosistema/índices según P09 y WS11» cita WS11, pero `depends_on` solo incluye WS17 y WS30. Obliga a inventar si WS11 debe estar terminado, dónde están sus artefactos y qué hacer si faltan.
2. **Contrato y modelo indeterminados.** «P09 y contrato fijan ubicación/modelo opcional» no identifica qué contrato ni qué «modelo»; P09 sigue pendiente. Obliga a inventar formato, ubicación y contrato aplicable.
3. **Commit sin actor ni canal.** «acta … y commit» no define quién commitea, en qué rama ni con qué autoridad; P05 propone que guardar no commitea y el closeout es externo. Obliga a inventar la operación de commit.
4. **Repos conocidos no enumerados.** «Enlazar repos conocidos por identidad/origen y su entrada existente» no fija el conjunto ni qué constituye «proyecto adicional». Obliga a inventar el inventario a enlazar.

### WS44 [3]
1. **Quién confirma el permiso de acceso read-only.** Citas: «con acceso ya autorizado»; «appoint responsible operator and confirm read-only permission before probe»; y en WS07: «no requiere configurar/ejecutar Scion ni concede permiso G_EXEC». El nodo no nombra al actor que confirma ese acceso. Obligaría a inventar si basta la designación de P01, si el operador se autoconfirma o si hace falta acta del solicitante.
2. **Qué capabilities mínimas cuentan como comprobadas para intento y mensajes.** Citas: «verifica capacidades/identidad necesarias para intento y mensajes»; «identidad/fecha/capabilities». WS05 inventaría la API, pero WS44 no define el conjunto mínimo ni el umbral de respuesta válida. Obligaría a inventar qué endpoints/respuestas satisfacen el gate.
3. **Hub/endpoint concreto a probar.** Cita: `G_SCION` exige evidencia con «fecha/Hub/endpoint/identidad/capabilities», pero WS44 no identifica el Hub ni la fuente para resolverlo. Obligaría a inventar si se descubre leyendo configuración existente o si debe indicarlo otro actor.
