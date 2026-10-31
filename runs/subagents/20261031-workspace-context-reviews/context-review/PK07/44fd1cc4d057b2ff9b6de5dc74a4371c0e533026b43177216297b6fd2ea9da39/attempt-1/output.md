## REFORMULACION

**Propósito:** revisar PK07 como encargo de planificación: si su propósito, resultado, repo dueño, límites, dependencias y aceptación son comprensibles y comprobables. No se evalúa el producto ni se ejecuta nada.

**Resultado:** un juicio de revisión sobre PK07, no sobre sus hijos ni sobre los contratos edge de los vecinos. PK07 es un agregado de revisión: no se ejecuta; su aceptación depende de que WS29 y WS39 tengan revisión vigente o bloqueo explícito con responsable.

**Repo:** PK07 no declara `owner_repo` por ser agrupación; sus hijos pertenecen a `graph_ui`. La comprobación indicada se ejecuta desde la raíz de `deskops`.

**Límites:** no revisar los bloques edge de WS29/WS39; no tratar Pxx como aprobadas; no convertir trabajo futuro de los hijos en ambigüedad de PK07; no ejecutar `context_review.py`.

## AMBIGUEDADES

Ninguna.

La aceptación remite a un comando concreto (`context_review.py status`), define revisión vigente mediante coincidencia de hashes y presencia de `disposition.md`, y distingue bloqueo externo con responsable de ambigüedad sin resolver. No obliga al ejecutor de PK07 a inventar resultado, actor ni criterio de aceptación.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo PK07 y contratos edge de WS29/WS39), guía, brief, alcance, decisiones, cobertura y `context_review.py status` cuando corresponda.

**Cambios previstos:** ninguno en el plan; solo la disposición de revisión de PK07.

**Dependencias:** el script `context_review.py`, las revisiones de WS29 y WS39, sus hashes de input/contrato y sus `disposition.md`.

**Validaciones futuras:** ejecutar `status`; comprobar hashes actuales; verificar disposición guardada; aceptar `blocked` solo con responsable y dependencia registrados; confirmar que no hay ambigüedad pendiente en cada hijo.

## FUTURO

La sesión de coordinación ejecutará `context_review.py` y registrará cualquier bloqueo. Los nodos de revisión de WS29 y WS39 producirán sus disposiciones. La resolución de P08 y demás decisiones corresponde a un humano; no se produce aquí.
