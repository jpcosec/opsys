### WS13.3 [3]
1. «Volver sigue el orden inverso de navegación.» No define qué acciones crean entrada de historia: ¿abrir documento, cambiar de pestaña, activar una división o varias? Obliga a inventar qué apila y desapila “volver”, y por tanto el criterio comprobable de historia.
2. «Pestañas, dos documentos lado a lado» no aclara si cada división tiene su propio conjunto de pestañas o si hay uno global. Obliga a inventar el modelo de disposición y cómo se abren/cierran pestañas entre divisiones.
3. «Abrir, cambiar y cerrar pestañas» no define qué documento queda activo al cerrar la pestaña activa ni si se permite cerrar la última. Obliga a inventar una transición de estado que la aceptación no cubre.

### WS14 [2]
1. Contradicción entre scope y acceptance. Cita: «Sin resultados/error/degradación diferenciados.» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». Obliga a inventar si el ejecutor debe diferenciar esos estados o, por el contrario, no hacerlo.  
2. Criterio de aceptación no comprobable. Cita: «no cargar todo grafo en cada tecla». Obliga a inventar qué cuenta como «todo grafo», cómo se observa y qué umbral o instrumentación valida el cumplimiento.

### WS16 [1]
1. «Fallos abren tarea de corrección en el repo dueño»: no se identifica el repo dueño por tipo de fallo ni quién crea la tarea. Obliga a inventar si la corrección corresponde a `graph_ui`, `deskops` o `sldb/pron`, y si WS16 debe abrirla pese a `promotion: not_authorized`.

### WS17 [3]
1. **Alcance del contenido y cobertura de repos.** El título dice «entradas e índices del desk ejemplo» (singular), la aceptación exige resolver «los dos desks del manifiesto WS40» y cobertura.md asigna a WS17 índices para UF10, cuyo corpus incluye «un tercer repo temporal sin desk». Obliga a inventar si las plantillas cubren uno, dos o tres repos y qué índices mínimos son exigibles.
2. **Criterio de éxito ante la referencia rota deliberada.** La aceptación pide «recorrer links Markdown sin UI», mientras WS40 incluye «referencia rota» como parte del corpus. Obliga a inventar si esa referencia debe quedar rota, excluirse del recorrido o documentarse como error esperado; sin ello, «recorrer links» no fija aceptación comprobable.
3. **Soporte de la procedencia.** «Mostrar el root/store de procedencia al resolver los dos desks» no dice si se muestra en las propias plantillas, en un acta o en la salida del generador. Obliga a inventar dónde y cómo se materializa ese requisito.

### WS18 [2]
1. **«Vista portable renderiza sobre un store real»**: no hay definición de “portable” en brief, alcance ni glosario. Obliga a inventar el criterio de portabilidad —entre stores, hosts o formatos— y, por tanto, cuándo la aceptación se cumple.
2. **«para selecciones y notación ya soportadas»**: no se indica dónde queda fijado qué selecciones y notaciones están soportadas. WS09 inventaría renderizaciones y advierte que «ViewDoc es grafo, no contrato universal de UI»; WS11 cierra navegación e identidad, no un catálogo de notación. Obliga a inventar el conjunto exacto y el alcance de lo declarable.

### WS22 [1]
1. «estados y gates leídos de deskops (Board, lifecycle)». Las fuentes no definen qué es un “gate” de deskops ni qué operación de Board/lifecycle lo expone; “gates” solo aparece como G_* de `dag.yaml`, que la propia frase excluye. Obligaría a inventar la fuente y la semántica de los gates mostrados.

### WS24 [3]
1. **Cobertura de aceptación incompleta.** El scope exige «clasificación y vecindad» y define «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops», pero la aceptación solo exige «Navegación ida/vuelta por fuentes y backlinks derivados» y el caso Markdown no modelado. Obliga a inventar si clasificación y vecindad deben probarse o solo mostrarse.
2. **«crossroads» sin definición suministrada.** Aparece en «átomos/protoátomos/crossroads (inventariados en WS02 y catalogados en WS09)», pero no está definido en brief ni glosario. Aunque WS09 lo catalogue, el nodo no fija qué entidad es ni qué representación mínima debe tener; el ejecutor tendría que inventarlo antes de esa dependencia.
3. **Alcance del Code local impreciso.** «preservar Code local del ticket workspace en draft que identifique el acta WS11» no fija si el nodo debe implementar Code o solo conservarlo; obliga a decidir el límite de cambios en esa proyección.

### WS40 [1]
1. **Esquema del manifiesto**: «imprime un manifiesto JSON con roots, stores, commits y documentos clave». No se fijan nombres de campos, tipos, rutas relativas/absolutas ni qué documentos son «clave». El ejecutor tendría que inventar un contrato de facto que WS16/WS30/WS17 consumirán; la aceptación solo enumera categorías, no una estructura verificable de intercambio.
