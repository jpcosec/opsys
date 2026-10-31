### WS19.1 [1]
1. Cita: «endpoints autorizados por el contrato WS12» dentro de `output_scope`. Al figurar como parte del alcance de salida, no queda claro si el nodo solo consume endpoints ya autorizados o también puede modificar su código; esto obligaría a inventar si el cambio cruza a otro repo y dónde termina el límite de `graph_ui`.


### WS21 [3]
1. Contradicción de gates. Cita: «No requiere G_SOURCE si el humano eligió fuente read_only». El nodo base lista `G_SOURCE` en `requires` y la regla de variantes dice que «Una variante añade dependencias y gates a los del nodo base; nunca los quita»; la variante read_only usa `requires: []`. Obligaría a inventar si `G_SOURCE` sigue siendo prerrequisito en read_only.
2. Confirmación de descarte del buffer. Cita: «nunca se descarta sin confirmación». No se define actor, canal ni condición de esa confirmación; obligaría a inventar quién confirma y qué ocurre si no hay confirmación disponible.
3. Estado `pending` dentro de la aceptación. Cita: «Cumplir la aceptación específica de la variante P04», mientras solo existen variantes `editable` y `read_only`. El `scope` dice que con pending no se prepara ni promueve, pero la aceptación no declara resultado verificable para ese valor; obligaría a inventar si el nodo queda no ejecutable o bloqueado.


### WS25.2 [2]
1. «Capturar en drawer o protoátomo» / «drawer/protoátomo». No fija si hay que implementar ambos destinos, uno de ellos o una elección del usuario; tampoco qué distingue drawer de protoátomo. Obligaría a inventar el alcance funcional y si la aceptación («una captura persiste») se cumple con cualquiera de los dos.
2. «Origen = ruta o mensaje del que nace la captura.» No aclara si deben soportarse y validarse ambos orígenes o solo uno, ni cómo se representa el origen. Obligaría a inventar el modelo de origen y la matriz de aceptación.


### WS26.1 [2]
1. «Autoría explícita desde candidato, evidencia declarada, dependencias y binding de contexto/pills» frente a «UF04 sobre TaskDoc real». La aceptación no define qué resultado observable ni qué comprobación cubre evidencia, dependencias o binding; UF04 no los detalla. Obliga al ejecutor a inventar criterios de aceptación para esas partes del alcance.
2. «G_HUMAN_MANUAL no pasa hasta que el dueño de esa operación la resuelva». G_HUMAN_MANUAL lo produce WS30 y no figura en `requires` de WS26.1; tampoco se concreta la operación ni el dueño. Obliga a inventar cómo este nodo bloquea o verifica un gate ajeno.


### WS26.2 [1]
1. «sin archivos solapados, como define el ritual de fase»: no se adjunta el ritual ni se fija qué archivos se comparan ni cuándo hay solapamiento. Obligaría a inventar el algoritmo, el conjunto de archivos y la fuente de verdad de la capa lista.


### WS27.1 [3]
1. «historial read-only junto a la TaskDoc»: el alcance promete historial, pero la aceptación solo exige «Diff real acotado al repo y tarea»; no define qué historial ni cómo comprobarlo. Obligaría a inventar alcance y prueba del historial.
2. «Base: commits de TaskDoc.references; sin ellos, working tree contra HEAD limitado a TaskDoc.files»: no se nombra quién produce ni con qué contrato se resuelven `TaskDoc.references`/`TaskDoc.files`. WS12 registra capabilities Git, no el modelo TaskDoc. Obligaría a inventar la fuente y el fallback.
3. «Diff real acotado al repo y tarea»: no se define qué repo cuando `TaskDoc.files` puede referenciar varios; `output_scope` solo declara `graph_ui`. Obligaría a inventar la selección de repos.


### WS27.2 [3]
1. «encontrada = artefactos hallados»: no define qué fuente ni qué criterio produce un “hallazgo” (¿rutas declaradas en la TaskDoc?, ¿búsqueda en el repo?, ¿artefactos de test?). Obliga al ejecutor a inventar el mecanismo y el universo de búsqueda.
2. «una evidencia ausente se ve como ausente»: solo cubre el caso ausente; no define qué mostrar cuando declarada, encontrada y verificada discrepan (declarada sin artefacto, encontrada no declarada, verificación fallida). Obliga a inventar la semántica de estados y su combinación.
3. «Abrir soporte = abrir el artefacto en el lector»: no aclara qué lector ni qué hacer con artefactos no Markdown o fuera del workspace; `alcance.md` limita adjuntos binarios, pero el nodo no restringe “artefacto”. Obliga a inventar el manejo de esos casos.


### WS29 [4]
1. «relaciones alcanzadas» (aceptación) y «relaciones comprobadas» (scope): no se define desde qué nodo, con qué profundidad ni dirección se consideran alcanzadas; obligaría a inventar el criterio de impacto.
2. «documento afectado, relaciones alcanzadas y errores»: «errores» no se acota —¿de lectura, `check`, `doctor` o `drift`?— ni su forma de mostrarse; obligaría a inventar taxonomía y origen.
3. «la vista enlaza al comando documentado»: no identifica cuál de los tres comandos enlaza ni dónde está documentado; obligaría a inventar el destino del enlace y la correspondencia error→reparación.
4. «Delta sobre tarea Changes actual»: no nombra la tarea/ticket receptor concreto; obligaría a decidir si es delta o ticket nuevo, aunque `integration_mode` y la matriz WS06 pretendan resolverlo transitivamente.


### WS31 [3]
1. **Universo de átomos indeterminado.** Cita: «un átomo por acuerdo durable de decisiones.md y contratos/». `decisiones.md` declara «No consta aún decisión humana sobre las propuestas» y solo contiene Pxx pendientes; `contratos/` no enumera aquí qué contratos existen ni en qué repo. Obliga a inventar qué acuerdos son “durables”, si se atomizan propuestas Pxx o si el conjunto es vacío.
2. **Soporte y ubicación de capturas.** Cita: «incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md». `output_scope` solo autoriza el Markdown y átomos; no define dónde viven las imágenes ni si crear assets queda dentro del alcance. Obliga a inventar rutas/formato o a decidir omitir capturas, contra el enunciado.
3. **Referente de «versión publicada».** Cita: «Cada instrucción remite a un acta o prueba de la versión publicada». No queda claro si es el acta de WS30 en graph_ui, el acta de publicación de WS43 en deskops, o una prueba nueva contra el manual final. Obliga a inventar la fuente de evidencia y, eventualmente, una verificación no prevista en dependencias.


### WS39 [2]
1. «G_HUMAN_MODEL debe pasar antes de marcar disponible el capítulo 15 del manual.»  
   No se identifica qué manual, dónde vive ni por qué es el capítulo 15. Obliga a inventar la fuente del manual, su numeración y qué significa «marcar disponible».

2. «Guardar acta de prueba humana [...] con participante designado y resultado»  
   No se nombra quién designa al participante ni qué persona concreta valida. Obliga a inventar el actor y el procedimiento de designación; `P08` sigue pendiente y no lo resuelve.


### WS42 [2]
1. «materializaciones se inspeccionan/validan, no se generan destinos arbitrarios» — el alcance incluye un comportamiento (inspección/validación de materializaciones) que la aceptación no recoge: no dice qué se valida, contra qué contrato ni cómo se comprueba. Obligaría a inventar resultado y criterio de aceptación, o a decidir si queda fuera.
2. «cada capability no soportada se declara no disponible y bloquea ese escenario» — «ese escenario» no está delimitado: puede ser la capability concreta, UF03 o el gate WS30. Obligaría a inventar el alcance del bloqueo y su efecto sobre la validación.


### WS43 [3]
1. «Persona designada recorre Markdown y UI real»: no se identifica quién designa ni qué persona acepta. Obligaría a inventar el actor de aceptación y quién firma/commitea el acta.
2. «Repos a enlazar = `deskops list repositories`» frente a «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: no queda claro si todos los repos listados pueden enlazarse en WS43 o solo los que ya tengan tarea/acuerdo. Obligaría a inventar el criterio de inclusión y si hay que abrir tareas antes.
3. «links/roots verificables»: no se define qué es un `root` ni qué hace verificable un enlace. Obligaría a inventar el criterio de aceptación y el método de comprobación.

