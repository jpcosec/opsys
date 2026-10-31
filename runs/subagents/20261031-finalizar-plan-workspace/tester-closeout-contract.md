# G_CLOSEOUT — verificación independiente focalizada

Estado: PASS focalizado — 23 passed, 3 deselected; exit 0; 120.46 s. Este archivo no es el dictamen del plan final.

Dictamen: G_CLOSEOUT puede registrarse satisfied para su contrato acotado: implementación/commit de cierre + evidencia declarada + relación exacta task→commit/autoría de cierre. No hace falta WS45 por identidad de actor; no se incorpora un requisito de autorización ajeno al gate.

## Contrato examinado

G_CLOSEOUT exige implementación y commit de cierre verificables, evidencia declarada y relación/autoría de cierre por tarea. La autoría aquí verificable es el vínculo exacto `Task-Id` de la tarea con su commit de cierre y la protección contra enmendar el cierre de otra tarea. No significa autenticación de persona, firma criptográfica, RBAC ni autoridad UI/coordinador multiescritor.

## Recibos históricos y runtime

`tester-closeout-receipts.json` conserva argv/salida/exit de `git show` y ancestros. 59244c946f048dd6c527133f1b3025c22026d9b2 implementa el contrato. 1fefa97a3c7a94b967543136d550e00a7786766c cierra la tarea exacta con trailers Task-Id/Run-Dir, elimina el TaskDoc y lo retira del Board. Ambos pertenecen a la historia del HEAD examinado. El cuerpo histórico se obtiene de `git show 1fefa97^:<ruta>`, sin recrear tarea activa.

`tester-closeout-runtime.json` comprueba desde /tmp que imports usados por subprocess corresponden al checkout actual, no a copia instalada obsoleta. Los SHA256 de tests y fuentes están en los recibos.

## Qué prueban las pruebas seleccionadas

- `tests/test_closeout_declared_evidence.py`: CLI real en repos temporales: external URL abre/cierra y sin URL bloquea; code sin tests bloquea; docs/spec/design requieren commit+document; vocabulario cerrado; migración legacy como code con alerta; .py sin tests alerta sin bloquear; add task exige declaración o tipo y respeta evidencia explícita. El selector `-k closeout` incluye todos los tests de este módulo por su nombre de archivo.
- `test_task_lifecycle_runs_from_intake_to_closeout_via_real_cli`: intake→drawer→task authored→transiciones→closeout; verifica trailer Task-Id y archivos reales del commit.
- `test_closeout_amends_only_head_with_its_own_task_id`: task-foo no enmienda el cierre de task-foo-bar; verifica parentage real de Git y trailer exacto.
- Lectura adicional de `test_auto_commit_task_closure_commits_only_its_own_paths` (DESELECCIONADO por -k closeout): tanto commit como amend excluyen archivos ajenos ya staged; tarea desaparece en el commit correcto. No se presenta como ejecución actual.
- Lectura adicional de `test_auto_commit_task_closure_failure_path_keeps_bundle` (DESELECCIONADO): commit rechazado conserva TaskDoc y Board. No se presenta como ejecución actual.
- El tercer deselectado es `test_deleting_the_drawer_entry_leaves_the_task_valid`. Los dos lifecycle ejecutados son el ciclo CLI completo y la protección de Task-Id ajeno. Las 21 parametrizaciones del módulo de evidencia declarada se ejecutaron.

## Límites

El gate de evidencia `tests` acepta una referencia a archivo Python existente bajo tests/; no ejecuta el test ni valida el sufijo ::node. `commit` exige un commit ancestro resoluble, no prueba por sí solo que ese commit implemente el requisito. Las pruebas de lifecycle usan pequeños archivos smoke como evidencia para probar el workflow real, no como prueba de funcionalidad del producto. La comprobación actual del contrato viene de ejecutar las aserciones de CLI/Git y leer las fuentes, no de esos smoke.

Los recibos históricos prueban cierre y enlace, no que aquel cierre histórico pasara automáticamente el gate nuevo (el TaskDoc histórico aún no declaraba closeout_evidence y tenía references vacías). No se reescribe historia para simularlo. La evidencia focalizada actual prueba comportamiento presente.

No se ejecuta suite global conocida roja, no se arregla producto, no se acredita G_SOURCE/G_HUMAN_READ/G_SCION, ni se habilita ejecución del DAG. Tampoco se valida el plan final hasta recibir handoff congelado.
