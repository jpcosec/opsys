REFORMULACION
Propósito: revisar que PK02, agrupación de revisión, tenga un encargo claro y una aceptación comprobable para sus hijos directos. Resultado: dictamen sobre el encargo; no produce capacidades ni ejecuta tareas. Repo: PK02 no declara `owner_repo`; según la guía, PK es agrupación de revisión y no entregable operativo. Límites: no evaluar el producto, no ejecutar, no revisar los contratos de los vecinos WS07–WS12 ni tratar propuestas Pxx como aprobadas.

AMBIGUEDADES
Ninguna. La aceptación fija la condición —revisión vigente por hijo o bloqueo externo con responsable—, nombra la fuente (`dag.yaml`), el artefacto (`disposition.md`) y el comando de comprobación (`context_review.py status`). Las expresiones «causa externa (ajena al encargo del propio hijo)» y «responsable (actor o repo que debe resolverla)» quedan acotadas por el registro exigido en `disposition.md`.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura y nodo PK02 en `dag.yaml`; no se revisan los bloques edge. Cambios previstos: ninguno; solo dictamen. Dependencias: revisiones vigentes de WS07–WS12, hashes de input/contrato, `disposition.md` y `python desk/drawer/plans/workspace-documental/context_review.py status`. Validaciones futuras: ejecutar `status` desde la raíz de deskops; comprobar coincidencia de hashes y disposition por hijo; admitir bloqueo solo si es externo, tiene responsable y dependencia registrada. Sin ejecución.

FUTURO
Cada hijo produce su `context_review`/`disposition.md` y sus hashes; la sesión de coordinación ejecuta el script y registra bloqueos externos con responsable; WS07 y el humano resuelven decisiones; la promoción/TaskDoc fija detalles. Nada de ello es ambigüedad de PK02.
