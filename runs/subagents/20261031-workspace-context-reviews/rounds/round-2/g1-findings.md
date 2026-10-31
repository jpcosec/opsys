### PK04 [2]
1. **Contradicción sobre el bloqueo.** La aceptación admite «revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable», pero luego afirma: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». No queda claro si un hijo `blocked` con responsable permite que PK04 sea verdadera o la invalida; el ejecutor tendría que inventar la regla.
2. **Actor del bloqueo no identificado.** «que el coordinador registra con responsable y dependencia en esa disposition.md»: ninguna fuente suministrada define quién es «el coordinador» ni cómo se le reconoce. Para verificar un bloqueo explícito habría que inventar el actor autorizado.


### PK05 [1]
1. **Contradicción entre bloqueo aceptable y ambigüedad bloqueada.** El input dice: «sin ambigüedad de encargo o bloqueo explícito con responsable» y luego: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera.» No queda claro si un hijo bloqueado por ambigüedad no resuelta satisface PK05 por ser «bloqueo explícito» o la invalida por ser «ambigüedad sin resolver». Para decidirlo habría que inventar si «bloqueo explícito» cubre solo bloqueos por dependencia externa o también bloqueos por ambigüedad; el nodo no distingue ambos casos.


### PK06 [2]
1. **Contradicción sobre el efecto de un hijo bloqueado.** Cita: «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable». Frente a: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». Obliga a decidir si un hijo `blocked` con responsable permite cumplir PK06 o si, por el contrario, lo impide; ambas frases admiten lecturas opuestas.

2. **Actor del registro de bloqueo no identificado.** Cita: «que el coordinador registra con responsable y dependencia en esa disposition.md». El input no nombra a ese coordinador ni indica cómo designarlo. Si aparece un bloqueo, el ejecutor tendría que inventar quién lo registra y con qué legitimidad, pese a que la aceptación depende de ese registro.


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


### WS12 [2]
1. «si no existe, se registra hueco y dueño, no se diseña uno aquí» frente a «la capacidad raw-source faltante se diseña y queda gated por G_SOURCE». Obliga a inventar si WS12 debe producir un diseño de la capacidad faltante o solo el registro de hueco/dueño, y si G_SOURCE corresponde únicamente a WS20.
2. La aceptación enumera «WS19, WS20, WS25, WS26, WS27, WS28, WS32, WS34, WS36, WS39 y WS42», pero G_UI_WRITE incluye WS21 en `scope_nodes`. Obliga a decidir si WS21 (edición fuente desde UI) debe tener capability en este contrato o queda fuera de la whitelist.

