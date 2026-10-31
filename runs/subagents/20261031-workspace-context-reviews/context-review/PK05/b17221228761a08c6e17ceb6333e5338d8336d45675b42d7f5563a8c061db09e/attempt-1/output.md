REFORMULACION
Propósito: agrupar la revisión de autoría y operación manual, no ejecutar una entrega. Resultado: PK05 es verdadero cuando cada hijo directo (WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30, WS42) tiene revisión vigente o bloqueo externo con responsable y dependencia registrados. Repo dueño: no aplica; es una agrupación de revisión, no un entregable ejecutable. Límites: no revisar los nodos hijos ni sus bloques edge; no aprobar Pxx; no ejecutar comandos.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y nodo PK05 con su lista de hijos; los bloques edge se usan solo como contexto y no se revisan. Cambios previstos: ninguno sobre archivos; solo emitir esta revisión. Dependencias: el `context_review` de cada hijo, sus hashes de input y contrato, la `disposition.md` del intento correspondiente y el comando de estado. Validaciones futuras: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; comprobar por hijo que los hashes coinciden y que existe disposition guardada; admitir un bloqueo solo si `context_review.status=blocked`, la causa es externa al encargo del hijo y constan responsable y dependencia. No se ejecuta ahora.

FUTURO
Cada sesión de context review de un hijo produce su disposition; la sesión de coordinación registra bloqueos externos; WS07 y las personas responsables resuelven las decisiones Pxx; WS12 produce el contrato de operaciones. El comando de estado confirmará o no la aceptación de PK05. Nada de esto es ambigüedad del encargo actual.
