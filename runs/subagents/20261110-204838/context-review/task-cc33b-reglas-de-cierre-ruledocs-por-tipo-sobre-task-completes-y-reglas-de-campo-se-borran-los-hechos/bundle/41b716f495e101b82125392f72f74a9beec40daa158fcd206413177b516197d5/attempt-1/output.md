REFORMULACION

CC33b (repo `deskops`) es un nodo ejecutable, no un agregado. Debe hacer que el cierre de cada tipo lo decida una `RuleDoc` semilla `on_transition` sobre `task_completes` (`where current_node = "ritual-testing"`) que exija los recibos `evidence` de CC33a; pasar las reglas de campo a `RuleDoc` alert; borrar `__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified` y `_add_closeout_facts`; y migrar a `RuleDoc` o justificar los chequeos de CC38. Resultado observable: sin recibo commit accepted, `task_completes` bloqueada con `fact = "commit"`; editar `goal` tras verificar vuelve a bloquear; grep vacío; tests de closeout, goldens, `doctor`, docs, ritual y CHANGELOG correctos. Límites: fuera grafo (CC33c), selectores/escrituras y API de tags (DO7); formato del desk y gramática CLI sin cambios; código viejo borrado en el mismo paso.

AMBIGUEDADES

1. «los 9 chequeos de CC38 como RuleDoc» frente a «8 filas: 3, 5, 13, 14, 15, 18, 24 y 25». b1 lo resuelve usando 8; sin esa precisión habría que inventar un noveno.
2. «4 pasos del workflow en clon limpio» no enumera los pasos. Habría que inventar la secuencia exacta.
3. «los chequeos de CC38»: el bundle no incluye `runs/subagents/cc38-worker-report.md`. b5 da el criterio, pero no la condición ni el mensaje de cada fila; inventaríamos su expresión.
4. «ritual closeout vía deskops» no identifica qué ritual ni qué texto cambia. Habría que inventar el documento y la edición.
5. «goldens idénticos» no nombra conjuntos; b8 aclara ayuda y salida. Sin b8, inventaríamos el alcance.

DRY-RUN

Lecturas: TaskDoc, Board, rituales, pills, átomos y archivos listados; `deskops/data/rules/`, `data/lifecycle/`, modelos, operaciones, servicios, `tests/`, `docs/`, `CHANGELOG.md`; línea base de `doctor` en 6 desks. Cambios previstos: sembrar RuleDocs por tipo y de campo; borrar hechos, atributos y limpieza; retirar chequeos Python migrados; actualizar docs, ritual y CHANGELOG. Dependencias: APIs de `RuleDoc`, recibos de CC33a y decisión b5. Validaciones futuras: tests de archivos tocados de a uno, goldens sin `--update-golden`, grep vacío, bloqueo/reloqueo, `doctor` sin hallazgos nuevos y 4 pasos en clon limpio. No se ejecuta nada.

FUTURO

El supervisor fija worktree y corre la suite integrada contra main; el coordinador dispone hallazgos. DO7, CC33c y las decisiones de sldb quedan fuera.
