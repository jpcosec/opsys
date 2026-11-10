REFORMULACION
Propósito: sustituir el cierre en Python por reglas declarativas — RuleDocs semilla `on_transition` sobre `task_completes` (where `current_node = "ritual-testing"`) que exigen los recibos evidence de CC33a, reglas de campo como `alert`, borrado de `closeout_evidence_verified`, `pill_graduation_verified`, `__closeout_evidence__` y `_add_closeout_facts`, y reubicación de los 9 chequeos de CC38. Resultado: cierre gobernado por datos, grep vacío, goldens idénticos, doctor sin hallazgos, docs y CHANGELOG. Repo: deskops (worktree, robocop2). Límites: fuera grafo (CC33c), selectores/escrituras y tags por API de sldb (DO7); nada a mano en `desk/`. Es tarea `task.code` ejecutable, sin hijos: no es agregado.

AMBIGUEDADES
1. «cada una pasa a RuleDoc o queda con razón escrita» frente a la aceptación «los 9 chequeos de CC38 como RuleDoc con su función vieja borrada»: el criterio de qué queda como hipótesis no se da; obligaría a inventar la partición.
2. «si la RuleDoc necesita la API de tags de sldb… si se expresan con el lenguaje de reglas sin esa API»: exige decidir la expresividad del lenguaje de reglas; no consta en el input.
3. «Este nodo decide y deja escrito en el TaskDoc si closeout commit escribe los recibos antes de evaluar la regla»: la decisión sí/no no viene dada.
4. «la regla lo contempla (p. ej. or con el caso exento) o pide otro value; la elección va en el TaskDoc»: elección no especificada.
5. «usa el recibo kind goldens de deskops review record (follow-up de CC32) si existe»: existencia condicionada, no verificable con este input.
6. «las reglas sobre campos pasan a RuleDocs on_check/on_write alert (vocabulario de closeout_evidence, código implícito…)»: no se da el predicado de cada regla; habría que inventarlo.

DRY-RUN
Lecturas: TaskDoc, rituales del Board, `deskops/data/rules/rule-activation-*`, `data/lifecycle/closeout-task_completes.md`, `services/tasks.py:202-203,307`, `services/closure.py:836-837,1094`, `cli/commands/operations.py:44`, `models/task_types.py`, inventario CC38. Cambios previstos: nuevas RuleDocs semilla y su declaración; quitar `has(closeout_evidence_verified)` de la arista; borrar hechos y `_add_closeout_facts`; migrar chequeos; tests, docs, CHANGELOG. Dependencias: CC33a en main (6d133045), sldb con RuleDoc/GO08, recibos evidence. Validaciones futuras: pytest por archivo desde /dev/shm, test_cli, goldens help/output idénticos, grep vacío de los cuatro nombres, doctor en 6 desks, `desk update --apply` idempotente, 4 pasos en clon limpio.

FUTURO
Las decisiones de a2/DO6 y las hipótesis las valida el supervisor; CC33c integra el grafo; DO7 resuelve #3/#5; CC32 aporta el recibo goldens.
