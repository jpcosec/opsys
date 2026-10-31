### WS13.1 [1]
1. La aceptación remite a «la matriz de WS09 y el contrato WS11», mientras `integration_mode` afirma «matriz WS06 llega de forma transitiva por WS11/WS12». Si son matrices distintas, el ejecutor debe inventar cuál define las representaciones soportadas y, por tanto, qué debe probar al alternar texto/graph/code. Cita: «en las representaciones que la matriz de WS09 y el contrato WS11 declaren soportadas».

### WS13.3 [3]
1. **Eventos que forman la historia.** Cita: «Cambiar de pestaña o división cambia el documento activo sin alterar el foco guardado de cada documento; volver restaura documento, foco y origen» y «Volver sigue el orden inverso de navegación». No define si cambiar pestaña/división, abrir un documento o seguir un enlace empujan historia; obligaría a inventar qué acciones son navegables.

2. **Efecto de cerrar pestaña.** Cita: «Abrir, cambiar y cerrar pestañas». No indica qué documento queda activo al cerrar la pestaña activa ni si se descartan su foco y su entrada de historia; obligaría a inventar la regla de cierre.

3. **Entrada de apertura y dependencia.** Cita: «Abrir documentos en pestañas y divisiones» con `output_scope` limitado a `layout/`. No nombra desde dónde se abren (enlaces de WS13.1, explorador de WS13.2) ni si WS13.2 es prerrequisito; obligaría a inventar interfaz de apertura o dependencia ausente.

### WS14 [2]
1. «resultados enlazan identidad y contexto». No define qué identidad ni qué contexto deben mostrarse/enlazarse, y la aceptación no lo comprueba. Obliga a inventar campos, enlace y criterio de verificación.
2. «Búsqueda vacía/error/degradación diferenciados» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». «Vacía» puede significar consulta vacía o ausencia de resultados. Obliga a decidir si hay un cuarto estado y cómo probarlo.

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

### WS41 [1]
1. «seguir enlaces authored del corpus entre desks». WS40 es el productor del corpus y de los dos stores, pero su alcance solo menciona Markdown no modelado, Code local, referencia rota y enlaces internos de la entrada mínima; no enumera enlaces authored entre desks. Esto obliga a inventar si WS41 debe crear esos enlaces en `tests/` —invadiendo el corpus— o si WS40 debe ampliarse, y cuál es el enlace exacto que prueba UF08.
