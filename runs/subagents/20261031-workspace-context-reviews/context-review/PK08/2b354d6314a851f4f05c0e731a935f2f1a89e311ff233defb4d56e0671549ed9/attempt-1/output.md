## REFORMULACION

**Propósito:** PK08 es una agrupación de revisión del ramal Scion opcional; no ejecuta trabajo ni sustituye la aceptación de producto. Su función es declarar si todos sus hijos directos están revisados o bloqueados explícitamente.

**Resultado:** PK08 es verdadero cuando cada hijo directo tiene `context_review` vigente sin ambigüedad de encargo, o un `status=blocked` con responsable y dependencia registrados en su `disposition.md`.

**Repo:** deskops, por `dag.yaml`, `context_review.py` y las disposiciones de revisión. Los hijos pertenecen a deskops y graph_ui, pero PK08 no ejecuta sus entregas.

**Límites:** agrupación no ejecutable; no autoriza implementación, no aprueba el producto Scion, no resuelve decisiones Pxx ni satisface gates por inferencia.

## AMBIGUEDADES

Ninguna.

La aceptación define resultado comprobable (`context_review.py status`, coincidencia de hashes de input y contrato, existencia de `disposition.md`) y distingue bloqueo propio de bloqueo externo con responsable. El alcance enumera los hijos directos. No hay repo o actor ausente para ESTE nodo, porque PK08 no ejecuta y sus hijos son revisados por otros nodos.

## DRY-RUN

**Lecturas previstas:** nodo PK08 y sus hijos WS32–WS38 y WS44 en `dag.yaml`; sus `disposition.md` e intentos; estado reportado por `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops.

**Cambios previstos:** ninguno durante esta revisión. La sesión de coordinación podrá guardar la disposición de PK08; no modifica nodos ni estados de hijos.

**Dependencias:** revisiones vigentes de los ocho hijos directos; para WS44, designación del operador en WS07 y probe read-only; gates declarados por los hijos (`G_SCION`, `G_EXEC`, `G_WRITE_CONTRACT`, `G_UI_READ`, `G_UI_WRITE`, `G_HUMAN_DELEGATE`, `G_PRODUCT`).

**Validaciones futuras:** ejecutar `status`; comprobar hash de input y contrato de cada hijo; verificar `disposition.md` guardada; para bloqueos, confirmar responsable y dependencia registrados; no interpretar `completed` como aprobación.

## FUTURO

La sesión de coordinación registra la disposición de PK08 y su resultado agregado. Los revisores de cada hijo producen o actualizan sus revisiones. WS07 designa al operador Scion y registra su acceso read-only; WS44 produce el recibo de probe. Un humano decide las Pxx y gates de producto. Ninguna de esas decisiones se sustituye desde PK08.
