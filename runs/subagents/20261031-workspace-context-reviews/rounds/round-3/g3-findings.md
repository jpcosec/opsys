### WS19.1 [2]
1. «Delta sobre ticket draft de edición». No se identifica el ticket/Board receptor concreto; obligaría a inventar cuál es el ticket existente y su alcance exacto, pese a que `integration_mode` alude a un ticket draft.
2. «conflicto visible (mensaje de rechazo con el texto local conservado)» frente a la aceptación «una escritura obsoleta no pierde texto local». La aceptación no exige comprobar que el conflicto sea visible; obligaría a inventar el criterio de visibilidad y la evidencia que lo demuestra (sin fijar aquí textos de pantalla).

### WS25.2 [1]
1. «ambos tipos se registran y se muestran tras recargar». No queda claro si “ambos tipos” son los destinos —drawer/protoátomo— o los orígenes —ruta/mensaje—. Obligaría a inventar qué matriz debe registrarse y mostrarse, aunque el alcance exige probar cada destino por separado.

### WS26.2 [4]
1. «representación de capa lista por dependencias/no solapamiento» frente a una aceptación que solo exige «Tras enrutar, `deskops show board` muestra la tarea». Falta criterio comprobable de la capa lista; obligaría a inventar su verificación y prueba.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc» no define qué ocurre con `files` vacíos o ausentes, ni si el solapamiento es por ruta exacta, prefijo o directorio. Obligaría a inventar la regla.
3. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real» no aclaran si WS26.2 implementa promoción o solo prepara handoff, ni cómo se comprueba «estado real». Obligaría a inventar alcance y evidencia.
4. «dependencias pendientes» remite al «ritual de fase», pero no se aporta qué estados cuentan como pendientes ni cómo mapearlos desde deskops. Obligaría a inventar esa semántica.

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

### WS42 [3]
1. **«las materializaciones existentes se inspeccionan y validan contra el modelo SLDB vigente»** — no se nombra artefacto, versión, repo ni nodo que produzca ese modelo. Obligaría a inventar cuál es la fuente autoritativa y cómo determinar su vigencia.
2. **«se inspeccionan y validan»** — no define resultado observable ni criterio de validación (¿mostrar, informar, bloquear?) ni qué ocurre si la validación falla. Obligaría a inventar la aceptación concreta de esa parte.
3. **«que ve el alcance y la procedencia antes de ejecutar»** — no fija qué información mínima debe verse ni cómo se comprueba en la aceptación, que no menciona esta confirmación. Obligaría a inventar contenido y verificación.

### WS43 [1]
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» / «Repos a enlazar = todos los de `deskops list repositories`» / aceptación: «un enlace es verificable si resuelve a un path existente del repo enlazado». Si un repo listado carece de «entrada existente» o de path local, no se dice si omitirlo, enlazar su raíz o detenerse; el ejecutor tendría que inventar la excepción.
