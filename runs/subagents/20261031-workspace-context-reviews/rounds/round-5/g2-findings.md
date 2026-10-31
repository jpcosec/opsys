### WS14 [3]
1. «Sin resultados/error/degradación diferenciados.» Esta frase del scope puede leerse como que esos estados no deben diferenciarse, mientras la aceptación exige que «se ven como tres estados distintos». Obligaría a decidir si el scope niega o enumera los tres estados.
2. «resultados abren el documento con su identidad y ruta de origen» no se comprueba en la aceptación, que solo exige abrir/volver y conservar consulta/foco. Obligaría a inventar dónde se muestran identidad y ruta, o si basta con abrir el documento.
3. «no cargar todo grafo en cada tecla» no fija umbral ni forma de comprobación. Obligaría a inventar qué cuenta como “todo grafo” y cómo demostrar que no se carga en cada pulsación.

### WS17 [3]
1. «Mostrar el root/store de procedencia al resolver los dos desks del manifiesto WS40». No aclara si “mostrar” exige contenido concreto en las plantillas —formato, ubicación— o una comprobación/acta de aceptación. Obligaría a inventar el artefacto y podría exceder `documentation` hacia UI/renderer.
2. «recorrer links Markdown sin UI». No fija criterio ni método: ¿todos los enlaces deben resolver?, ¿solo los de los dos desks?, ¿inspección manual o script? El ejecutor tendría que inventar el umbral comprobable.
3. «source versionado y destino temporal no son registros independientes». No define observación verificable —identidad de contenido, ausencia de duplicados, hash—; obligaría a inventar cómo demostrarlo.

### WS22 [4]
1. «como tablero agrupado por estado y con las dependencias declaradas en el TaskDoc» — la tercera representación no define qué muestra (aristas, dirección, profundidad, agrupación, layout). Obligaría a inventar el diseño de la vista de dependencias; la aceptación solo exige que abra el mismo TaskDoc.
2. «abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados» — no se define qué cuenta como átomo referenciado por un TaskDoc ni cómo resolverlo. Obligaría a inventar el criterio de vinculación. (La guía excluye pills; no el criterio de átomos.)
3. «no duplicar tareas» — con tres representaciones simultáneas del mismo Board, no queda claro si prohíbe repetir una tarea entre lista y tablero o solo crear registros duplicados. Obligaría a decidir cuál de las dos lecturas aplicar.
4. «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml» — no se nombra qué canal/API las expone ni quién lo garantiza; `depends_on` solo incluye WS09 (que inventaría Board/ritual) y WS13. Obligaría a inventar la fuente o asumir disponibilidad.

### WS24 [3]
1. **Clasificación en soportes no modelados.** Cita: «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» y «La vista muestra la clasificación (tipo y tags)». No se define qué mostrar para Markdown sin modelo ni de dónde salen los tags si el modelo no los declara. Obliga a inventar si se muestran vacíos, se omiten o se leen del frontmatter.

2. **Uso concreto de WS18.** Cita: «Reutilizar el gráfico actual y una vista de documento genérica única registrada en shell/registry.js» junto con `depends_on: WS18`. El nodo no dice qué salida de WS18 consume —ViewDoc o NotationDoc— ni cómo condiciona el grafo o la vista. Obliga a inventar la integración o a ignorar la dependencia.

3. **Ubicación del soporte no modelado.** Cita: «un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista con su ruta de origen». No precisa si «la vista» es el grafo local o la vista de documento genérica. Obliga a inventar dónde debe aparecer y qué aceptación se prueba.

### WS40 [4]
1. «hace commits git reales en los repos temporales»: no fija identidad, rama ni mensaje de commit; obligaría a inventar configuración Git y política de commits.
2. «imprime un manifiesto JSON con roots, stores, commits y documentos clave»: no enumera qué documentos son «clave»; obligaría a elegir el conjunto exacto del manifiesto.
3. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «output_scope: tests/fixtures/workspace_documental/»: no aclara si se versiona el generador, una copia fixture o ambos; obligaría a decidir qué es artefacto y qué es efímero.
4. «Entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal»: no define si el Board se crea mediante CLI ni qué tareas contiene; obligaría a inventar su contenido.
