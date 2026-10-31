### PK02 [0]
ninguna.

La aceptación define revisión vigente por hash de input/contrato y `disposition.md` guardada, y distingue bloqueo externo con responsable de ambigüedad propia del hijo. Las decisiones Pxx pendientes no cuentan como ambigüedad de PK02.

### PK03 [0]
ninguna

### PK04 [0]
ninguna.

### PK05 [0]
Ninguna.

### PK06 [0]
ninguna.

La aceptación define el criterio y lo delega a `context_review.py status`; no exige al ejecutor inventar hashes, disposiciones ni responsables.

### PK07 [0]
ninguna.

La aceptación es mecánica y comprobable mediante el comando indicado. La distinción entre ambigüedad propia del hijo y bloqueo externo con responsable está explicitada. Los detalles de hash y `disposition.md` quedan delegados a `context_review.py`, no al ejecutor de PK07.

### PK08 [0]
ninguna.

### WS05 [3]
1. «marca qué capabilities requieren WS32 y WS33». El input no incluye alcance ni aceptación de WS33; el ejecutor tendría que inventar qué necesidades tiene WS33 y qué capabilities marcar.
2. «señalar los campos internos que no figuren en la API pública definida en el scope». El scope dice «API pública de Scion (endpoints/SDK documentados o exportados...)», pero no fija versión ni prevalencia entre documentación y SDK exportado; si discrepan o están incompletos, el ejecutor debe inventar el criterio de qué es interfaz pública.
3. «separar slug/agente/intento/dispatch/mensaje/conversación». El glosario suministrado define “intento”, pero no define slug, dispatch ni conversación; si la API no los etiqueta, el ejecutor tendría que inventar sus equivalencias.

### WS07 [3]
1. «output_scope: decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml» frente a «leyendo ... `baseline_proposal` de dag.yaml». El input no define `baseline_proposal` ni aclara si WS07 debe modificarlo o solo leerlo. Obliga a inventar su contenido y si entra en el cierre.
2. «reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí». No se indican las variantes concretas ni dónde registrar esa reconsideración. Obliga a inventar el artefacto y el alcance del ajuste.
3. «registrar qué acceso read-only tiene» el operador Scion frente a «No cerrar sin registro de designación de responsables ... y operador Scion en P01». La aceptación solo exige identidad, no el nivel de acceso que el scope pide registrar. Obliga a inventar si el acceso debe constar y cómo se verifica.

### WS08 [4]
1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: UF03/UF04/UF05 agrupan varios pasos con operaciones distintas; obligaría a inventar si se documenta una fila por UF o una por paso.
2. «nodo y gate humano» en singular: `cobertura.md` asigna varios («WS22/26», «WS16 diagnóstico; prueba propia WS29»); obligaría a inventar si se elige uno o se listan todos.
3. «cubrir manual»: no existe UF de manual en `user-flows.md`; obligaría a inventar un flujo nuevo o a reinterpretar UF05.
4. «Nodo = ID del DAG»: no aclara si es el nodo de implementación o el de validación; el campo separado «gate humano» sugiere lo primero, pero no lo fija.

### WS09 [1]
1. «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)».  
   Obliga a decidir si «estado» mide madurez de implementación en la UI o publicación/verificación en el manual. WS10 define las etiquetas para el manual y WS04 aporta disponibilidad actual; sin una regla de precedencia, el ejecutor debe inventar la correspondencia entre ambos ejes y podría producir una aceptación no comprobable.

### WS10 [0]
ninguna.

### WS11 [4]
1. «Un documento Markdown mantiene identidad/ruta/modelo opcional». No se define qué compone la identidad —ruta, ID estable, hash o clave por store— ni cómo se resuelve entre repos. Obligaría a inventar la semántica de identidad que luego WS13.1 debe mostrar y WS41 usar en multidesk.
2. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer». Solo se definen instancia y vínculo; no hay criterio para distinguir consulta, API y renderer. Obligaría a inventar la taxonomía y, con ella, cuándo un hueco genera una dependencia nueva.
3. «si falta API abrir dependencia acotada del repo dueño antes de code». No se fija qué hace “acotada” ni cómo identificar al dueño si la API faltante no pertenece a un repo ya nombrado. Obligaría a inventar alcance y propietario de la dependencia.
4. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk». WS41 exige aliases/roots «explícitamente autorizados en contrato WS11», pero no se indica quién autoriza, con qué formato ni qué límites. Obligaría a inventar la política de autorización multidesk.

### WS12 [0]
ninguna.

### WS13 [0]
ninguna.

### WS14 [3]
1. «Sin resultados/error/degradación diferenciados.» Esta frase del scope puede leerse como que esos estados no deben diferenciarse, mientras la aceptación exige que «se ven como tres estados distintos». Obligaría a decidir si el scope niega o enumera los tres estados.
2. «resultados abren el documento con su identidad y ruta de origen» no se comprueba en la aceptación, que solo exige abrir/volver y conservar consulta/foco. Obligaría a inventar dónde se muestran identidad y ruta, o si basta con abrir el documento.
3. «no cargar todo grafo en cada tecla» no fija umbral ni forma de comprobación. Obligaría a inventar qué cuenta como “todo grafo” y cómo demostrar que no se carga en cada pulsación.

### WS15 [0]
Ninguna.

### WS16 [0]
ninguna

### WS17 [3]
1. «Mostrar el root/store de procedencia al resolver los dos desks del manifiesto WS40». No aclara si “mostrar” exige contenido concreto en las plantillas —formato, ubicación— o una comprobación/acta de aceptación. Obligaría a inventar el artefacto y podría exceder `documentation` hacia UI/renderer.
2. «recorrer links Markdown sin UI». No fija criterio ni método: ¿todos los enlaces deben resolver?, ¿solo los de los dos desks?, ¿inspección manual o script? El ejecutor tendría que inventar el umbral comprobable.
3. «source versionado y destino temporal no son registros independientes». No define observación verificable —identidad de contenido, ausencia de duplicados, hash—; obligaría a inventar cómo demostrarlo.

### WS18 [0]
Ninguna.

### WS19 [1]
1. **`kind: implementation` frente a `node_role: aggregate` y “Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.”** El nodo declara naturaleza de implementación y estimación M, pero su aceptación lo declara no ejecutable. Esto obliga al ejecutor a inventar si WS19 produce artefactos propios (código, tests, evidencia) o solo coordina a sus hijos; una lectura literal de `kind` podría exceder el alcance agregado.

### WS19.1 [0]
ninguna

### WS19.2 [0]
ninguna

### WS22 [4]
1. «como tablero agrupado por estado y con las dependencias declaradas en el TaskDoc» — la tercera representación no define qué muestra (aristas, dirección, profundidad, agrupación, layout). Obligaría a inventar el diseño de la vista de dependencias; la aceptación solo exige que abra el mismo TaskDoc.
2. «abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados» — no se define qué cuenta como átomo referenciado por un TaskDoc ni cómo resolverlo. Obligaría a inventar el criterio de vinculación. (La guía excluye pills; no el criterio de átomos.)
3. «no duplicar tareas» — con tres representaciones simultáneas del mismo Board, no queda claro si prohíbe repetir una tarea entre lista y tablero o solo crear registros duplicados. Obligaría a decidir cuál de las dos lecturas aplicar.
4. «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml» — no se nombra qué canal/API las expone ni quién lo garantiza; `depends_on` solo incluye WS09 (que inventaría Board/ritual) y WS13. Obligaría a inventar la fuente o asumir disponibilidad.

### WS23 [0]
Ninguna. Los términos RitualDoc/StepDoc/lifecycle están glosados en brief.md; origen, contrato, renderer, error y estado de la fila de ritual corresponden a WS09; la falta de contrato o permiso se resuelve con la regla común de alcance.md; `G_UI_READ` pendiente es estado intencional, no defecto.

### WS24 [3]
1. **Clasificación en soportes no modelados.** Cita: «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» y «La vista muestra la clasificación (tipo y tags)». No se define qué mostrar para Markdown sin modelo ni de dónde salen los tags si el modelo no los declara. Obliga a inventar si se muestran vacíos, se omiten o se leen del frontmatter.

2. **Uso concreto de WS18.** Cita: «Reutilizar el gráfico actual y una vista de documento genérica única registrada en shell/registry.js» junto con `depends_on: WS18`. El nodo no dice qué salida de WS18 consume —ViewDoc o NotationDoc— ni cómo condiciona el grafo o la vista. Obliga a inventar la integración o a ignorar la dependencia.

3. **Ubicación del soporte no modelado.** Cita: «un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista con su ruta de origen». No precisa si «la vista» es el grafo local o la vista de documento genérica. Obliga a inventar dónde debe aparecer y qué aceptación se prueba.

### WS25 [0]
ninguna.

### WS25.1 [0]
Ninguna.

La eventual “respuesta local” queda condicionada por el contrato WS12 y su ausencia tiene salida explícita: “si no se declara no disponible”. El source del inbox, permisos concretos y endpoints quedan delegados al contrato/dependencia, no al ejecutor.

### WS25.2 [2]
1. «destino elegido explícitamente por la persona usuaria» no se refleja en «una captura persiste tras recargar con origen...». Falta criterio para comprobar la elección explícita o rechazar un destino por defecto; obligaría a inventar cómo se evidencia y si un default cumple.
2. «cada destino se prueba por separado» no se concreta en la aceptación, que habla de «una captura». Obligaría a inventar si drawer y protoátomo deben pasar ambos persistencia/origen tras recarga o si basta uno, y qué resultado distinto se espera.

### WS26 [0]
Ninguna.

El agregado no ejecuta: su aceptación remite a los hijos y su alcance queda cubierto por WS26.1/WS26.2. La frase «promoción solo cuando el contrato resuelve commits previos por canal autorizado» identifica el contrato en WS12 (whitelist/capabilities) y G_CLOSEOUT; no obliga a inventar otro. «El canal de promoción debe respetar commits previos y estado real» es criterio operativo delegado a WS12 y a la aceptación de WS26.2, no resultado indefinido para este nodo. La dependencia de WS26 respecto de sus propios hijos es coherente con la semántica de agregado indicada en la guía.

### WS26.1 [0]
ninguna

### WS26.2 [2]
1. «sin archivos solapados según los `files` declarados en cada TaskDoc» y «archivos solapados» en acceptance. No se define contra qué conjunto se compara el solapamiento: otras tareas de la capa lista, tareas en ejecución, todo el Board o tareas futuras. Obliga a inventar el criterio de exclusión y, por tanto, el resultado de «capa lista».
2. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real». No queda claro si WS26.2 debe implementar una acción/UI de promoción o solo enrutar y declarar handoff; «estado real» no se define. Obliga a inventar alcance y aceptación observable.

### WS29 [1]
1. «muestra documento afectado, relaciones alcanzadas (...) y errores. (...) errores = hallazgos de esos tres comandos, agrupados por comando». No se especifica si deben mostrarse **todos** los hallazgos o solo los asociados al documento afectado. El ejecutor tendría que inventar el criterio de filtrado y el alcance de la lista de errores.

### WS30 [1]
1. Cita: «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». `WS08` no figura en `depends_on` de WS30 y `validacion-humana.md` no fija el guion de teclado; esto obligaría a inventar esos escenarios o a suponer una dependencia no declarada.

### WS31 [0]
Ninguna.

### WS32 [0]
Ninguna.

El agregado tiene aceptación comprobable por estado de hijos; repo, límites y gates están nombrados; las dependencias directas e indirectas son coherentes. La posible redundancia de WS05/WS12 en `depends_on` no obliga a inventar ni altera la aceptación del agregado.

### WS32.1 [3]
1. «confirmed desconocido hasta reconciliar»: no define quién reconcilia, con qué evidencia ni estado final; obliga a inventar el proceso y la aceptación del timeout.  
2. «ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico»: no aclara si WS32.1 crea el registro o solo escribe hechos que WS32.2 materializa; obliga a inventar el límite de salida frente a WS32.2.  
3. «Dos intentos del mismo agente y un dispatch fallido»: no precisa si el fallido es uno de esos dos o un tercer caso; obliga a inventar cardinalidad y evidencia esperada.

### WS32.2 [3]
1. «hash de sesión» — no se define qué sesión ni cómo se calcula (¿id de sesión de la API Scion, del RunDoc, derivado localmente?). El ejecutor debe inventar el origen y la función de hash para cumplir la coincidencia triple.
2. «conserva identidad y evidencia sin crear registros nuevos» — no dice qué ocurre si una segunda finalización aporta evidencia distinta. Obliga a inventar política de conflicto (rechazar, preservar la primera, marcar discrepancia).
3. «Manifiesto = registro canónico por intento que materializa RunDoc y registros de closeout» — «materializa» no aclara soporte ni forma (archivo aparte, campo embebido, registro de almacenamiento). El ejecutor debe elegir un mecanismo no fijado por la aceptación.

### WS33 [0]
Ninguna.

El alcance del agregado remite a WS33.1/WS33.2, que concretan claves de deduplicación, procedencia, actor y resultado. `Hub` y el contrato público quedan cubiertos por `G_SCION`, producido por WS44; si falta, aplican las reglas comunes de alcance. La ausencia de TaskDoc detallado no cuenta: la promoción lo fijará.

### WS33.1 [3]
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «una importación repetida (mismo Hub/proyecto y conversación)». No queda claro si la conversación integra la clave. Obliga a decidir si un mismo id de mensaje en conversaciones distintas deduplica o no.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente... con la misma regla de deduplicación y procedencia». No se fija la clave de resultados ni si «misma regla» remite a Hub/proyecto/mensaje. Obliga a inventar la composición de la clave.
3. «ni atribuye una conversación completa a un intento». No define criterio observable de «conversación completa» ni cómo probar la no atribución. La aceptación no es comprobable sin inventar ese criterio.

### WS33.2 [0]
Ninguna. La operación concreta, campos y actor se delegan expresamente al contrato WS12 («por la operación que fije el contrato WS12»), con regla de hueco si falta; la aceptación es comprobable y el estado `completed` del agente queda excluido de aprobación.

### WS37 [0]
Ninguna. Las frases «con actor humano», «cierre por el handoff de WS28» y «G_SCION/G_EXEC» remiten a actores, gates o dependencias transitivas ya previstos; el guion detallado queda para el TaskDoc de promoción.

### WS38 [1]
1. «cada acuerdo durable deja su átomo vinculado»: no define qué acuerdos son «durables» ni quién los identifica. Obliga al ejecutor a inventar un criterio de selección y el conjunto de átomos exigidos. Si el acta de WS37 los enumera, la ambigüedad se resuelve con ella; el input no lo garantiza.

### WS39 [1]
1. **Alcance de la mutación según `source_mode`.** Cita: «UF09 inspección y mutación en store temporal real de prueba» y «usar draft/validate/promote de sldb». El contrato vecino WS12 indica: «aceptar delta en sldb solo si source_mode=editable». Si `source_mode=read_only`, no queda claro si WS39 puede cerrar solo con inspección o si la aceptación exige mutación y el nodo queda bloqueado. Obligaría a inventar el criterio de cierre en modo lectura.

### WS40 [4]
1. «hace commits git reales en los repos temporales»: no fija identidad, rama ni mensaje de commit; obligaría a inventar configuración Git y política de commits.
2. «imprime un manifiesto JSON con roots, stores, commits y documentos clave»: no enumera qué documentos son «clave»; obligaría a elegir el conjunto exacto del manifiesto.
3. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «output_scope: tests/fixtures/workspace_documental/»: no aclara si se versiona el generador, una copia fixture o ambos; obligaría a decidir qué es artefacto y qué es efímero.
4. «Entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal»: no define si el Board se crea mediante CLI ni qué tareas contiene; obligaría a inventar su contenido.

### WS41 [0]
Ninguna. Las referencias al contrato WS11, corpus WS40 y gate `G_UI_READ` tienen productor nombrado; la falta de contrato/API se cubre con las reglas comunes de `alcance.md`. La aceptación es comprobable mediante UF08 sobre dos stores y casos de error visibles; textos exactos y pruebas quedan al TaskDoc de promoción.

### WS42 [0]
ninguna.

La condición “cuando disponibles” queda resuelta por la aceptación: cada capability no soportada se declara no disponible y solo bloquea su escenario UF03. La ausencia de contrato la cubre la regla común de ejecución. Los detalles de pantalla, archivos y pruebas quedan para el TaskDoc de promoción.

### WS43 [2]
1. «Registrar conocimiento durable en átomos antes de docs» / «los acuerdos durables aplicados al mapa quedan en átomos enlazados desde él». No se define qué acuerdos son «durables» ni el criterio de «aplicados al mapa». WS31 sí fija una regla (Pxx aceptadas y contratos), pero WS43 no remite a ella. Obligaría a inventar el conjunto de átomos y si incluye contratos o solo decisiones aceptadas.
2. «Aplicar entradas/índices authored validados en Taller al deskops real» / «el mapa publicado corresponde a las entradas/índices validados en Taller». WS17 entrega plantillas de ejemplo y WS30 las valida, pero no se define qué parte es plantilla reutilizable y qué debe reescribirse con los repos reales. Obligaría a inventar el mapeo ejemplo→ecosistema real.
