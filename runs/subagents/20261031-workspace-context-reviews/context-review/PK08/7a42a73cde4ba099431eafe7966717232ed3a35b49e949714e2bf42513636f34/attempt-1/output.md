## REFORMULACION
**Propósito:** revisar PK08 como encargo de planificación: agrupación de revisión del ramal Scion opcional, no una dependencia operativa.
**Resultado:** veredicto de revisión de PK08; no código ni ejecución de hijos.
**Repo:** deskops (ruta de `context_review.py` y disposición); hijos con repos deskops/graph_ui.
**Límites:** no revisar los bloques edge vecinos; no evaluar producto; no promover hijos; PK08 no se ejecuta, termina cuando sus hijos tienen revisión vigente o bloqueo explícito con responsable.

## AMBIGUEDADES
1. «hash de input y de contrato coinciden con los actuales»  
   No se define qué artefacto es el «contrato» ni cómo se calcula su hash. Si `context_review.py` no lo fija, el ejecutor debe inventar qué se compara (bloque edge, nodo del DAG u otro).

2. «por causa externa (ajena al encargo del propio hijo)»  
   Falta el criterio para separar causa externa de ambigüedad propia. El ejecutor tendría que inventar el límite que permite admitir un bloqueo como externo.

3. «revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable»  
   El alcance del «o» es ambiguo: ¿un hijo bloqueado satisface la condición aunque su revisión no sea vigente, o la vigencia sigue siendo exigida? Obliga a inventar la lógica del gate.

## DRY-RUN
- **Lecturas previstas:** nodo PK08 y aristas de WS32–WS38/WS44; guía; brief, alcance, decisiones, cobertura; referencia a `context_review.py` (sin ejecutarlo).
- **Cambios previstos:** ninguno en código ni en dag.yaml; solo disposición de revisión de PK08.
- **Dependencias:** herramienta de estado en la ruta indicada; disposiciones de los ocho hijos; hashes vigentes.
- **Validaciones futuras:** ejecutar `context_review.py status` desde la raíz de deskops; comprobar coincidencia de hashes y existencia de disposition.md; verificar responsable y dependencia en bloqueos explícitos.

## FUTURO
La sesión de coordinación ejecuta `context_review.py`, registra bloqueos y responsables. El humano resuelve Pxx y G_PRODUCT; WS07 designa operador Scion y su acceso read-only. Las promociones de los hijos producen sus revisiones; este nodo no las sustituye.
