REFORMULACION

Propósito: revisar PK08 («Ramal Scion opcional») como encargo de planificación, no como producto. Resultado: veredicto sobre si la agrupación y su aceptación son comprensibles y comprobables. Repo dueño: PK08 no declara `owner_repo` porque es agrupación de revisión no ejecutable; sus hijos pertenecen a deskops y graph_ui. Límites: solo input explícito; no ejecutar `context_review.py`, no editar `dag.yaml`, no revisar los bloques edge de los hijos, no tratar gates ni Pxx como aprobados, no implementar.

AMBIGUEDADES

ninguna.

DRY-RUN

Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y bloques de PK08/hijos. Cambios previstos: ninguno; solo el informe. Dependencias: estado de revisión de los 8 hijos directos (WS32–WS38, WS44), hashes de input/contrato y `disposition.md`; el comando de estado nombrado en la aceptación. Validaciones futuras, sin ejecutar: `python desk/drawer/plans/workspace-documental/context_review.py status`; comprobar revisión vigente de cada hijo y, si hay bloqueo, causa externa, responsable y dependencia registrada. La ausencia de `owner_repo` no es defecto por ser agrupación; los gates pendientes son intencionales.

FUTURO

La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos; los revisores de cada hijo emiten su `disposition.md`; WS07 designa operador Scion y acceso read-only; WS44 ejecuta el probe real; los gates G_PRODUCT, G_SCION y G_EXEC los resuelven humanos u otros nodos, no esta revisión.
