### ROOT [0]
Ninguna. La aceptación es comprobable mediante `context_review.py status` y `validate_plan.py --check`; define revisión vigente, disposición guardada y bloqueo explícito. Las decisiones Pxx pendientes no cuentan según la guía y ROOT no exige resolverlas.

### PK01 [0]
ninguna

### PK02 [1]
1. «sin ambigüedad de encargo o bloqueo explícito con responsable» frente a «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa, y entonces esta aceptación no es verdadera; un bloqueo externo con responsable sí la admite». Un hijo bloqueado por ambigüedad propia cumple literalmente «bloqueo explícito con responsable» —la definición exige responsable y dependencia—, pero la frase siguiente lo excluye. Para decidir hay que inventar un discriminador de causa en `disposition.md` o una precedencia no escrita.

### PK03 [0]
ninguna.

### PK04 [3]
1. Cita: «`context_review` del hijo en dag.yaml cuyo hash de input y de contrato coinciden con los actuales». No se define qué campo constituye el «contrato» del hijo ni de dónde se obtiene su hash actual. Obligaría a inventar la fuente y el algoritmo; el script `status` puede resolverlo, pero el encargo no lo declara como definición.
2. Cita: «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa... un bloqueo externo con responsable sí la admite». Ambos casos pueden acabar en `status=blocked` con «responsable y dependencia»; no hay campo ni criterio que distinga la causa. El revisor tendría que inventar cómo clasificar el bloqueo.
3. Cita: «con responsable y dependencia en esa disposition.md». No se define qué identifica a un «responsable» (nombre, rol, designación WS07) ni el formato mínimo. Obligaría a inventar el criterio de aceptación del bloqueo.

### PK05 [3]
1. «hash de input y de contrato coinciden con los actuales»: el input no define qué artefacto es el «contrato» ni cómo se calcula su hash. Obligaría a inventar el objeto y el algoritmo que la sesión coordinadora debe comparar.
2. «disposition.md guardada en su intento»: un hijo puede tener varios intentos; no se indica cuál cuenta (¿el último, cualquiera?). Obligaría a inventar la regla de vigencia entre intentos.
3. «read_only excluye WS20 de la entrega» (decisiones.md) frente a «cada hijo directo tiene revisión vigente»: con P04 en read_only, WS20 sigue listado como hijo, pero se excluye de la entrega. Obligaría a decidir si su revisión sigue siendo exigible para que PK05 sea verdadera.

### PK06 [2]
1. «un bloqueo externo con responsable sí la admite»: no se define qué hace «externo» a un bloqueo frente a la ambigüedad propia del hijo. Obligaría a inventar el criterio de clasificación (¿dependencia ajena, causa técnica, actor externo?) para decidir si PK06 admite el bloqueo.
   Cita: «un bloqueo externo con responsable sí la admite».
2. «cuyo hash de input y de contrato coinciden con los actuales»: no se identifica qué artefacto es el «contrato» del hijo ni quién fija su hash actual; el input remite a `dag.yaml` y a la guía, pero no a un contrato separado por hijo. Obligaría a inventar la fuente de hash.
   Cita: «cuyo hash de input y de contrato coinciden con los actuales».

### PK07 [0]
Ninguna.

La aceptación remite a un comando concreto (`context_review.py status`), define revisión vigente mediante coincidencia de hashes y presencia de `disposition.md`, y distingue bloqueo externo con responsable de ambigüedad sin resolver. No obliga al ejecutor de PK07 a inventar resultado, actor ni criterio de aceptación.

### PK08 [0]
Ninguna.

La aceptación define resultado comprobable (`context_review.py status`, coincidencia de hashes de input y contrato, existencia de `disposition.md`) y distingue bloqueo propio de bloqueo externo con responsable. El alcance enumera los hijos directos. No hay repo o actor ausente para ESTE nodo, porque PK08 no ejecuta y sus hijos son revisados por otros nodos.

### WS01 [3]
1. «Un review barato sin historial reformula el producto solo con brief.md». No define qué debe contener esa reformulación ni qué umbral la hace aceptable; obligaría a inventar criterios de suficiencia (propósito, superficies, recorridos, límites) para decidir si pasa.  
2. «Cada acuerdo de la sección «Encargo y acuerdos explícitos» cita al solicitante». La sección mezcla citas textuales y prosa de autorización; no aclara si «acuerdo» incluye solo blockquotes o también afirmaciones como «Esto autoriza corregir el plan…». Obligaría a inventar la clasificación y la forma de cita.  
3. «cada propuesta del registro Pxx remite a decisiones.md». No precisa si basta un enlace general o hay que enumerar cada Pxx en `brief.md`; obligaría a inventar cobertura y formato de remisión.

### WS02 [3]
1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» y «inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs»: no delimita si «archivo» incluye código fuente, planes, TaskDocs o solo datos runtime, ni la profundidad del inventario. Obliga a inventar el universo inventariable.

2. «Cada fila incluye ubicación (archivo o símbolo de código) y operación expuesta»: para un archivo Markdown o un dato no define qué cuenta como operación expuesta —lectura, comando que lo muta o método de API—. Obliga a inventar el vínculo archivo→operación.

3. «firmas públicas, efectos Git y cierre»: «efectos Git» no especifica qué efectos ni qué comandos entran; con aceptación de estado comprobado, obliga a decidir el alcance de esa comprobación sin ejecutar.

### WS03 [3]
1. «conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar)». No define qué es un «conflicto» (detección, resolución, solapamiento de escrituras) ni qué «límite» (timeout, granularidad, máximo, alcance). El ejecutor tendría que inventar las dimensiones del informe.
2. «referencias, búsquedas y alcance real ViewDoc». «Referencias» puede ser integridad referencial de DB, enlaces documentales o referencias de código; «búsquedas», API full-text, índices o consultas. Sin precisión, el ejecutor inventa qué inventariar y con qué evidencia.
3. «distinguir API comprobada, ausencia y hueco». No fija qué cuenta como comprobación (lectura de código, prueba ejecutada, documentación) ni qué revisión se audita; obliga a inventar el estándar de prueba y el snapshot de referencia.

### WS04 [3]
1. «mapear nodos de este plan a deltas existentes (tarea o entrada del Board de graph_ui, o commit que ya lo implementa)» junto con «Hash = SHA256 del archivo de tarea». Obliga a inventar qué `path` y qué hash corresponden a una entrada de Board sin archivo de tarea o a un commit, porque la regla de hash solo cubre archivos de tarea.

2. «identificar sesiones y solapamientos sin cambiar sus tareas». La aceptación no incluye sesiones ni solapamientos y no define qué cuenta como solapamiento. Obliga a inventar el criterio, la evidencia exigible y si ese inventario forma parte del resultado o es solo contexto.

3. «mapear nodos de este plan a deltas existentes». No acota si son todos los nodos o solo los relacionados con UI/graph_ui; el título dice «UI» pero el alcance no lo limita. Obliga a inventar el subconjunto de nodos que debe mapearse y permite exceder el alcance de `auditoria/ui.md`.

### WS05 [2]
1. «separar slug/agente/intento/dispatch/mensaje/conversación y permisos» frente a una aceptación que solo exige «No usar tablas internas como interfaz; señalar los campos internos… y capacidades que requieren API real». Obligaría a inventar qué matriz o evidencia demuestra la separación completa y si el inventario de permisos forma parte de la aceptación.  
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)» frente a «API pública definida en el scope». Obligaría a inventar la precedencia cuando documentación y exports discrepan, o el criterio para decidir si un símbolo exportado pero auxiliar cuenta como API pública; sin ello, el límite «no funciones internas» no es plenamente operable.

### WS06 [0]
Ninguna.

### WS07 [2]
1. «El humano dueño del producto confirma o corrige P01–P09 de decisiones.md y `baseline_proposal` de dag.yaml» y «decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml». No se define qué es `baseline_proposal`, dónde está ni qué campos tiene. Obligaría a inventar su esquema, su contenido y si confirmarlo equivale a aprobar el plan completo o solo una parte.
2. «| P08 | Uso humano y alcance | Proyecto Taller temporal, participante humano y presupuestos propuestos en validacion-humana.md.» Ese archivo no se suministra ni figura como dependencia de WS07. Obligaría a inventar los presupuestos, el participante y qué se está aprobando exactamente en P08, o a dar por suficiente una referencia que el ejecutor no puede verificar.

### WS08 [0]
Ninguna.

El encargo nombra el resultado, el archivo de salida, la fuente de operaciones (`auditoria/{deskops,infraestructura,ui}.md`, vía WS06/WS07), la regla ante operaciones ausentes y los límites de UF02/UF08. La aceptación es comprobable por UF y el detalle exacto de formato queda para la promoción.

### WS09 [0]
ninguna.

### WS10 [0]
ninguna.

### WS11 [3]
1. «graph/code admiten otros nodos con origen»: no se define qué tipos de nodo admite cada representación ni con qué criterio. Obligaría a inventar una taxonomía de nodos admisibles.
2. «obtener aceptación del delta lector en graph_ui»: el input no delimita qué cambios componen ese “delta lector”. Obligaría a inventar el alcance exacto que el responsable de `graph_ui` debe aceptar.
3. «El acta receptora enumera scope_nodes de G_UI_READ/G_SPEC_VIEW, incluidos corpus WS40 y multidesk WS41»: no queda claro si WS40/WS41 deben constar también en el acta de `spec2viz`; en `dag.yaml#gates` solo figuran bajo `G_UI_READ`. Obligaría a decidir a qué acta pertenecen.

### WS12 [1]
1. «Aceptar deltas de escritura por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable.» No define la unidad de aceptación: ¿un acta global o una por operación/campo? Tampoco aclara si «delta» abarca todas las operaciones de los `scope_nodes` de G_UI_WRITE o solo las incluidas en la whitelist final. G_UI_WRITE fija la evidencia mínima del acta, no su granularidad. Obligaría a inventar el criterio de cierre y qué actas son exigibles.

### WS13 [0]
ninguna.

### WS13.1 [1]
1. La aceptación remite a «la matriz de WS09 y el contrato WS11», mientras `integration_mode` afirma «matriz WS06 llega de forma transitiva por WS11/WS12». Si son matrices distintas, el ejecutor debe inventar cuál define las representaciones soportadas y, por tanto, qué debe probar al alternar texto/graph/code. Cita: «en las representaciones que la matriz de WS09 y el contrato WS11 declaren soportadas».

### WS13.2 [0]
Ninguna. Las frases «según contrato WS11» y «store temporal de prueba» remiten a fuentes suministradas; G_UI_READ pendiente es un gate intencional, no un defecto.

### WS13.3 [3]
1. **Eventos que forman la historia.** Cita: «Cambiar de pestaña o división cambia el documento activo sin alterar el foco guardado de cada documento; volver restaura documento, foco y origen» y «Volver sigue el orden inverso de navegación». No define si cambiar pestaña/división, abrir un documento o seguir un enlace empujan historia; obligaría a inventar qué acciones son navegables.

2. **Efecto de cerrar pestaña.** Cita: «Abrir, cambiar y cerrar pestañas». No indica qué documento queda activo al cerrar la pestaña activa ni si se descartan su foco y su entrada de historia; obligaría a inventar la regla de cierre.

3. **Entrada de apertura y dependencia.** Cita: «Abrir documentos en pestañas y divisiones» con `output_scope` limitado a `layout/`. No nombra desde dónde se abren (enlaces de WS13.1, explorador de WS13.2) ni si WS13.2 es prerrequisito; obligaría a inventar interfaz de apertura o dependencia ausente.

### WS14 [2]
1. «resultados enlazan identidad y contexto». No define qué identidad ni qué contexto deben mostrarse/enlazarse, y la aceptación no lo comprueba. Obliga a inventar campos, enlace y criterio de verificación.
2. «Búsqueda vacía/error/degradación diferenciados» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». «Vacía» puede significar consulta vacía o ausencia de resultados. Obliga a decidir si hay un cuarto estado y cómo probarlo.

### WS15 [0]
ninguna

### WS15.1 [0]
ninguna

### WS15.2 [3]
1. «tras ejecutar init fuera de la UI, refrescar muestra el desk real» / «refrescar lectura»: no se define el disparador ni el mecanismo —recarga manual, botón, relectura automática—. Obliga a inventar cuándo y cómo se refresca y qué cuenta como “refrescar”.
2. «la ruta absoluta del proyecto como destino»: “destino” no se define —¿argumento de `init`, ubicación del futuro desk, texto copiable?—. Obliga a inventar su significado y representación.
3. «un proyecto sin desk muestra orientación»: no se nombra criterio ni fuente de detección; WS11 solo se cita para «rutas de lectura definidas por el contrato WS11». Obliga a inventar cómo se determina la ausencia de desk —sistema de archivos, API, qué artefacto lo define—.

### WS16 [1]
1. **Cita:** «Fallos abren correcciones antes de edición».
   **Qué obligaría a inventar:** el input no identifica quién registra la corrección, en qué repo, con qué formato ni si WS16 debe crearla o solo reportarla. El ejecutor tendría que decidir alcance y destino de esas correcciones.

### WS17 [3]
1. «Resolver dos desks y procedencia»: no define qué significa “resolver” ni cómo se comprueba la procedencia. Obliga al ejecutor a inventar el criterio observable de aceptación (enlace, campo, manifiesto o combinación).
2. «no duplicar registry»: no identifica el registry concreto, su ubicación ni su representación. Obliga a inventar qué artefacto debe evitarse y cómo demostrar que no se duplicó.
3. «Resolver dos desks»: no nombra cuáles dos desks del corpus WS40 son exigibles. Aunque WS40 crea dos repos con desk y un tercero sin desk, el nodo no fija la correspondencia; obliga a inferirla del manifiesto.

### WS18 [1]
1. **«ViewDoc/NotationDoc para selecciones y notación ya soportadas»** (dag.yaml#node:WS18, scope).
   Las fuentes suministradas definen «Proyección de grafo ViewDoc» en el glosario, pero no definen **NotationDoc**: ni su contrato, ni su formato, ni si es un entregable separado de ViewDoc. El ejecutor tendría que inventar qué artefacto declarar y con qué contenido, y la aceptación no permite comprobar ese objeto por separado.

### WS19 [0]
Ninguna.

### WS19.1 [2]
1. «Delta sobre ticket draft de edición». No se identifica el ticket/Board receptor concreto; obligaría a inventar cuál es el ticket existente y su alcance exacto, pese a que `integration_mode` alude a un ticket draft.
2. «conflicto visible (mensaje de rechazo con el texto local conservado)» frente a la aceptación «una escritura obsoleta no pierde texto local». La aceptación no exige comprobar que el conflicto sea visible; obligaría a inventar el criterio de visibilidad y la evidencia que lo demuestra (sin fijar aquí textos de pantalla).

### WS19.2 [0]
ninguna.

### WS20 [0]
ninguna. Los campos protegidos, el canal/API, los fallos parciales y la revisión quedan fijados por WS12/`G_WRITE_CONTRACT`; `source_mode` por P04/WS07; archivos y escenarios finos por el TaskDoc de promoción.

### WS21 [0]
Ninguna.

### WS22 [2]
1. **“Representar Board real como lista, como tablero y con dependencias”** frente a una aceptación que solo exige: **“Selección y links comunes con lector; estados y gates leídos de deskops (Board, lifecycle), no de dag.yaml; no duplicar tareas…”**. No queda claro si las tres representaciones son obligatorias ni cómo se comprueban; obligaría a inventar si basta una o si deben entregarse todas y con qué evidencia.
2. **“como tablero y con dependencias”** no define qué agrupación usa el tablero ni qué dependencias deben mostrarse (¿`depends_on`, gates, solapamiento de archivos?). Obligaría a inventar el modelo de representación y su fuente.

### WS23 [2]
1. «pasos, transiciones y fuentes navegables» frente a «El estado de un paso solo viene de deskops; esta vista no lo escribe.» No aclara si las transiciones son solo representadas o también accionables (por ejemplo, avanzar un paso). Obligaría a inventar si existe mutación, qué contrato/permiso la habilita y qué ocurre al activar una transición.

2. «RitualDoc/StepDoc/lifecycle sobre referencias reales» y «Un procedimiento abre sus documentos y soporte». No nombra el inventario o API que provee los rituales ni el criterio para seleccionar el procedimiento mostrado; «referencias reales» no fija su resolución ni el comportamiento si una referencia falta. Obligaría a inventar la fuente de datos, el conjunto mostrable y el tratamiento del hueco.

### WS24 [4]
1. «crossroads (CrossroadDoc del árbol de dominio)»: “CrossroadDoc” y “árbol de dominio” no se definen en brief/glosario ni en alcance. Obligaría a inventar qué entidad es, de dónde se obtiene y cómo se representa.
2. «materializaciones»: se enumera como clase a mostrar, pero no hay definición ni contrato de origen en las fuentes. Obligaría a inventar su identificación y procedencia.
3. «Clasificación = tipo y tags»: no se define de dónde salen los tags ni su autoridad. Obligaría a decidir si son campos del modelo, del documento o inventados.
4. «Vecindad = 1–2 hops»: el rango no fija si se muestran uno, dos o ambos, ni si es configurable. Obligaría a inventar el comportamiento y el criterio comprobable.

### WS25 [0]
Ninguna. Lo comprobado:

- Resultado definido: `output_scope: 'Agregado: salidas de WS25.1, WS25.2'`, con dos hijos (`Leer inbox y registrar ack o respuesta local`, `Capturar en drawer o protoátomo`) que cubren el alcance del agregado.
- Aceptación comprobable: agregado no ejecutable, resuelto por aceptación de cada hijo.
- Repo y actor presentes: `owner_repo: graph_ui`.
- Dependencias coherentes: WS12 (contrato de operaciones) y WS16 (validación humana de lectura); los hijos como cierre del agregado.
- Gates explícitos y pendientes: `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.
- Límite claro: ack no equivale a aprobación; respuesta solo si el contrato WS12 la define.

No se computan como ambigüedad las Pxx pendientes ni los detalles que fijará el TaskDoc de promoción.

### WS25.1 [0]
Ninguna.

### WS25.2 [1]
1. «ambos tipos se registran y se muestran tras recargar». No queda claro si “ambos tipos” son los destinos —drawer/protoátomo— o los orígenes —ruta/mensaje—. Obligaría a inventar qué matriz debe registrarse y mostrarse, aunque el alcance exige probar cada destino por separado.

### WS26 [0]
Ninguna.

### WS26.1 [0]
ninguna

### WS26.2 [4]
1. «representación de capa lista por dependencias/no solapamiento» frente a una aceptación que solo exige «Tras enrutar, `deskops show board` muestra la tarea». Falta criterio comprobable de la capa lista; obligaría a inventar su verificación y prueba.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc» no define qué ocurre con `files` vacíos o ausentes, ni si el solapamiento es por ruta exacta, prefijo o directorio. Obligaría a inventar la regla.
3. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real» no aclaran si WS26.2 implementa promoción o solo prepara handoff, ni cómo se comprueba «estado real». Obligaría a inventar alcance y evidencia.
4. «dependencias pendientes» remite al «ritual de fase», pero no se aporta qué estados cuentan como pendientes ni cómo mapearlos desde deskops. Obligaría a inventar esa semántica.

### WS27 [0]
ninguna.

El alcance, la aceptación agregada, el repo y las dependencias están definidos; la guía aclara que un `aggregate` no se ejecuta y que un gate pendiente es intencional.

### WS27.1 [6]
1. «sin ejecutar ni revertir nada» frente a «Diff real e historial read-only»: prohibir "ejecutar" literalmente impide invocar Git para obtener el diff. Obligaría a inventar qué invocaciones de lectura están permitidas y por qué canal.

2. «Diff real e historial read-only acotados al repo y tarea»: no define extensión del historial (rango, profundidad, filtro por rutas, renames). Obligaría a inventar sus límites.

3. «Base: commits listados en TaskDoc.references»: no indica cómo distinguir commits de otras referencias (documentos, URLs) ni qué hacer con hashes inexistentes o clones shallow. Obligaría a inventar filtro y comportamiento de fallo.

4. «Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado»: falta la regla ruta→repo y dónde se declara el repo. Obligaría a inventar resolución y fuente de declaración.

5. «working tree contra HEAD limitado a esas rutas»: sin regla para archivos no rastreados ni repos sin HEAD. Obligaría a inventar inclusión y degradación.

6. «junto a la TaskDoc»: `depends_on` solo nombra WS13/WS12; ningún nodo listado garantiza el panel TaskDoc donde montar. Obligaría a inventar el punto de montaje o asumir una vista existente.

### WS27.2 [2]
1. «Declarada = closeout_evidence de la TaskDoc; encontrada = artefactos resolubles en las references/files de la TaskDoc; verificada = resultado de `deskops closeout verify`». Obliga a inventar la regla de correspondencia entre una evidencia declarada y un artefacto encontrado —ruta, identificador, nombre u orden— y si los estados son por evidencia o del conjunto. Sin esa regla no puede decidirse «declarada sin artefacto», «artefacto no declarado» ni atribuir una verificación fallida.
2. «una evidencia ausente se ve como ausente; declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos». Obliga a inventar si «ausente» es un cuarto estado —sin evidencia declarada— o el mismo caso de «declarada sin artefacto». La aceptación no fija esa taxonomía ni el caso vacío.

### WS28 [2]
1. «diagnosticar faltantes y ofrecer handoff explícito con evidencia». La aceptación solo exige que `deskops show task` y el commit de closeout confirmen el cierre; no define qué cuenta como “faltante”, qué artefacto produce el diagnóstico ni cómo se comprueba. Obligaría a inventar el criterio de diagnóstico y su salida verificable.
2. «y refrescar estado». No identifica qué estado debe refrescarse, qué lo dispara ni quién lo verifica. Obligaría a decidir si el refresco es automático o manual y cómo demostrarlo en la aceptación.

### WS29 [2]
1. **Canal de obtención de hallazgos no definido.** Cita: «stores check/doctor/drift y relaciones comprobadas; errores = hallazgos de esos tres comandos». Obligaría a inventar si la vista ejecuta los comandos, consume una API o solo lee resultados ya producidos; la aceptación solo exige enlazar al comando documentado para reparar.

2. **Atribución y filtro de errores al documento afectado.** Cita: «muestra documento afectado, relaciones alcanzadas [...] y errores» junto a «agrupados por comando». Obligaría a inventar si se muestran todos los hallazgos de los tres comandos o solo los atribuibles al documento y relaciones alcanzadas.

### WS30 [1]
1. **Dependencia ausente para el guion.** Cita: «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS30 no incluye WS08 en `depends_on` y no se deduce de sus dependencias listadas. Obliga a inventar el guion, asumir que WS08 ya lo produjo o decidir si basta `validacion-humana.md`.

### WS31 [3]
1. «Cada instrucción remite al acta de WS30 o al acta de publicación de WS43 de la versión publicada»: no fija qué acta acredita cada instrucción. WS30 valida el manual en graph_ui/Taller y WS43 publica el deskops real; obligaría a inventar la correspondencia y si una instrucción sobre el desk real puede apoyarse solo en WS30.
2. «Scion solo capítulo marcado propuesto hasta WS38.»: no dice si WS31 debe incluir un capítulo Scion propuesto o puede omitirlo, ni su contenido mínimo; obligaría a inventar su existencia y cobertura.
3. «incorporar el índice de borradores/manual.md, capturas y limitaciones» frente a «etiquetas, links y atom->doc verificados»: la aceptación no fija qué capturas incluir ni cómo comprobar que son reales y de la versión publicada; obligaría a inventar el conjunto y su evidencia.

### WS32 [0]
Ninguna. La aceptación del agregado queda definida por la aceptación de sus hijos; las identidades, el manifiesto y la idempotencia están acotados en WS32.1/WS32.2. Los gates pendientes tienen productor nombrado y no obligan a inventar sustituto.

### WS32.1 [0]
ninguna.

### WS32.2 [3]
1. «manifiesto, RunDoc e índice de cierre coinciden en id de intento, hash de sesión y evidencia». El «hash de sesión» no aparece entre los campos mínimos del manifiesto ni se define su origen. Obliga a inventar qué sesión se hashea, cómo se obtiene y cómo se compara.
2. «índice de cierre» aparece en aceptación, mientras el scope habla de «registros de closeout». Obliga a inventar si es un artefacto distinto, su formato, ubicación y dueño.
3. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos». No define qué ocurre si la repetición trae evidencia o commit de cierre distintos. Obliga a inventar si se rechaza, se conserva lo primero o se sobrescribe.

### WS33 [0]
ninguna.

Las referencias a Hub/proyecto/conversación/mensaje, al identificador de la fuente y a la decisión humana quedan delegadas a WS33.1/WS33.2 y al contrato G_SCION producido por WS44; no obligan al ejecutor de este agregado a inventar resultado, repo ni aceptación.

### WS33.1 [2]
1. «una importación repetida (mismo Hub/proyecto y conversación, con checkpoint)». No se define qué es el checkpoint ni quién lo emite. Obligaría a inventar cómo se simula o reanuda y qué evidencia demuestra la idempotencia; la aceptación deja de ser comprobable sin esa decisión.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente ... con la misma regla de deduplicación y procedencia». La clave explícita es «Hub + proyecto + id de mensaje»; para resultados no se fija una clave equivalente. Obligaría a inventar si la deduplicación usa Hub+proyecto+intento+id de fuente u otra combinación, y cómo resolver colisiones.

### WS33.2 [3]
1. «Registrar la decisión humana (aprobar o pedir corrección) con actor»: no se nombra el canal ni quién produce la decisión (endpoint de deskops, CLI, payload de Scion u otro). Obliga a inventar interfaz, autorización y validación; `G_SCION` cubre el contrato de Scion, no la captura de la decisión.
2. «con actor»: no se define de dónde sale ni cómo se verifica la identidad del actor. Obliga a inventar si es cadena libre, identidad autenticada o referencia externa, y qué aceptación tendría.
3. «asociada al intento y, por él, a su tarea»: no se explicita quién garantiza el vínculo intento→tarea ni qué ocurre si un intento no resuelve tarea. WS33.1 vincula mensajes/resultados, no esa asociación.

### WS34 [0]
Ninguna. Los puntos que podrían parecerlo están cubiertos por fuentes suministradas: «Autoridad del coordinador según contrato WS12» delega en WS12, que registra hueco y dueño; «Confirmación = respuesta de la API de Scion» define el criterio en WS34.1; «la API que fije el contrato WS12» y los textos exactos corresponden a promoción; G_SCION/G_EXEC/G_WRITE_CONTRACT pendientes son intencionales; rutas exactas y archivos los fija el TaskDoc.

### WS34.1 [2]
1. «timeout/errores» y «vencido por timeout»: no fija umbral, política de timeout ni formato de error. WS34.2 sí dice «con el umbral del contrato WS12», pero WS34.1 no lo remite. Obligaría a inventar cuándo vence y cómo se reporta.
2. «identidad de intento»: no indica si la produce Scion, WS33 o el adaptador, ni su formato/unicidad. Aunque depende de WS33, el nodo solo remite expresamente la autoridad del coordinador a WS12 («Autoridad del coordinador según contrato WS12»). Obligaría a inventar fuente y semántica.

### WS34.2 [0]
ninguna.

### WS35 [3]
1. Scope: «Lectura tarea-intento-conversación-resultados-decisión»; acceptance: «Cada mensaje y resultado se muestra bajo su intento; cada uno enlaza a su fuente; la evidencia abre en el lector.» La aceptación no cubre tarea, conversación ni decisión, aunque el scope las incluye. Obligaría a inventar si deben mostrarse, con qué jerarquía y cómo se comprueban.
2. «Cada mensaje y resultado se muestra bajo su intento» presupone que todo mensaje/resultado tiene intento; no define qué hacer con mensajes no ligados a un intento. Obligaría a inventar su agrupación, visibilidad u omisión.
3. «la evidencia abre en el lector» no identifica qué lector ni el contrato de apertura. Obligaría a inventar el destino y la integración.

### WS36 [0]
ninguna

### WS37 [0]
ninguna.

### WS38 [0]
ninguna

### WS39 [0]
ninguna

### WS40 [0]
SIN SECCION: REFORMULACION: Propósito: versionar en graph_ui un generador reproducible del corpus Taller. Resultado: un comando crea/recrea un entorno aislado con dos repos/desks temporales y un tercer repo sin desk, documentos con Markdown no modelado, Code local y referencia rota, commits git reales, instrucci

### WS41 [1]
1. «seguir enlaces authored del corpus entre desks». WS40 es el productor del corpus y de los dos stores, pero su alcance solo menciona Markdown no modelado, Code local, referencia rota y enlaces internos de la entrada mínima; no enumera enlaces authored entre desks. Esto obliga a inventar si WS41 debe crear esos enlaces en `tests/` —invadiendo el corpus— o si WS40 debe ampliarse, y cuál es el enlace exacto que prueba UF08.

### WS42 [3]
1. **«las materializaciones existentes se inspeccionan y validan contra el modelo SLDB vigente»** — no se nombra artefacto, versión, repo ni nodo que produzca ese modelo. Obligaría a inventar cuál es la fuente autoritativa y cómo determinar su vigencia.
2. **«se inspeccionan y validan»** — no define resultado observable ni criterio de validación (¿mostrar, informar, bloquear?) ni qué ocurre si la validación falla. Obligaría a inventar la aceptación concreta de esa parte.
3. **«que ve el alcance y la procedencia antes de ejecutar»** — no fija qué información mínima debe verse ni cómo se comprueba en la aceptación, que no menciona esta confirmación. Obligaría a inventar contenido y verificación.

### WS43 [1]
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» / «Repos a enlazar = todos los de `deskops list repositories`» / aceptación: «un enlace es verificable si resuelve a un path existente del repo enlazado». Si un repo listado carece de «entrada existente» o de path local, no se dice si omitirlo, enlazar su raíz o detenerse; el ejecutor tendría que inventar la excepción.

### WS44 [3]
1. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33.» WS05 produce ese inventario, pero su contrato solo obliga a señalar «capacidades que requieren API real», no a mapearlas como requeridas por WS32/WS33. Si faltan, WS44 tendría que inventar qué capabilities probar y para qué nodo.
2. «El solicitante registra en WS07 qué acceso read-only tiene el operador.» WS07 exige designar identidad/fecha del operador y declara que «no concede permiso G_EXEC», pero no obliga a registrar el nivel de acceso read-only. WS44 tendría que inventar si el acceso está autorizado y con qué alcance.
3. «verifica capacidades/identidad necesarias para intento y mensajes» / «identidad/fecha/capabilities y actor registrados». No se define si «identidad» es la del operador, el Hub/tenant, el agente remitente o el principal de API; el ejecutor tendría que elegir cuál evidenciar.
