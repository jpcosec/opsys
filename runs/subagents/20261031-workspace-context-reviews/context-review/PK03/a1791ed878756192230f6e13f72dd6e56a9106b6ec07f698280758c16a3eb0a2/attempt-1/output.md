REFORMULACION
Propósito: revisar PK03 como encargo de planificación: agrupación de revisión de lector, búsqueda, errores, corpus, lectura entre desks y validación humana temprana. Resultado: PK03 será verdadero cuando cada hijo directo (WS13, WS14, WS15, WS16, WS40, WS41) tenga revisión vigente sin ambigüedad de su propio encargo o un bloqueo externo con responsable y dependencia registrados; se comprueba con `context_review.py status`. Repo: PK03 no declara `owner_repo`; al ser agrupación de revisión no ejecutable, no produce entrega propia. Límites: no es dependencia operativa, no implementa, no sustituye la revisión de los hijos y no revisa los contratos de los vecinos.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: definición de PK03 en dag.yaml; salida de `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; `disposition.md` de cada hijo en el intento correspondiente a los hashes vigentes. Cambios previstos: ninguno. Dependencias: revisiones de WS13, WS14, WS15, WS16, WS40 y WS41; no hay ejecución de hijos ni de sus entregas. Validaciones futuras: comprobar coincidencia de hash de input y de contrato, existencia de `disposition.md`, ausencia de ambigüedad propia y, si hay bloqueo, que sea externo y tenga responsable y dependencia.

FUTURO
Cada hijo produce su `context_review`/`disposition.md`; la sesión de coordinación ejecuta `context_review.py` y registra bloqueos externos con responsable. No hay decisión humana específica en PK03 ni entregable propio.
