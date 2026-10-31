REFORMULACION  
PK03 es una agrupación de revisión, no una tarea ejecutable. Propósito: comprobar que cada hijo directo (WS13, WS14, WS15, WS16, WS40, WS41) tiene revisión vigente sin ambigüedad de encargo o con bloqueo explícito y responsable. Resultado: que PK03 sea verdadera solo bajo esa condición, comprobable con `context_review.py status`. Repo: no tiene `owner_repo` ni entrega propia; agrupa nodos de graph_ui y deskops. Límites: no ejecuta hijos, no valida producto, no sustituye aprobación humana, no resuelve Pxx, no revisa contratos de vecinos ni modifica el DAG.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas: `input.md`, `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `dag.yaml` (PK03 y edges de sus hijos; los edges no se revisan).  
Cambios previstos: ninguno en archivos del plan; no se modifica `dag.yaml` ni los nodos hijos.  
Dependencias: las revisiones/dispositions vigentes de los seis hijos directos; PK03 no declara `depends_on` operativo.  
Validaciones futuras: ejecutar desde la raíz de deskops `python desk/drawer/plans/workspace-documental/context_review.py status`; comprobar por hijo hash de input/contrato actuales, `disposition.md` guardada en su intento y, si aplica, `blocked` con responsable y dependencia.

FUTURO  
La sesión de coordinación ejecuta el script y registra bloqueos; otros revisores producen las dispositions de los hijos; el humano resuelve Pxx o bloqueos externos. Esta revisión no decide la aceptación de PK03 ni de sus hijos.
