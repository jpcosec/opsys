REFORMULACION
Propósito: ejecutar CC33b del plan deskops-como-config. Resultado: el cierre por tipo se decide con RuleDocs semilla `on_transition` sobre `task_completes`, que exigen los recibos evidence de CC33a; las reglas de campo pasan a RuleDocs `alert`; se borran los hechos y gates viejos; los chequeos de CC38 asignados pasan a RuleDoc o quedan con razón. Repo: deskops. Límites: fuera grafo (CC33c), selectores/escrituras y tags por API sldb (DO7); nada manual en `desk/` fuera de drawer ni en `.sldb/`; goldens idénticos; tests por archivo; worktree fijado por el coordinador.

AMBIGUEDADES
1. “los 9 chequeos de CC38 como RuleDoc con su función vieja borrada” frente a “el inventario de CC38 … asigna a CC33 8 filas” y “no hay que buscar un noveno”. Obligaría a inventar un noveno chequeo o a ignorar la aceptación.
2. “los 9 chequeos de CC38 como RuleDoc con su función vieja borrada” frente a “Los que quedan por b5 se listan en el informe con su razón y se eximen del grep”. Obligaría a inventar que todos migran y que ninguno queda exento.

DRY-RUN
Lecturas: TaskDoc, Board, ritual de closeout, pills/átomos ligados, informe de CC38, reglas y lifecycle actuales, tests/docs/goldens y línea base de `deskops doctor` en los 6 desks. Cambios previstos: añadir `deskops/data/rules/rule-closeout-task-<tipo>.md` y `closeout-evidence.yaml`; ajustar `task_types.py`, `operations.py`, `tasks.py`, `closure.py`, CLI y lifecycle; borrar `__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified` y `_add_closeout_facts`; migrar las 8 filas aplicables y las reglas de campo; actualizar tests, docs, ritual y CHANGELOG. Dependencias: recibos de CC33a, `verify` como productor, `RuleDoc`/`rules explain` de sldb, recibo `goldens` de `review record`, arista `task_completes` y store. Validaciones futuras: bloqueo por falta de recibo commit, reedición de `goal`, greps vacíos, tests de a uno, goldens, doctor y cuatro pasos del workflow.

FUTURO
El supervisor ejecuta preflight/bundle en frío, la suite completa y los cuatro pasos en clon limpio; el worker se detiene y avisa si un golden debe cambiar; el coordinador decide esa excepción y las hipótesis; DO7/CC33c y sldb resuelven después lo que queda fuera.
