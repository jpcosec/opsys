## REFORMULACION

**Propósito:** agrupar la revisión del plan completo del workspace documental (lector temprano, autoría manual, publicación básica, extensiones y ramal Scion opcional) sin implementar producto ni resolver decisiones humanas.

**Resultado:** ROOT será verdadero cuando cada hijo directo (PK01–PK08) tenga revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable; además, `execution_authorized=false` y `validate_plan.py --check` en PASS.

**Repo:** no aplica a esta agrupación; no ejecuta ni produce entregables propios. El host concreto sigue pendiente en P01.

**Límites:** no implementa producto, no autoriza ejecución y no sustituye decisiones humanas.

## AMBIGUEDADES

1. «según `context_review.py status`» y «`validate_plan.py --check` en PASS»: no se indica ruta, repo ni forma de invocación de esas herramientas. Obliga a inventar dónde están y cómo se ejecutan.
2. «input y contrato actuales»: no define cuándo una revisión deja de ser vigente (hash, fecha, cambio de dag o de fuentes). Obliga a inventar el criterio de frescura.
3. «sin ambigüedad de encargo o bloqueo explícito con responsable»: no define qué disposición corresponde a ROOT si un hijo queda con ambigüedad pero sin `blocked`; obliga a inventar si ROOT falla, se bloquea o escala, y quién sería el responsable.

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `vision.md`, nodo ROOT y aristas PK01–PK08 (estas últimas solo como contexto, sin revisarlas).

**Cambios previstos:** ninguno; esta revisión no modifica `dag.yaml` ni otros archivos.

**Dependencias:** disposiciones de revisión de PK01–PK08, estado de `context_review.py`, resultado de `validate_plan.py --check` y valor `execution_authorized` en `dag.yaml`.

**Validaciones futuras:** consultar estado por hijo, comprobar `execution_authorized=false` y ejecutar `validate_plan.py --check`. Nada se ejecuta en este nodo.

## FUTURO

- Los revisores de PK01–PK08 emiten sus disposiciones.
- El humano resuelve P01–P09, designa responsables de repos y operador Scion.
- Otro nodo o persona ejecuta las comprobaciones de estado y validación.
- La promoción, TaskDoc y detalles de implementación quedan fuera de ROOT.
