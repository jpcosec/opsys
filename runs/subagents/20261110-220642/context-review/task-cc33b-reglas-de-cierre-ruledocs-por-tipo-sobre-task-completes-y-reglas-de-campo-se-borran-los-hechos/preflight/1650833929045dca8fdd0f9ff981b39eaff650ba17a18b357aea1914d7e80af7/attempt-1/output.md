REFORMULACION
Propósito: sustituir en deskops el cierre por hechos y gates Python por RuleDocs semilla por tipo sobre la arista `task_completes`, y pasar las reglas de campo a RuleDocs alert. Resultado: reglas que exigen los recibos evidence de CC33a, tabla de kinds, borrado de `__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified` y `_add_closeout_facts`, chequeos de CC38 migrados o justificados, más tests, goldens, docs, CHANGELOG y ritual. Repo: deskops, worktree en robocop2. Límites: fuera grafo (CC33c), selectores/escrituras y tags por API sldb (DO7); no cambia el formato del desk ni la gramática CLI; nada a mano en `desk/` fuera de `drawer/`.

AMBIGUEDADES
1. "los 9 chequeos de CC38" (Goal, Done When) frente a b1: "8 filas: 3, 5, 13, 14, 15, 18, 24 y 25". Obliga a inventar si falta un noveno o cuál es.
2. "pasan a RuleDoc o quedan con razón" no fija criterio en el contrato; b5 lo define por expresividad. Sin b5 habría que inventarlo.
3. "editar goal tras verificar vuelve a bloquear": no se dice qué invalida el recibo (`anchor_state`/contrato). Habría que inventar la semántica de anclaje.
4. "goldens idénticos" frente a b8: "el worker para y avisa con el diff". No se aclara qué hacer si el mensaje cambia por diseño.
5. "una RuleDoc semilla ... por tipo": no enumera los tipos; hay que tomarlos de `task_types.py:41-105`.
6. "deskops doctor sin hallazgos nuevos" sin línea base explícita en Done When; b9 la define.

DRY-RUN
Lecturas: contrato, `task_types.py:41-105`, `rule-activation-*`, `lifecycle/closeout-task_completes.md`, `closure.py`, `tasks.py`, `operations.py`, informe CC38, ritual. Cambios previstos: crear `closeout-evidence.yaml` y `rule-closeout-task-<tipo>.md`; borrar hechos/gates y limpiar grep; migrar las 8 filas; editar ritual vía deskops; docs/CHANGELOG/tests. Dependencias: CC33a en main, `sldb rules explain`, `review record --kind goldens`. Validaciones futuras: pytest por archivo, goldens sin `--update`, doctor en 6 desks, 4 pasos del workflow, grep vacío, bloqueo/rebloqueo.

FUTURO
El supervisor corre la suite completa sobre lo integrado y decide goldens; el coordinador fija worktree, corre los 4 pasos y la línea base; sldb recibe nota de inbox y H1 (DO7) para #5; humano/coordinador resuelve hipótesis de `children` y exenciones.
