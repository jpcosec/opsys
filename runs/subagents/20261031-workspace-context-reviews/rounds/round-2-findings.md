### ROOT [0]
ninguna.

### PK01 [0]
ninguna

### PK02 [0]
ninguna.

La aceptación define la condición de verdad, la fuente (`context_review` del hijo en `dag.yaml`), la coincidencia exigida de hashes, la existencia de `disposition.md` y el comando de comprobación. El bloqueo explícito también queda definido con responsable y dependencia. No hay una frase que obligue al ejecutor de PK02 a inventar resultado, aceptación, repo, actor o límite.

### PK03 [0]
Ninguna. La aceptación define revisión vigente por coincidencia de hashes y `disposition.md` guardada, y delega la comprobación en `context_review.py status`; el bloqueo exige responsable y dependencia. No hay criterio que obligue a inventar resultado, repo o aceptación.

### PK04 [2]
1. **Contradicción sobre el bloqueo.** La aceptación admite «revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable», pero luego afirma: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». No queda claro si un hijo `blocked` con responsable permite que PK04 sea verdadera o la invalida; el ejecutor tendría que inventar la regla.
2. **Actor del bloqueo no identificado.** «que el coordinador registra con responsable y dependencia en esa disposition.md»: ninguna fuente suministrada define quién es «el coordinador» ni cómo se le reconoce. Para verificar un bloqueo explícito habría que inventar el actor autorizado.

### PK05 [1]
1. **Contradicción entre bloqueo aceptable y ambigüedad bloqueada.** El input dice: «sin ambigüedad de encargo o bloqueo explícito con responsable» y luego: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera.» No queda claro si un hijo bloqueado por ambigüedad no resuelta satisface PK05 por ser «bloqueo explícito» o la invalida por ser «ambigüedad sin resolver». Para decidirlo habría que inventar si «bloqueo explícito» cubre solo bloqueos por dependencia externa o también bloqueos por ambigüedad; el nodo no distingue ambos casos.

### PK06 [2]
1. **Contradicción sobre el efecto de un hijo bloqueado.** Cita: «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable». Frente a: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». Obliga a decidir si un hijo `blocked` con responsable permite cumplir PK06 o si, por el contrario, lo impide; ambas frases admiten lecturas opuestas.

2. **Actor del registro de bloqueo no identificado.** Cita: «que el coordinador registra con responsable y dependencia en esa disposition.md». El input no nombra a ese coordinador ni indica cómo designarlo. Si aparece un bloqueo, el ejecutor tendría que inventar quién lo registra y con qué legitimidad, pese a que la aceptación depende de ese registro.

### PK07 [0]
Ninguna. La aceptación remite a `python desk/drawer/plans/workspace-documental/context_review.py status`, define “revisión vigente” por coincidencia de hashes y `disposition.md`, y define “bloqueo explícito” con `context_review.status=blocked`, responsable y dependencia. No obliga a inventar resultado, repo, actor ni aceptación.

### PK08 [2]
1. Contradicción sobre el efecto de un bloqueo explícito. Cita: «sin ambigüedad de encargo o bloqueo explícito con responsable». Cita: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». Obliga a inventar si un hijo explícitamente `blocked`, con responsable y dependencia, permite que PK08 sea verdadera o, por el contrario, la impide.
2. Actor no identificado para registrar el bloqueo. Cita: «que el coordinador registra con responsable y dependencia en esa disposition.md». No se define quién es el coordinador ni en qué repo actúa; obliga a inventar la identidad o autoridad que validaría un `blocked`.

### WS01 [2]
1. «distinciones documento/nodo/vista/renderer/consulta/foco». El brief define «Renderización/representación» y «Vista de trabajo», pero no usa el término «renderer». Obliga a inventar si debe añadirse una entrada nueva «renderer», renombrar la existente o interpretarla como sinónimo.
2. «Cada acuerdo cita al solicitante y cada propuesta remite a decisiones.md.» No se delimita qué afirmaciones del brief son «acuerdo» ni qué es «propuesta» (frente a vocabulario, criterio de éxito o límites). Obliga a inventar el inventario de acuerdos/propuestas y su correspondencia con Pxx.

### WS02 [3]
1. «Inventariar superficies y operaciones Deskops»: no se define «superficie» ni su unidad. El ejecutor tendría que inventar si cuenta archivos, comandos, modelos, endpoints, componentes UI o filas del desk, con riesgo de exceder el alcance.
2. «Cada fila incluye archivo/código/operación y estado comprobado»: la barra no aclara si exige los tres campos o uno de ellos. Afecta a la aceptación comprobable; el ejecutor inventaría el contrato de fila.
3. «lo no comprobado se marca así»: no hay vocabulario para distinguir ausente, inaccesible o no encontrado. El ejecutor inventaría estados y podría declarar como «no comprobado» algo que simplemente no existe.

### WS03 [1]
1. «conflictos y límites de locks»: no identifica qué mecanismo de bloqueo debe auditarse —transacción/DB, archivo, coordinador/CLI u otro— ni qué cuenta como conflicto o límite. Obligaría al ejecutor a inventar el objeto de la auditoría y el criterio para declararlo comprobado, ausente o hueco.

### WS04 [3]
1. «Leer graph_ui Board, tareas y código actuales»: el input no indica ruta ni localización del Board/repo graph_ui, y `owner_repo` es deskops. Obligaría a inventar dónde leer; `reconciliacion.md` alude a `external_references`, pero no se suministra su contenido.

2. «mapear nodos de este plan a deltas existentes»: no define qué cuenta como delta existente (¿tarea draft, ticket, commit, nodo del Board?) ni qué evidencia del mapa debe quedar en `auditoria/ui.md`; la aceptación solo exige datos de tareas externas. Obligaría a inventar el universo y el formato del mapeo.

3. «reconciliar también SPEC externo y cualquier encargo aportado al ejecutar»: no fija criterio para reconciliar el SPEC (qué comparar, qué registrar ante coincidencia o discrepancia). Obligaría a inventar el criterio y su evidencia.

### WS05 [4]
1. «Leer runtime/templates/RunDoc y API pública de Scion» junto a «no contacta endpoints vivos ni usa credenciales». No se define qué cuenta como «API pública» ni su fuente de verdad: ¿OpenAPI/docs, endpoints exportados o módulos Python? Obliga a inventar el criterio y el nivel de exposición, con riesgo de presentar funciones internas como interfaz.
2. «separar slug/agente/intento/dispatch/mensaje/conversación y permisos». «Permisos» no indica si son roles de usuario, scopes de token, permisos de operación o autorización del Hub. Obliga a inventar la taxonomía y podría omitir la que consuma WS32/WS33.
3. «Sin agentes/mensajes/config ni mostrar tokens». «Config» puede leerse como prohibición de leer configuración o solo de cambiarla; el alcance no lo aclara. Obliga a decidir si puede inspeccionar documentación/configuración existente para inventariar API y Hub.
4. Aceptación: «señalar campos internos no expuestos». No dice “no expuestos” respecto de qué superficie (API HTTP, SDK, documentación) ni cómo determinarlo sin probe. Obliga a inventar el criterio de exposición.

### WS06 [3]
1. **Alcance de la matriz frente a Scion.** Cita: «Una matriz por implementación: ya cubierto, extender ticket existente o nuevo delta». `reconciliacion.md` incluye la línea «Scion RunDoc/cierre | WS32/33», pero WS06 solo depende de WS02–WS04. Si la matriz abarca esa línea, el ejecutor tendría que inventar la correspondencia o decidir omitirla sin inventario previo. Falta WS05 como dependencia explícita o una exclusión expresa.
2. **Criterio de «ya cubierto».** Cita: «ya cubierto». No se define si significa cubierto por código existente, por una tarea del Board o por una capacidad ya planificada. El ejecutor tendría que inventar el criterio de clasificación.
3. **Unidad de fila.** Cita: «Una matriz por implementación». No queda fijado si cada fila es un nodo del DAG, una capacidad, un ticket existente o un delta. El ejecutor tendría que inventar la granularidad.

### WS07 [2]
1. «`baseline_proposal` de dag.yaml»: no se define qué es ni aparece en el fragmento suministrado, mientras `output_scope` solo admite «decisiones.md; parameters.source_mode en dag.yaml». Obligaría a inventar si WS07 puede modificar esa clave, qué contiene y si hacerlo excede el alcance de salida.  
2. «reconsiderar alcance según P04»: no se precisa si implica editar nodos, dependencias o variantes del DAG, o solo dejar constancia en `decisiones.md`. `output_scope` no incluye cambios en nodos. Obligaría a inventar el alcance real de esa reconsideración.

### WS08 [3]
1. «cubrir manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado»: no asigna UF a «cambios» ni a «modo degradado». Obliga a inventar si «cambios» es WS29/impacto, UF08 o edición, y en qué UF se documenta el modo degradado.
2. «ack local disponible según contrato»: no nombra el contrato ni su productor; WS12 (`contratos/operaciones.md`) depende de WS08. Obliga a inventar el contrato o a dar por disponible una operación no verificada, contra la regla de marcar hueco.
3. «Mapear UF a operaciones de WS02/03/04» frente a «Las operaciones vienen de auditoria/{deskops,infraestructura,ui}.md»: no fija si la autoridad es el nodo o el archivo de auditoría. Obliga a decidir qué operación citar cuando solo una fuente la contiene.

### WS09 [2]
1. «disponibilidad actual viene de auditoria/ui.md»  
   No se identifica nodo, actor ni repo que produzca ese archivo, ni qué hacer si falta. Obliga a inventar el inventario de disponibilidad actual o a suponer que el artefacto existe.

2. «Estado = disponible/propuesto/bloqueado según WS10»  
   WS10 no figura en `depends_on` de WS09 y no se define su salida ni fallback. Obliga al ejecutor a inventar la regla de clasificación o a asumir un resultado de WS10 no suministrado.

### WS10 [1]
1. Cita: «Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva por WS07.» El bloque suministrado de WS07 solo declara `depends_on: WS06`, no WS03/WS04. Esto contradice la afirmación del nodo y obliga al ejecutor a inventar de dónde obtiene las auditorías WS03/WS04, si debe esperarlas o si puede omitirlas.

### WS11 [0]
Ninguna.

### WS12 [2]
1. «si no existe, se registra hueco y dueño, no se diseña uno aquí» frente a «la capacidad raw-source faltante se diseña y queda gated por G_SOURCE». Obliga a inventar si WS12 debe producir un diseño de la capacidad faltante o solo el registro de hueco/dueño, y si G_SOURCE corresponde únicamente a WS20.
2. La aceptación enumera «WS19, WS20, WS25, WS26, WS27, WS28, WS32, WS34, WS36, WS39 y WS42», pero G_UI_WRITE incluye WS21 en `scope_nodes`. Obliga a decidir si WS21 (edición fuente desde UI) debe tener capability en este contrato o queda fuera de la whitelist.

### WS13 [0]
Ninguna.

Las dependencias y el gate pendiente están nombrados con actor/productor (WS11, WS07) y la regla de falta de contrato está cubierta por `alcance.md`. Los detalles de archivos, TaskDoc y pills se delegan a la promoción.

### WS13.1 [1]
1. «Code local con selección por documento/nodo». No define qué se selecciona ni qué efecto observable tiene. La aceptación solo exige «alternar entre texto/graph/code» y preservar origen, no comprobar la selección por documento/nodo. El ejecutor tendría que inventar si seleccionar un documento/nodo actualiza Code, si seleccionar Code cambia foco o si es solo estado visual, y cómo demostrarlo.

### WS13.2 [0]
ninguna.

### WS13.3 [2]
1. **Cobertura de pestañas en la aceptación.** Cita: alcance “Pestañas, dos documentos lado a lado…” frente a aceptación “Abrir dos documentos en divisiones…”. Obliga a inventar si abrir/cambiar/cerrar pestañas es requisito verificable o si basta con dos divisiones; la aceptación no dice cómo comprobar la parte de pestañas.
2. **Significado operativo de “foco” y “origen”.** Cita: “alternar foco y volver conservando origen e historia” y “Foco es por documento; cambiar de pestaña cambia el documento activo, no el foco guardado…”. El glosario define foco como elemento seleccionado, pero aquí puede leerse como panel/documento activo. Obliga a inventar qué acción concreta demuestra “alternar foco” y qué estado observable prueba conservar el origen al volver.

### WS14 [2]
1. «según auditoria/infraestructura.md y contrato WS11»: no se identifica qué nodo o actor produce `auditoria/infraestructura.md` ni se aporta su contenido. El ejecutor tendría que inventar si ese documento existe, quién lo emite y qué criterio de infraestructura aplica, o asumir sin base que WS11 lo cubre.
2. «Sin resultados, error de backend y búsqueda degradada se ven como tres estados distintos»: no se define qué sigue funcionando en «búsqueda degradada» ni qué la diferencia funcionalmente del error de backend. Con «no parser propio», el ejecutor tendría que inventar un fallback o el criterio de distinción entre ambos estados.

### WS15 [0]
Ninguna.

### WS15.1 [0]
ninguna.

### WS15.2 [0]
ninguna.

### WS16 [1]
1. «Incluye UF10 arranque/ausencia de desk» junto a «sin crear corpus propio», frente a WS40 («Crear dos repos temporales… sus stores») y validacion-humana («Proyecto Taller… con su propio git y desk/store temporal»; «Segundo desk temporal para UF08»). El corpus descrito no contiene un proyecto sin desk. El ejecutor tendría que inventar/crear ese fixture —corpus propio— o decidir omitir UF10; ninguna de ambas está autorizada.

### WS17 [0]
Ninguna que obligue al ejecutor de WS17 a inventar resultado, aceptación, repo, actor, dependencia o límite.

### WS18 [2]
1. «output_scope: sldb/views/ (nombres confirmados por contrato)» — no se identifica qué contrato ni quién confirma esos nombres. Obliga a inventar la ruta/archivo exacto o a asumir que el contrato es `contratos/navegacion.md` de WS11, que no los enumera.
2. «Vista portable evaluada sobre store real» — no fija resultado observable ni criterio de paso/fallo de esa evaluación. Obliga a inventar qué significa «evaluada» (¿render?, ¿selección correcta?, ¿ambas?). El TaskDoc puede fijar escenarios, pero solo dentro de una aceptación que aquí queda indefinida.

### WS19 [0]
Ninguna.

El nodo distingue propósito, hijos, repo, dependencias y aceptación agregada. Las puertas pendientes son intencionales y tienen productor/resolver identificado: `G_HUMAN_READ` por WS16; `G_UI_WRITE` y `G_WRITE_CONTRACT` por WS12. Los detalles de archivos, pruebas y textos quedan delegados a la promoción/TaskDoc, conforme a la guía.

### WS19.1 [1]
1. Cita: «endpoints autorizados por el contrato WS12» dentro de `output_scope`. Al figurar como parte del alcance de salida, no queda claro si el nodo solo consume endpoints ya autorizados o también puede modificar su código; esto obligaría a inventar si el cambio cruza a otro repo y dónde termina el límite de `graph_ui`.

### WS19.2 [0]
Ninguna.

El nodo nombra el contrato que define las relaciones permitidas («permitidas por contrato»), la API («usando API real») y la revisión («before-image»); WS12 produce la whitelist y las capabilities, y `alcance.md` resuelve qué hacer si faltan. La aceptación es comprobable: persistencia tras recarga y rechazo visible de relación no permitida o revisión obsoleta. Los textos exactos de pantalla y archivos quedan delegados al TaskDoc de promoción.

### WS20 [0]
ninguna

### WS21 [3]
1. Contradicción de gates. Cita: «No requiere G_SOURCE si el humano eligió fuente read_only». El nodo base lista `G_SOURCE` en `requires` y la regla de variantes dice que «Una variante añade dependencias y gates a los del nodo base; nunca los quita»; la variante read_only usa `requires: []`. Obligaría a inventar si `G_SOURCE` sigue siendo prerrequisito en read_only.
2. Confirmación de descarte del buffer. Cita: «nunca se descarta sin confirmación». No se define actor, canal ni condición de esa confirmación; obligaría a inventar quién confirma y qué ocurre si no hay confirmación disponible.
3. Estado `pending` dentro de la aceptación. Cita: «Cumplir la aceptación específica de la variante P04», mientras solo existen variantes `editable` y `read_only`. El `scope` dice que con pending no se prepara ni promueve, pero la aceptación no declara resultado verificable para ese valor; obligaría a inventar si el nodo queda no ejecutable o bloqueado.

### WS22 [0]
Ninguna.

### WS23 [1]
1. Cita: “obligaciones, transiciones y fuentes navegables”. “Obligaciones” no está definido en el glosario ni en la aceptación. Obligaría a inventar qué obligaciones debe mostrar la vista, de qué campo/documento salen y cómo se comprueba que están bien representadas.

### WS24 [5]
1. **“crossroads”**: «Reutilizar gráfico actual y documento genérico para átomos/protoátomos/crossroads/materializaciones/pills». No aparece definido en brief.md ni en el glosario. Obligaría a inventar qué entidad es y cómo se representa.

2. **“documento genérico”**: «documento genérico para átomos/protoátomos…». El glosario define “Documento” y “Vista de trabajo”, pero no este componente. Obligaría a inventar qué contrato o componente existente se reutiliza.

3. **Referencia normativa ausente**: «Backlinks = relaciones entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md». Ese archivo no consta en el input ni se identifica nodo que lo produzca. Obligaría a inventar la semántica de backlinks y la capacidad real de la API.

4. **Aceptación no comprobable**: «soporte no modelado visible». No define qué cuenta como “soporte no modelado” ni qué evidencia demuestra “visible”. Obligaría a inventar el criterio de aceptación.

5. **“tarea actual”**: «preservar Code local de tarea actual» y «Code local = proyección Code del ticket workspace». No se identifica la tarea concreta entre las draft de graph_ui. Obligaría a inventar el destino de integración.

### WS25 [0]
Ninguna. El nodo delega resultado y aceptación comprobable en WS25.1/WS25.2, identifica repo, dependencias y límites. Los gates pendientes son intencionales. La ausencia de contrato operativo está cubierta por alcance.md: detenerse, registrar hueco y declarar la operación no disponible. Los detalles de archivos, pruebas y textos quedan para el TaskDoc de promoción.

### WS25.1 [0]
Ninguna. El nodo nombra repo, resultado, límites, dependencias y aceptación comprobable; la condicionalidad de la respuesta y el comportamiento ante contrato ausente quedan cubiertos por WS12 y por `alcance.md` («detenerse, registrar el hueco... La operación queda no disponible»). No hay frase que obligue al ejecutor a inventar.

### WS25.2 [2]
1. «Capturar en drawer o protoátomo» / «drawer/protoátomo». No fija si hay que implementar ambos destinos, uno de ellos o una elección del usuario; tampoco qué distingue drawer de protoátomo. Obligaría a inventar el alcance funcional y si la aceptación («una captura persiste») se cumple con cualquiera de los dos.
2. «Origen = ruta o mensaje del que nace la captura.» No aclara si deben soportarse y validarse ambos orígenes o solo uno, ni cómo se representa el origen. Obligaría a inventar el modelo de origen y la matriz de aceptación.

### WS26 [0]
Ninguna.

El encargo es legible como agregado: el resultado está definido por sus hijos («Agregado: salidas de WS26.1, WS26.2»), la aceptación remite a ellos («se cumple cuando todos sus hijos cumplen su aceptación»), el repo está presente (`owner_repo: graph_ui`) y los límites excluyen ejecución y promoción no autorizada. Que `depends_on` incluya WS26.1/WS26.2 es coherente con un agregado que termina cuando terminan sus hijos; no obliga a inventar nada. Los gates pendientes son intencionales según la guía.

### WS26.1 [2]
1. «Autoría explícita desde candidato, evidencia declarada, dependencias y binding de contexto/pills» frente a «UF04 sobre TaskDoc real». La aceptación no define qué resultado observable ni qué comprobación cubre evidencia, dependencias o binding; UF04 no los detalla. Obliga al ejecutor a inventar criterios de aceptación para esas partes del alcance.
2. «G_HUMAN_MANUAL no pasa hasta que el dueño de esa operación la resuelva». G_HUMAN_MANUAL lo produce WS30 y no figura en `requires` de WS26.1; tampoco se concreta la operación ni el dueño. Obliga a inventar cómo este nodo bloquea o verifica un gate ajeno.

### WS26.2 [1]
1. «sin archivos solapados, como define el ritual de fase»: no se adjunta el ritual ni se fija qué archivos se comparan ni cuándo hay solapamiento. Obligaría a inventar el algoritmo, el conjunto de archivos y la fuente de verdad de la capa lista.

### WS27 [0]
ninguna.

### WS27.1 [3]
1. «historial read-only junto a la TaskDoc»: el alcance promete historial, pero la aceptación solo exige «Diff real acotado al repo y tarea»; no define qué historial ni cómo comprobarlo. Obligaría a inventar alcance y prueba del historial.
2. «Base: commits de TaskDoc.references; sin ellos, working tree contra HEAD limitado a TaskDoc.files»: no se nombra quién produce ni con qué contrato se resuelven `TaskDoc.references`/`TaskDoc.files`. WS12 registra capabilities Git, no el modelo TaskDoc. Obligaría a inventar la fuente y el fallback.
3. «Diff real acotado al repo y tarea»: no se define qué repo cuando `TaskDoc.files` puede referenciar varios; `output_scope` solo declara `graph_ui`. Obligaría a inventar la selección de repos.

### WS27.2 [3]
1. «encontrada = artefactos hallados»: no define qué fuente ni qué criterio produce un “hallazgo” (¿rutas declaradas en la TaskDoc?, ¿búsqueda en el repo?, ¿artefactos de test?). Obliga al ejecutor a inventar el mecanismo y el universo de búsqueda.
2. «una evidencia ausente se ve como ausente»: solo cubre el caso ausente; no define qué mostrar cuando declarada, encontrada y verificada discrepan (declarada sin artefacto, encontrada no declarada, verificación fallida). Obliga a inventar la semántica de estados y su combinación.
3. «Abrir soporte = abrir el artefacto en el lector»: no aclara qué lector ni qué hacer con artefactos no Markdown o fuera del workspace; `alcance.md` limita adjuntos binarios, pero el nodo no restringe “artefacto”. Obliga a inventar el manejo de esos casos.

### WS28 [0]
Ninguna.

### WS29 [4]
1. «relaciones alcanzadas» (aceptación) y «relaciones comprobadas» (scope): no se define desde qué nodo, con qué profundidad ni dirección se consideran alcanzadas; obligaría a inventar el criterio de impacto.
2. «documento afectado, relaciones alcanzadas y errores»: «errores» no se acota —¿de lectura, `check`, `doctor` o `drift`?— ni su forma de mostrarse; obligaría a inventar taxonomía y origen.
3. «la vista enlaza al comando documentado»: no identifica cuál de los tres comandos enlaza ni dónde está documentado; obligaría a inventar el destino del enlace y la correspondencia error→reparación.
4. «Delta sobre tarea Changes actual»: no nombra la tarea/ticket receptor concreto; obligaría a decidir si es delta o ticket nuevo, aunque `integration_mode` y la matriz WS06 pretendan resolverlo transitivamente.

### WS30 [0]
ninguna.

### WS31 [3]
1. **Universo de átomos indeterminado.** Cita: «un átomo por acuerdo durable de decisiones.md y contratos/». `decisiones.md` declara «No consta aún decisión humana sobre las propuestas» y solo contiene Pxx pendientes; `contratos/` no enumera aquí qué contratos existen ni en qué repo. Obliga a inventar qué acuerdos son “durables”, si se atomizan propuestas Pxx o si el conjunto es vacío.
2. **Soporte y ubicación de capturas.** Cita: «incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md». `output_scope` solo autoriza el Markdown y átomos; no define dónde viven las imágenes ni si crear assets queda dentro del alcance. Obliga a inventar rutas/formato o a decidir omitir capturas, contra el enunciado.
3. **Referente de «versión publicada».** Cita: «Cada instrucción remite a un acta o prueba de la versión publicada». No queda claro si es el acta de WS30 en graph_ui, el acta de publicación de WS43 en deskops, o una prueba nueva contra el manual final. Obliga a inventar la fuente de evidencia y, eventualmente, una verificación no prevista en dependencias.

### WS32 [0]
Ninguna.

### WS32.1 [3]
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc»: no se define dónde se registra cada hecho ni qué evento exacto constituye «Scion aceptó». El ejecutor tendría que inventar el modelo de estados.
2. «cambios de RunDoc por el flujo de modelos SLDB»: el input no describe ese flujo ni su autoridad; obligaría a inventar el canal y el criterio de comprobación.
3. «un dispatch fallido conservan identidades distintas»: no se delimita qué fallos cubre (rechazo, timeout, error de transporte) ni cómo se evidencia la identidad distinta. Obligaría a inventar el criterio de aceptación.

### WS32.2 [3]
1. «sobre el intento correcto»: no se define cómo elegir ese intento entre varios del mismo agente o tras un dispatch fallido. Obliga a inventar la regla de selección y su efecto sobre el cierre.
2. «según el ticket de external_references.scion»: el ticket no se transcribe en el input y sería la única definición de manifiesto y registros de closeout. Obliga a inventar campos, formato y qué significa «materializa RunDoc».
3. «Manifiesto, RunDoc y cierre consistentes» frente a «Una finalización repetida... conserva identidad y evidencia sin crear registros nuevos»: la aceptación solo cubre idempotencia, no la consistencia entre los tres. Obliga a inventar cómo se comprueba esa consistencia.

### WS33 [0]
Ninguna.

Comprobado y descartado como ambigüedad según la guía:
- G_SCION `unverified`: gate pendiente intencional; su productor (WS44, operador designado en WS07) está nombrado y alcance.md fija qué hacer si falta.
- Detalles de archivos/pills/TaskDoc: delegados a promoción (`task_file` nombrado).
- Dependencia de hijos en el propio agregado: patrón consistente con WS32/WS34; la aceptación declara explícitamente que los dependientes siguen colgando de este ID.
- Clave de deduplicación: definida en WS33.1 (Hub + proyecto + id de mensaje) y heredada por el agregado.

### WS33.1 [4]
1. «Referencias Hub/proyecto/conversación/mensaje/intento y resultados» y «Clave de deduplicación: Hub + proyecto + id de mensaje». La clave solo cubre mensajes: no define identidad, procedencia ni deduplicación de «resultados». El ejecutor tendría que inventar el esquema de resultados y su idempotencia; la aceptación tampoco los menciona expresamente.  
2. «Solo se vinculan mensajes y resultados con referencia al intento.» No define qué es una referencia válida ni qué hacer si un mensaje referencia varios intentos, uno inexistente o solo una conversación. Obliga a inventar la regla de correspondencia y el tratamiento de conflictos; WS32 define identidad de intento, no referencia de mensaje.  
3. «una importación repetida no duplica»: no se define «importación» (unidad, origen, lote) ni el alcance de la repetición. Aunque la deduplicación por id de mensaje acota mensajes, el ejecutor debe inventar qué se importa y cómo se prueba la no duplicación de resultados.  
4. `depends_on: WS32, WS11`: WS11 entrega contrato de navegación e identidad documental, pero el scope de WS33.1 no menciona documentos ni navegación. El ejecutor tendría que inventar qué parte de WS11 consume o por qué bloquea este backend.

### WS33.2 [3]
1. «asociada a tarea/intento», frente a la aceptación «referencia al intento»: no queda claro si el vínculo obligatorio es la tarea, el intento o ambos. Obligaría a inventar el campo y su integridad referencial.
2. «(aprobar o pedir corrección)»: la aceptación no fija valores de resultado ni exige contenido para una corrección. Obligaría a inventar el vocabulario/estado y si el texto correctivo es obligatorio.
3. «validado y cerrado los lee de deskops»: no se nombra quién valida/cierra ni el dato exacto que consumen. Si este nodo debe exponerlo, obligaría a inventar un contrato de lectura o estados que su límite no posee.

### WS34 [0]
Ninguna.

El nodo es agregado y su aceptación declara explícitamente que no es ejecutable, en línea con la guía. El repo, los hijos, las dependencias y los gates están identificados. La autoridad del coordinador remite a WS12, que la produce, y el comportamiento ante contrato ausente lo cubre alcance.md ("detenerse, registrar el hueco... no crear sustituto"). Las decisiones Pxx pendientes no se interpretan como aprobadas.

### WS34.1 [1]
1. «output_scope: runtime/; cli/commands/runtime.py o API definida; tests/» no aclara si «API definida» es un canal público ya existente o una API que este nodo deba definir. WS12 establece que el adapter es un canal público existente y que, si falta, se registra hueco y dueño, no se diseña aquí. Obligaría a inventar el canal/contrato de dispatch y podría exceder el alcance.

### WS34.2 [1]
1. «con timeout/errores» frente a «agente real demuestra respuesta vinculada al intento correcto». La aceptación solo exige demostrar el caso exitoso; no fija comportamiento observable para timeout ni para errores. El ejecutor tendría que inventar el umbral de timeout, qué errores cubrir y cuándo considerarlos aceptados.

No encuentro otras: el repo está identificado, el resultado está acotado, las dependencias y gates están nombrados, y los contratos externos tienen productores designados.

### WS35 [1]
1. «Cada mensaje y resultado se muestra bajo su intento» junto con «mensajes de Scion por su API»: no se define qué es un «resultado» ni qué dependencia lo produce con contrato propio. WS33 se titula «Vincular mensajes, resultados y decisiones», pero el alcance de WS35 solo nombra mensajes de Scion, tarea, intento y decisión. El ejecutor tendría que inventar si «resultado» es un payload de mensaje Scion, una salida del intento o un registro de WS33, y cómo se enlaza «a su fuente».

### WS36 [2]
1. «revisión con actor/evidencia visible» — no define qué actor (humano, coordinador, agente), qué evidencia ni cómo se comprueba; la aceptación no la recoge. Obliga a inventar el sujeto y el criterio de visibilidad y prueba.
2. «registrar decisiones con WS33.2» — WS33.2 no se describe en el input ni figura en `depends_on`; solo aparece como referencia. Obliga a inventar su contrato o asumir una dependencia no declarada.

### WS37 [1]
1. «G_SCION/G_EXEC y protocolo» (acceptance). No identifica qué protocolo: `validacion-humana.md` es el único protocolo suministrado, pero el nodo no lo cita ni concreta qué pasos o evidencia de ese protocolo aplican a UF06. Obligaría a inventar el protocolo de aceptación o a elegir entre fuentes. Cita textual: «acceptance: G_SCION/G_EXEC y protocolo».

### WS38 [0]
Ninguna. El alcance, la fuente de verdad (acta de WS37) y la aceptación son comprobables. Los átomos y archivos exactos quedan para la promoción, y la ausencia de acta o de contrato se resuelve por las reglas comunes de `alcance.md`, no inventando contenido.

### WS39 [2]
1. «G_HUMAN_MODEL debe pasar antes de marcar disponible el capítulo 15 del manual.»  
   No se identifica qué manual, dónde vive ni por qué es el capítulo 15. Obliga a inventar la fuente del manual, su numeración y qué significa «marcar disponible».

2. «Guardar acta de prueba humana [...] con participante designado y resultado»  
   No se nombra quién designa al participante ni qué persona concreta valida. Obliga a inventar el actor y el procedimiento de designación; `P08` sigue pendiente y no lo resuelve.

### WS40 [3]
1. «Crear dos repos temporales bajo .tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «nunca toca desk real». Falta la base de `.tmp`: si cuelga de graph_ui, del cwd o de un desk. Obliga a inventar dónde se escribe y si eso contradice el límite.
2. «entrada mínima ecosistema/proyecto con enlaces al Board/FAQ/conocimiento». No se define si Board/FAQ/conocimiento son documentos Markdown, datos reales de Deskops (tareas/Board) o vistas. Obliga a inventar qué se enlaza y qué se crea en el corpus.
3. «usar contratos/CLI reales» no nombra el contrato ni los comandos concretos. Aunque WS11 es dependencia, el nodo no explicita que su contrato de navegación sea el aplicable ni qué CLI crea stores/commits; obliga a elegir interfaz.

### WS41 [0]
Ninguna.

### WS42 [2]
1. «materializaciones se inspeccionan/validan, no se generan destinos arbitrarios» — el alcance incluye un comportamiento (inspección/validación de materializaciones) que la aceptación no recoge: no dice qué se valida, contra qué contrato ni cómo se comprueba. Obligaría a inventar resultado y criterio de aceptación, o a decidir si queda fuera.
2. «cada capability no soportada se declara no disponible y bloquea ese escenario» — «ese escenario» no está delimitado: puede ser la capability concreta, UF03 o el gate WS30. Obligaría a inventar el alcance del bloqueo y su efecto sobre la validación.

### WS43 [3]
1. «Persona designada recorre Markdown y UI real»: no se identifica quién designa ni qué persona acepta. Obligaría a inventar el actor de aceptación y quién firma/commitea el acta.
2. «Repos a enlazar = `deskops list repositories`» frente a «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: no queda claro si todos los repos listados pueden enlazarse en WS43 o solo los que ya tengan tarea/acuerdo. Obligaría a inventar el criterio de inclusión y si hay que abrir tareas antes.
3. «links/roots verificables»: no se define qué es un `root` ni qué hace verificable un enlace. Obligaría a inventar el criterio de aceptación y el método de comprobación.

### WS44 [0]
Ninguna.
