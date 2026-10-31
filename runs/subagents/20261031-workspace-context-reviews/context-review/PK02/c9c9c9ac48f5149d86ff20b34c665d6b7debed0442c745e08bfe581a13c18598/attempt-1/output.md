## REFORMULACION
- **Propósito**: revisar PK02 como agrupación de revisión de decisiones y contratos, no como tarea ejecutable.
- **Resultado**: PK02 será verdadero cuando cada hijo directo (WS07–WS12) tenga revisión vigente sin ambigüedad de encargo, o un bloqueo explícito con responsable.
- **Repo**: deskops; la comprobación se ejecuta desde su raíz con `context_review.py status`.
- **Límites**: no es dependencia operativa ni entregable; no ejecuta hijos; no sustituye decisiones humanas ni gates.

## AMBIGUEDADES
Ninguna. La aceptación remite a una comprobación concreta (`context_review.py status`), define revisión vigente por coincidencia de hashes y disposition.md, y distingue bloqueo externo con responsable. No exige inventar resultado, actor ni repo.

## DRY-RUN
- **Lecturas previstas**: nodo PK02 y sus hijos directos en `dag.yaml`; `context-review-guide.md`; `decisiones.md`, `alcance.md`, `brief.md`, `cobertura.md`; disposition.md de cada hijo en el intento correspondiente a sus hashes.
- **Cambios previstos**: ninguno; PK02 es agrupación de revisión.
- **Dependencias**: revisiones vigentes de WS07–WS12; estado `blocked` solo si es externo y tiene responsable y dependencia registrados.
- **Validaciones futuras**: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; comprobar por hijo hash de input/contrato, disposition.md y, si aplica, responsable del bloqueo.

## FUTURO
La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos externos con responsable. Los revisores de cada hijo resuelven ambigüedades propias o emiten disposition.md. Las decisiones P01–P09 y los gates G_PRODUCT/G_WRITE_POLICY quedan para el humano y WS07; este nodo no los aprueba ni autoriza ejecución.
