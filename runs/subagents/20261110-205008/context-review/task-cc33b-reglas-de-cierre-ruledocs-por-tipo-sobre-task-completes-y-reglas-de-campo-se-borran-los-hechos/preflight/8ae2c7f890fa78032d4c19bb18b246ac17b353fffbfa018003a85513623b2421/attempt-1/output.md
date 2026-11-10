## REFORMULACION
Nodo `task.code` ejecutable del plan `deskops-como-config`, repo **deskops**. Propósito: que el cierre de cada tipo lo decida una RuleDoc semilla `on_transition` sobre `task_completes`, con recibos `evidence`; convertir reglas de campo en RuleDocs `alert`; borrar hechos y gates viejos. Resultado: aceptación del TaskDoc (bloqueo sin recibo `commit`, grep limpio, 8/9 chequeos migrados, tests/goldens/doctor/CI). Límites: fuera grafo (CC33c), selectores/escrituras y tags por API de sldb (DO7).

## AMBIGUEDADES
1. «los 9 chequeos de CC38» frente a «8 filas» (b1/c1). Obliga a decidir si se busca un noveno o se aceptan 8.
2. a5: «el tipo pasa a leer sus kinds de la RuleDoc o de una tabla de datos» frente a c3: «de una tabla de datos […] no de la RuleDoc». Obliga a elegir fuente.
3. a1: «por cada kind de __closeout_evidence__ del tipo» frente a a5: «se borra __closeout_evidence__». Obliga a inventar cómo sobreviven los kinds.
4. Título: «se borran los hechos y gates viejos» frente a c4: «Los productores de closeout_gates.py se quedan». Obliga a decidir qué gates se borran.
5. «los 9 chequeos […] como RuleDoc con su función vieja borrada» frente a b6: «se eximen del grep». Obliga a fijar la aceptación de los no expresables.
6. «tests de closeout verdes» sin archivos: obliga a elegir el conjunto de tests.

## DRY-RUN
Lecturas: TaskDoc, `dag.yaml`, informe CC38, recibos de CC33a, plantillas `rule-activation-*`, `closeout_gates.py`, `task_types.py`, goldens y línea base de `doctor`. Cambios previstos: crear `rule-closeout-task-<tipo>.md` y `closeout-evidence.yaml`; quitar `has(closeout_evidence_verified)` de la arista; borrar `_add_closeout_facts`, `closeout_evidence_verified`, `pill_graduation_verified` y `__closeout_evidence__`; migrar 8 filas (las no expresables, hipótesis); actualizar ritual vía deskops, docs y CHANGELOG. Dependencias: CC33a en main; lenguaje de reglas de sldb; DO7 para #3/#5. Validaciones futuras: caso bloqueado/desbloqueado, grep, pytest por archivo, goldens idénticos (parar ante diff), `doctor` en 6 desks, 4 pasos CI e idempotencia de `desk update --apply`. Sin ejecutar nada.

## FUTURO
El coordinador corre los 4 pasos en clon limpio, decide diffs de goldens e hipótesis, y el supervisor revisa. sldb/DO7 resuelve H1 y API de tags; CC33c cubre el grafo.
