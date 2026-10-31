### PK06 [1]
1. **“hash de input y de contrato”** — cita: «cuyo hash de input y de contrato coinciden con los actuales». No se define qué constituye el “contrato” cuyo hash se compara (¿bloque edge del hijo?, ¿TaskDoc?, ¿parámetros?). El ejecutor de la comprobación tendría que inventar el objeto hasheado; sin embargo, el propio input indica que `context_review.py status` lo comprueba, por lo que la invención queda delegada a la herramienta. No obliga a inventar al revisor de PK06.

Ninguna otra: hijos enumerados (WS31, WS43), criterio de verdadero/falso y tratamiento de bloqueo externo con responsable están definidos; el aggregate no requiere repo ni aceptación de producto propia.

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
