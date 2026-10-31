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

### WS09 [2]
1. «Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado» exige "contrato" por fila, pero brief.md dice que un documento «puede tener contrato estructurado o no» y vistas.md incluye «Issue Markdown sin modelo». No se aclara si "contrato" admite "sin contrato/no aplica" o exige modelo/contrato a filas Markdown, Code, issue o FAQ. Obligaría a inventar un contrato o a incumplir la aceptación.
2. «error = fallo visible esperado para esa fila» no define clase ni fuente del fallo: ¿error de UI, operación no soportada, backend/CDN, contrato ausente? Obligaría a inventar el error esperado y haría desigual la comprobación.

### WS11 [3]
1. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk.» No se indica quién autoriza aliases/roots multidesk, dónde se declaran ni qué formato tienen. Obligaría a inventar la fuente de autorización y su responsable, afectando a WS41.
2. «Clasificar huecos sin modelos hipotéticos.» No hay criterio para decidir qué modelo es hipotético, pese a que el glosario admite modelo opcional y nodos no Markdown. Obligaría a inventar el límite entre hueco real y modelo supuesto.
3. «El acta de G_UI_READ enumera sus scope_nodes […] el acta de G_SPEC_VIEW enumera los suyos», pero `output_scope` solo nombra `contratos/navegacion.md`. Obligaría a inventar ubicación y formato de ambas actas o a decidir si van dentro del contrato.

### WS12 [3]
1. «Aceptar el delta de escritura … por graph_ui antes de cerrar; aceptar delta en sldb…» No se define qué acto o tarea materializa esa aceptación ni qué ocurre si no llega o se rechaza. Obligaría a inventar el procedimiento de aceptación y su efecto sobre el cierre.
2. «operaciones de autoría/cierre quedan bloqueadas por G_CLOSEOUT»: «autoría» puede referir a autoría de tareas (WS26) o a edición de fuente (WS20/21). Obligaría a decidir qué operaciones bloquea G_CLOSEOUT frente a G_SOURCE.
3. «clasifica APIs como existentes/comprobadas o faltantes»: no fija criterio ni evidencia mínima de «comprobada». Obligaría a inventar el baremo de verificación.
