## REFORMULACION

**Propósito.** Que el cierre de cada tipo de tarea lo decida una RuleDoc semilla `on_transition` sobre la arista `task_completes` (en `ritual-testing`) exigiendo los recibos `evidence` de CC33a; que las reglas de campo pasen a RuleDocs `alert`; y que se borren los hechos y gates viejos (`__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified`, `_add_closeout_facts`).

**Resultado.** RuleDocs `rule-closeout-task-<tipo>.md` en `deskops/data/rules/`, tabla `closeout-evidence.yaml`, arista sin `has(...)`, chequeos de CC38 portados o eximidos con razón, grep de los cuatro nombres vacío, goldens idénticos, doctor sin hallazgos nuevos, ritual y CHANGELOG.

**Repo.** `deskops`. **Límites.** Fuera: grafo (CC33c), selectores/escrituras, tags por API sldb (DO7).

## AMBIGUEDADES

1. «los 9 chequeos de CC38» (Done When) frente a «el inventario … asigna a CC33 8 filas» (b1). Obliga a decidir el número; b1/c1 lo resuelven, pero el texto de aceptación sigue diciendo 9.
2. «message en español que nombra el tipo» (c2): no hay texto canónico; obliga a inventar la redacción salvo que se herede el mensaje del chequeo.
3. «los chequeos de CC38 como RuleDoc con su función vieja borrada» frente a b5/b6 (los no expresables quedan en código eximidos). Obliga a fijar qué filas se eximen.
4. «pasan a RuleDoc o quedan con razón» admite dos resultados por fila sin criterio cerrado; b5 lo cierra con `sldb rules explain`, que no está en el input.

## DRY-RUN

**Lecturas:** `task_types.py`, `services/closure.py`, `services/tasks.py`, `services/closeout_gates.py`, `lifecycle.py`, `data/lifecycle/closeout-task_completes.md`, `data/rules/rule-activation-*`, informe CC38, goldens help/output, baseline doctor de los 6 desks.

**Cambios previstos:** crear `rule-closeout-task-<tipo>.md` (subject `model <= <Clase>`, where `ritual-testing`, cláusulas `any(^subject: kind=evidence …)` por kind, atómico como `or`), crear `closeout-evidence.yaml` leída por closure y CLI, quitar `has(closeout_evidence_verified)` de la arista, borrar los cuatro nombres y `_add_closeout_facts`, portar/eximir filas CC38, editar `desk/rituals/closeout.md` (verify→commit), docs y CHANGELOG.

**Dependencias:** recibos de CC33a en main (6d133045), `review record --kind goldens`, `sldb rules explain`, DO7 para #3/#5.

**Validaciones futuras:** test de bloqueo con `fact="commit"` y re-bloqueo al editar `goal`; grep de los cuatro nombres; tests por archivo; goldens sin `--update-golden`; doctor comparado; 4 pasos del workflow en clon limpio.

## FUTURO

El coordinador fija 8 vs 9, aprueba o rechaza las hipótesis (children, filas eximidas), decide ante un diff de golden y envía la nota a sldb por DO7; el supervisor corre la suite completa sobre el resultado integrado.
