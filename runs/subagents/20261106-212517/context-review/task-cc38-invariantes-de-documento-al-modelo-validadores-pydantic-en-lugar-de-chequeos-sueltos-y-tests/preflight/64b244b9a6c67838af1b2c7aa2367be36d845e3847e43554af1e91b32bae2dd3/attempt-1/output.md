REFORMULACION
Propósito: aplicar DK6 en deskops moviendo cada invariante de UN documento desde chequeos sueltos (domain_tree, atom_tags, services/atoms, doctor, doc_access) a validadores pydantic en deskops/models/, borrando el chequeo viejo; clasificar las invariantes entre documentos para CC32/CC33 sin implementarlas. Resultado: inventario en el TaskDoc, validadores con test de ValidationError, rechazo vía sldb fields/docs update en copia del desk, goldens idénticos, doctor sin hallazgos nuevos, CHANGELOG. Repo: deskops; worktree por nodo; base origin/main con CC30 integrado o wt/cc30 si se autoriza. Límites: sin cambio de gramática, formato del desk ni textos de error; no toca ciclo de vida TaskDoc (CC37), escrituras de sldb ni reglas entre documentos; no se suple sldb con Python.

AMBIGUEDADES
1. «el validador produce el mismo texto que el chequeo viejo» (p5): para chequeos que solo vivían en tests no hay texto viejo; obligaría a inventar el mensaje.
2. «grep ... vacío salvo los asignados a CC32/CC33» (Done When): no exime los clasificados «fuera de DK6» (p4c), que seguirían en deskops; obligaría a inventar si se borran o se exceptúan.
3. «o el store» (p4b): frontera imprecisa de qué chequeo depende del store; obligaría a inventar su clasificación.
4. «runs/subagents/cc30-worker-report.md (rama wt/cc30)»: si el worktree sale de origin/main no consta que exista; obligaría a inventar la fuente del inventario.
5. «un caso para un AtomDoc y uno para un CrossroadDoc» (p6): no aclara si es un caso por modelo o por comando y modelo; obligaría a inventar la matriz de pruebas.

DRY-RUN
Lecturas: TaskDoc, dag.yaml rev2, informe cc30, archivos y líneas fijadas en p2, greps de p3. Cambios previstos: validadores en deskops/models/; borrado de _check_crossroad/_check_protoatom/_check_atom, validate_atom_tag_namespaces, validate_atoms y sus llamadas en services/doctor/doc_access; tests migrados y nuevos; CHANGELOG. Dependencias: CC30 integrado, comportamiento de sldb, copia de desk en /dev/shm. Validaciones futuras: pytest focalizado, sldb fields/docs update contra AtomDoc y CrossroadDoc, doctor y stores check en los 6 desks, goldens sin actualizar. Sin ejecutar.

FUTURO
El coordinador fija la base del worktree (origin/main o wt/cc30); el dueño decide si un documento existente inválido se corrige o bloquea; CC32/CC33 implementan las RuleDoc inventariadas; sldb responde a la nota si no aplica validadores; el supervisor corre la suite completa sobre lo integrado.
