### PK03 [2]
1. Cita: «bloqueo explícito: `context_review.status=blocked` por causa externa (ajena al encargo del propio hijo)». No se fija cómo distinguir una ambigüedad propia de un bloqueo externo cuando falta un contrato o API; obligaría a inventar el criterio de clasificación.  
2. Cita: «y dependencia en esa `disposition.md`». No se define el campo ni la forma de registrar esa dependencia; obligaría a inventar el esquema de `disposition.md` si no lo impone la herramienta.

### PK04 [3]
1. «cuyo hash de input y de contrato coinciden con los actuales»: no se define qué artefacto es el «contrato» —¿el bloque del hijo en `dag.yaml`, su `acceptance`, otro documento?— ni cómo se calcula su hash. Obliga a inventar la fuente y el algoritmo para declarar vigente una revisión.

2. «bloqueo explícito: `context_review.status=blocked` por causa externa (ajena al encargo del propio hijo)»: no hay criterio para separar una causa externa de una ambigüedad propia del hijo. Obliga a inventar la frontera y podría admitir como bloqueo lo que en realidad es un defecto del encargo.

3. «y dependencia en esa disposition.md»: no precisa qué dependencia debe registrarse —la del hijo bloqueado, la del responsable externo u otra— ni su formato mínimo. Obliga a inventar el contenido válido del registro.

### PK07 [3]
1. «sin ambigüedad de encargo o bloqueo explícito con responsable» y «por causa externa (ajena al encargo del propio hijo)» no fijan criterio para distinguir una causa externa de una ambigüedad propia del hijo. Obligaría a inventar esa clasificación y podría cambiar el veredicto de PK07.
2. «dependencia en esa disposition.md» no define campo, formato ni vínculo con el responsable. Obligaría a inventar cómo se registra y comprueba esa dependencia.
3. «sin bloquear lector ni manual básico» no delimita qué capítulos forman el «manual básico», en particular si el capítulo 15 de WS39 queda dentro. Obligaría a decidir si `G_HUMAN_MODEL` contradice ese límite.

### WS04 [4]
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui»: no define qué significa “tocar” (owner_repo, mención textual, archivos afectados). Obliga a inventar el universo de nodos incluidos.  
2. «Cada tarea externa con path, estado observado, hash y alcance» y «Hash = SHA256 del archivo de tarea»: una «entrada del Board» puede no tener archivo de tarea; obliga a inventar un path/hash o una regla de exclusión.  
3. «archivos reclamados por dos sesiones»: no define cómo se registra una reclamación ni cómo atribuir cambios de `git status` o herdr a una sesión; obliga a inventar evidencia de autoría.  
4. «reconciliar también el SPEC externo … frente a este plan»: no fija granularidad ni si “plan” comprende brief, alcance, dag y demás documentos; obliga a inventar la matriz de comparación.

### WS05 [3]
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input (solo WS32, WS32.1, WS32.2). El ejecutor tendría que inventar qué nodo es WS33 y qué capacidades necesita para poder marcarlas.
2. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco» frente a la aceptación de WS05, que obliga a «marca qué capabilities requieren WS32 y WS33». El ejecutor debe inventar si el mapeo por nodo es obligatorio para cerrar WS05 o si su ausencia es admisible y solo bloquea aguas abajo.
3. «Lee código y documentación en deskops y en el repo scion (../scion)». No consta en el input responsable ni autorización de lectura de ese repo; el ejecutor tendría que asumir acceso y que esa ruta es la fuente autoritativa frente a copias vendorizadas.

### WS07 [3]
1. «Designar con identidad explícita a responsable de graph_ui, sldb y spec2viz» y «con identidad registrada por el solicitante en P01». No se define qué dato constituye identidad suficiente ni cómo consta la aceptación del designado. Obligaría a inventar el formato y el criterio de designación válida.

2. «registrar qué acceso read-only tiene» el operador Scion. No se delimita el objeto del acceso —API, Hub, configuración, logs— ni su granularidad. El ejecutor tendría que inventar qué alcance consignar para que WS44 pueda probar sin ambigüedad.

3. «El humano dueño del producto confirma o corrige P01–P09» frente a «solicitante humano de esta sesión o persona que designe explícitamente» en `decisiones.md`. No se aclara si «dueño del producto» es el solicitante u otro rol; obligaría a decidir por cuenta propia quién puede firmar cada Pxx.

### WS08 [1]
1. «cubrir manual» junto con `output_scope: borradores/user-flows.md`. Obligaría a inventar qué “manual” debe cubrirse, si es un artefacto separado del user-flow, dónde se entrega y si WS08 puede escribir fuera de su `output_scope`. No hay nodo ni archivo de manual en el input.

### WS09 [2]
1. «Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes» frente a «Aplica a cada fila de las tablas de vistas.md». Obliga a decidir si el alcance se limita a las filas ya escritas o si deben añadirse filas para «vistas existentes» y categorías no listadas; sin criterio de cierre, el ejecutor inventa el conjunto inventariado.
2. «completa la ficha por fila», cuya ficha incluye «aceptación mediante user-flow», mientras la aceptación solo exige «origen, contrato..., renderer, acción/dueño, error y estado». Obliga a inventar la aceptación/user-flow de filas sin UF asociada o a decidir si ese campo queda vacío; no está definido qué campos son exigibles.

### WS11 [3]
1. “Resolver cada hueco como instancia/vínculo/consulta/API/renderer” y “Clasificar huecos sin modelos hipotéticos”: el input no enumera los huecos ni indica explícitamente qué artefacto de WS09/WS08 los aporta. Obligaría a inventar el inventario de huecos o a asumir una fuente no fijada.
2. “actas de aceptación de G_UI_READ y G_SPEC_VIEW en el repo receptor” frente a “owner_repo: deskops”: no queda claro si WS11 redacta/registra las actas en graph_ui/spec2viz, solo obtiene la aceptación, o las guarda en deskops. Obligaría a inventar autoría y ubicación del artefacto.
3. “graph/code admiten otros nodos con origen”: no se precisa el alcance de esa admisión para Code, mientras alcance.md limita “Code local a 1–2 hops”. Obligaría a decidir si Code navega nodos no documento o solo el ámbito local.
