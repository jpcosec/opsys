REFORMULACION
GC05 es un nodo de entrega ejecutable (no agregado) del plan gates-por-tipo, repo deskops. Propósito: que init y `desk update --apply` escriban en `desk/rules/` la regla común de dependencias y una `RuleDoc` `on_transition` por tipo de fábrica con recibos, y que `advance` explique el bloqueo con `edges_blocked`; produce `G_CONSUMER`. Resultado: reglas idempotentes, `add rule --type`, findings en `advance`/`show`/`next`, test de integración de `G_CONSUMER` y nota a sldb. Límites: no reimplementa el evaluador en Python; no toca sldb salvo `deskops message send`; no autentica; `closeout_evidence_verified` sigue siendo hecho de deskops.

AMBIGUEDADES
1. "condition = conjunción de any(...) por cada kind de __activation_receipts__ del tipo" frente a "task.refactor pasa por la regla de task.code (preflight + bundle) y por la suya (goldens)" y "desde __activation_receipts__ del tipo menos los kinds que ya exigen sus ancestros". Obliga a inventar si las reglas de fábrica exigen todos los kinds declarados o solo el delta sobre ancestros; cambia `task.refactor` y `add rule`.
2. "add rule --type task.code.cli en un desk con ese tipo genera una RuleDoc válida" no dice qué kinds suma `task.code.cli` ni qué condición esperar si no suma ninguno; obliga a inventar el escenario y el contenido válido (posible conjunción vacía).
3. "explicación de GO02 con cláusula, nodo y valor visto" atribuye a GO02 (contrato/hash) los campos de finding que `G_SLDB_EVAL` describe como `node, holds, clause, seen`; obliga a decidir si es errata por GO08 o un formato adicional.

DRY-RUN
Leería dag/brief/decisiones, GC01 (`task_types.py` y `__activation_receipts__`), GC02 (`ReviewDoc`), GC04 (`effects` y `advance`), `lifecycle.py`, `tasks.py`, `operations.py`, registry, `workspace.py`, `desk/rules` y tests. Crearía `desk/rules/activation-depends-on.md` y `activation-<tipo>.md`; haría init/`desk update` idempotentes; añadiría `add rule --type` con resta de ancestros; modificaría `advance` para consultar `edges_holding` y volcar `edges_blocked` en el envelope; `show`/`next`; tests `G_CONSUMER` y por tipo; docs, CHANGELOG y `message send`. Dependencias: GC01, GC02 y GC04 cerrados; `G_SLDB_LANG`, `RULES`, `ANCHORS` y `EVAL` pinneados. Validaría con `sldb rules check`, pytest y los escenarios de acceptance.

FUTURO
sldb debe cerrar GO05–GO08 y deskops pinnear versión; GC01 fija `__activation_receipts__`; GC02 el `ReviewDoc`; GC04 `edges_holding`/`effects`. El dueño acepta la nota `G_CONSUMER` y el mensaje a sldb; GC03/GC08 consumen después.
