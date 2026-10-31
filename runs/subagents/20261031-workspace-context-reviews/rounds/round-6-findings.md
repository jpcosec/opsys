### PK02 [0]
ninguna.

### PK04 [0]
ninguna

El encargo queda comprobable: nombra el comando de verificación, define revisión vigente por coincidencia de hash de input y contrato, exige `disposition.md` en el intento correspondiente y distingue bloqueo externo (admisible con responsable) de ambigüedad propia del hijo (no admisible). Los hijos listados coinciden con el alcance declarado y ninguno es `aggregate`.

### PK05 [0]
Ninguna.

La aceptación de PK05 define el resultado, el mecanismo de comprobación, la fuente de verdad y el tratamiento de bloqueos. Los detalles de hashes, intentos y `disposition.md` quedan delegados al script nombrado y a las reglas comunes; no obligan a inventar al ejecutor de este nodo.

### PK06 [0]
Ninguna.

### PK07 [0]
ninguna

### PK08 [3]
1. «hash de input y de contrato coinciden con los actuales»  
   No se define qué artefacto es el «contrato» ni cómo se calcula su hash. Si `context_review.py` no lo fija, el ejecutor debe inventar qué se compara (bloque edge, nodo del DAG u otro).

2. «por causa externa (ajena al encargo del propio hijo)»  
   Falta el criterio para separar causa externa de ambigüedad propia. El ejecutor tendría que inventar el límite que permite admitir un bloqueo como externo.

3. «revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable»  
   El alcance del «o» es ambiguo: ¿un hijo bloqueado satisface la condición aunque su revisión no sea vigente, o la vigencia sigue siendo exigida? Obliga a inventar la lógica del gate.

### WS06 [3]
1. «Una matriz por implementación» frente a «agrupada por repo dueño, no por nodo del DAG». No queda definido si debe haber una matriz por repo o una sola matriz con secciones por repo, ni qué significa «implementación». Obligaría a inventar la unidad y estructura de entrega.
2. «ya cubierto (capacidad observable en código o en el Board, con referencia), extender ticket existente o nuevo delta». Un borrador del Board es observable, pero `reconciliacion.md` indica que no equivale a trabajo implementado. Falta el criterio para decidir si se clasifica como «ya cubierto» o como «extender ticket»; obligaría a inventar ese corte.
3. «Matriz con una fila por delta o capacidad propuesta». No delimita si el universo son todos los nodos del DAG o solo los que tocan repos externos; obligaría a inventar qué filas incluir.

### WS07 [0]
**Ninguna.** Las identidades, el acceso Scion, `source_mode` y la confirmación de P01–P09 son decisiones humanas pendientes, no datos que el ejecutor deba inventar. La aceptación exige registro con actor/fecha y prohíbe cerrar por inferencia.

### WS08 [0]
ninguna

### WS09 [2]
1. «Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado» exige "contrato" por fila, pero brief.md dice que un documento «puede tener contrato estructurado o no» y vistas.md incluye «Issue Markdown sin modelo». No se aclara si "contrato" admite "sin contrato/no aplica" o exige modelo/contrato a filas Markdown, Code, issue o FAQ. Obligaría a inventar un contrato o a incumplir la aceptación.
2. «error = fallo visible esperado para esa fila» no define clase ni fuente del fallo: ¿error de UI, operación no soportada, backend/CDN, contrato ausente? Obligaría a inventar el error esperado y haría desigual la comprobación.

### WS10 [0]
Ninguna.

Las posibles dudas quedan cubiertas por fuentes suministradas: el ejemplo fijo depende de P08 y de `G_PRODUCT`, que WS07 debe registrar; el manual CLI a reutilizar es `docs/operator-manual.md`; la auditoría WS02–WS04 está declarada como acceso transitivo; y las etiquetas se apoyan en el estado comprobado de WS02. Que `G_PRODUCT` siga pendiente es intencional, no un defecto del nodo.

### WS11 [3]
1. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk.» No se indica quién autoriza aliases/roots multidesk, dónde se declaran ni qué formato tienen. Obligaría a inventar la fuente de autorización y su responsable, afectando a WS41.
2. «Clasificar huecos sin modelos hipotéticos.» No hay criterio para decidir qué modelo es hipotético, pese a que el glosario admite modelo opcional y nodos no Markdown. Obligaría a inventar el límite entre hueco real y modelo supuesto.
3. «El acta de G_UI_READ enumera sus scope_nodes […] el acta de G_SPEC_VIEW enumera los suyos», pero `output_scope` solo nombra `contratos/navegacion.md`. Obligaría a inventar ubicación y formato de ambas actas o a decidir si van dentro del contrato.

### WS12 [3]
1. «Aceptar el delta de escritura … por graph_ui antes de cerrar; aceptar delta en sldb…» No se define qué acto o tarea materializa esa aceptación ni qué ocurre si no llega o se rechaza. Obligaría a inventar el procedimiento de aceptación y su efecto sobre el cierre.
2. «operaciones de autoría/cierre quedan bloqueadas por G_CLOSEOUT»: «autoría» puede referir a autoría de tareas (WS26) o a edición de fuente (WS20/21). Obligaría a decidir qué operaciones bloquea G_CLOSEOUT frente a G_SOURCE.
3. «clasifica APIs como existentes/comprobadas o faltantes»: no fija criterio ni evidencia mínima de «comprobada». Obligaría a inventar el baremo de verificación.

### WS13 [0]
Ninguna.

Las posibles dudas quedan cubiertas por fuentes suministradas: el contrato de navegación e identidad lo produce WS11 («contratos/navegacion.md»), el gate `G_UI_READ` tiene resolver y evidencia definidos, y los detalles de archivos, textos y pruebas se delegan al TaskDoc de promoción. La elección entre implementar o conciliar el ticket draft queda nombrada en WS13.1 («Si el acta de WS11 eligió integrar el ticket draft…»).

### WS16 [0]
ninguna

### WS17 [1]
1. «Registrar el root/store de procedencia al resolver los dos desks del manifiesto WS40; no duplicar el registry de deskops».
   Obliga a inventar el artefacto, formato y ubicación del registro: ¿va dentro de las plantillas versionadas, en un documento aparte o se relee del manifiesto WS40? Un root temporal no puede fijarse en plantillas reproducibles sin contradecir su materialización. La aceptación no define cómo comprobar ese registro ni quién lo produce.

### WS18 [2]
1. «no modificar su repo desde este plan» frente a «owner_repo: spec2viz» y «output_scope: sldb/views/ ... tests/». Obliga a inventar si la ejecución de WS18 puede escribir en spec2viz o solo preparar handoff; la frase puede leerse como prohibición de tocar el repo que el propio nodo declara como dueño.
2. «Vista portable (el mismo ViewDoc sin código específico del host) renderiza sobre un store real la selección declarada». No se nombra renderer ni harness, ni si WS18 debe construir uno; el scope solo habla de ViewDoc/NotationDoc y prohíbe UI pages. Obliga a inventar el medio de renderizado y el alcance del código de prueba.

### WS24 [3]
1. «Vecindad = hasta 2 hops.» No fija dirección ni tipos de arista: obliga a inventar si incluye relaciones entrantes, salientes o ambas, y si los backlinks cuentan dentro de la vecindad.
2. «es visible y navegable en la vista de documento genérica con su ruta de origen.» No define de dónde se obtiene esa ruta (ruta de archivo, identidad del store u origen declarado) ni qué mostrar si falta; obliga a inventar fuente y fallback.
3. «La vista muestra la clasificación (tipo y tags)» junto a «un soporte no modelado (Markdown sin modelo)», que no tiene tipo ni tags. No aclara si se muestra vacío, se omite o se etiqueta como no modelado; obliga a inventar ese estado.

### WS25 [0]
ninguna.

### WS25.2 [0]
ninguna

### WS29 [0]
Ninguna.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08»: el `depends_on` de WS30 no incluye WS08 ni se aporta su guion. Obliga a inventar esos escenarios o a asumir que WS08 estará disponible sin dependencia declarada.
2. «abre tarea en el nodo que lo causó»: no hay criterio para atribuir un fallo a un nodo cuando afecta a varios o su causa no es inequívoca. Obliga a inventar la atribución y el destino de la tarea.

### WS31 [0]
Ninguna.

### WS32 [0]
Ninguna.

### WS33 [0]
Ninguna. La aceptación del agregado es comprobable por la aceptación de sus hijos; el repo y el gate están identificados; el actor de G_SCION se designa en WS07 y lo produce WS44; los detalles de contrato, deduplicación y campos se delegan expresamente a WS33.1/WS33.2 o al TaskDoc. Que G_SCION esté `unverified` es intencional, no un defecto.

### WS33.1 [2]
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente… con la misma regla de deduplicación y procedencia». La única clave explícita es «Hub + proyecto + conversación + id de mensaje», aplicable a mensajes, no a resultados. El ejecutor tendría que inventar la clave de deduplicación de resultados o asumir que el identificador de fuente sustituye al de mensaje.
2. «un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco». No se define qué artefacto, campos ni comprobación materializan ese «hueco»; la aceptación solo cubre deduplicación y no atribuir una conversación completa. El ejecutor tendría que inventar el modelo/reporte de hueco y su evidencia.

### WS33.2 [0]
ninguna

### WS40 [0]
Ninguna. “Documentos clave”, “entrada mínima” y los nombres exactos de archivos/pruebas son detalles que el TaskDoc de promoción concretará dentro de la aceptación. `G_UI_READ` pendiente es un gate intencional, no un defecto.

### WS42 [2]
1. «con confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar». No se define qué compone “alcance” ni de dónde sale “procedencia”; el ejecutor tendría que inventar campos, fuente y criterio de presentación, y la aceptación quedaría no comprobable.
2. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea». No se identifica dónde está registrado ese modelo ni qué reglas determinan que una materialización sea válida o inválida; obligaría a inventar registro, versión y criterios de validación.

### WS43 [2]
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» — no define qué hacer si un repo de `deskops list repositories` carece de entrada existente: omitirlo, bloquear la publicación o abrir tarea. Obliga a inventar el resultado para ese repo.
2. «los acuerdos durables aplicados al mapa (Pxx aceptadas y contratos aplicables)» — «contratos aplicables» no fija criterio ni lista; obliga a inventar si comprende solo `navegacion.md`, también `operaciones.md` u otros de `contratos/`.

### WS44 [2]
1. «Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo.» No se nombra quién detecta el cambio ni con qué mecanismo, ni cuándo ese control deja de ser responsabilidad del operador. El ejecutor tendría que inventar una vigilancia o un disparador de revalidación. Cita: «Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo.»
2. «identidad del operador y Hub, fecha, capabilities y actor registrados.» «Actor» e «identidad del operador» pueden ser el mismo dato; la aceptación no distingue si el actor es quien ejecuta el probe o quien autoriza el acceso. Obligaría a decidir por cuenta propia qué campo distinto registrar. Cita: «identidad del operador y Hub, fecha, capabilities y actor registrados.»
