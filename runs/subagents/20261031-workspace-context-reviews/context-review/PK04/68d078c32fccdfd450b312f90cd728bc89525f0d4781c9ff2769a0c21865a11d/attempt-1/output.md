REFORMULACION
Propósito: agrupar la revisión de encargo de las entradas authored y las representaciones de Board, procedimientos, conocimiento y grafo, sin ejecutar trabajo de producto. Resultado: PK04 es verdadero solo si cada hijo directo —WS17, WS18, WS22, WS23, WS24— tiene `context_review` vigente, con hashes de input y contrato coincidentes con los actuales y `disposition.md` guardada en el intento correspondiente, o un bloqueo externo con responsable y dependencia registrados en esa disposición. Repo: deskops, según la ruta del script y su ejecución «desde la raíz de deskops»; el nodo no declara `owner_repo` ni `kind`, coherente con una agrupación de revisión no ejecutable. Límites: no revisa los contratos de los edges vecinos, no promueve hijos, no sustituye disposiciones ni decisiones humanas y no ejecuta nada.

AMBIGUEDADES
Ninguna. La aceptación define resultado, comprobación y excepción de bloqueo; el actor que verifica es «la sesión de coordinación que ejecuta context_review.py»; el repo queda identificado por la ruta del script; y la vigencia se delega explícitamente en `context_review.py status`, no en cálculo manual del revisor. La ausencia de `owner_repo`/`kind` no obliga a inventar porque PK04 no se ejecuta como entrega.

DRY-RUN
- Lecturas previstas: `dag.yaml` (PK04 y el `context_review` de cada hijo), `disposition.md` de cada intento y salida de `python desk/drawer/plans/workspace-documental/context_review.py status`.
- Cambios previstos: ninguno; PK04 no escribe archivos ni ejecuta hijos.
- Dependencias: las cinco revisiones de hijos; sus propios prerrequisitos (WS11, WS40, WS09, WS13, WS18, gates G_SPEC_VIEW/G_UI_READ) son contratos de vecinos y no se revisan aquí.
- Validaciones futuras: ejecutar el script desde la raíz de deskops cuando existan las disposiciones, contrastar hashes y comprobar que todo `blocked` tenga responsable y dependencia.

FUTURO
- Las revisiones de WS17, WS18, WS22, WS23 y WS24 las produce la sesión de coordinación; los bloqueos externos los resuelven los actores o repos designados.
- Las decisiones P01/P02/P04/P07/P08/P09 y el `source_mode` los confirma un humano en WS07.
- La promoción en repos receptores y los gates G_SPEC_VIEW/G_UI_READ corresponden a otros nodos y dueños.
