## REFORMULACION

**Propósito:** revisar PK08, agrupación de revisión del ramal Scion opcional, como encargo de planificación; no evaluar el producto ni ejecutar.

**Resultado:** confirmar si PK08 se entiende como agregado cuya verdad depende de que cada hijo directo (WS32–WS38, WS44) tenga revisión vigente sin ambigüedad de encargo o bloqueo externo con responsable registrado.

**Repo:** deskops (plan en `desk/drawer/plans/workspace-documental/`); sin implementación.

**Límites:** no revisar bloques edge de vecinos; no promover nodos; no resolver Pxx; no ejecutar `context_review.py`.

## AMBIGUEDADES

Ninguna. La aceptación define el criterio (revisión `context_review` vigente por hash de input y contrato; disposition guardada en el intento correspondiente; bloqueo externo con responsable y dependencia), nombra la herramienta de comprobación y distingue bloqueo propio de externo. El scope enumera las materias de los ocho hijos y coincide con ellos.

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura; nodo PK08 y bloques edge WS32–WS38, WS44 en `dag.yaml`; para cada hijo, su entrada `context_review`, hashes de input/contrato y `disposition.md` del intento correspondiente bajo `runs/subagents/20261031-workspace-context-reviews/context-review/`; salida de `context_review.py status` (solo como referencia, sin ejecutarla aquí).

**Cambios previstos:** ninguno en plan, dag ni repos. Solo el artefacto de revisión de PK08 (disposition del intento).

**Dependencias:** WS07 (designación del operador Scion y acceso read-only, `source_mode`), WS05 (inventario), WS12 (`G_WRITE_CONTRACT`), gates `G_SCION`/`G_EXEC`/`G_PRODUCT` en hijos; revisiones de WS32–WS38 y WS44 producidas por sus nodos de revisión.

**Validaciones futuras:** coincidencia de hash de input y contrato por hijo; existencia de `disposition.md` en el intento correcto; clasificación de bloqueos; estado global vía `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops.

## FUTURO

- WS07: el solicitante designa operador Scion, su acceso read-only y responsables de repos.
- WS44: el operador ejecuta el probe real y produce evidencia de `G_SCION`.
- Otros nodos de revisión emiten dispositions de WS32–WS38 y WS44; PK08 solo las agrega.
- Promoción/TaskDoc y aceptación humana de Pxx quedan fuera de este nodo.
