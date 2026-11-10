# mv-worker: main en verde, los 10 fallos de la suite completa en CI (run 42694709414)

Tarea: `task-main-en-verde-los-10-fallos-de-la-suite-completa-en-ci-run-42694709414-c478614f` (task.debug).
Rama `wt/main-en-verde`, base `aef51c78`. Sin push.

Método (p1, p6): cada archivo fallido se corrió solo desde una copia del worktree en
`/dev/shm/deskops-mv`, con la guarda de pytest de la máquina, `TMPDIR=/dev/shm`, `timeout 900` y
`MemoryMax=2G`. Las corridas «antes» usan la copia en `aef51c78` y las «después» la copia recreada
en el commit final. Los logs están en `~/proyectos/SLDB_1/coord2-ccconfig/mv/` (`before-*.log` y `after-*.log`).
La causa se escribió y se comprobó en un sandbox antes de cada arreglo.

Nota de entorno: el binario `deskops` del venv importa `deskops-runtime` (en `c478614f`), no
este worktree. Todo comando se corrió con `PYTHONPATH=<worktree> python -m deskops`.

## Los 10 fallos

| # | test | antes | causa raíz (commit que la introdujo) | arreglo | commit | después |
|---|---|---|---|---|---|---|
| 1 | `e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout]` | FAIL: `deskops advance task task-add-changelog` → "Gate ritual-execution is blocked by its rules: [rules/rule-activation-task-code] … preflight (seen: {})" | `6afc78b0` (CC32) agrega `deskops/data/rules/rule-activation-task-code.md`: una task.code se activa con recibos preflight y bundle aceptados e intactos. El escenario hace `advance` sin recibos, y sin modelo ningún comando los producía, porque `review record` solo aceptaba reproduction, goldens y owner. | Decisión B del coordinador, revisable, con las condiciones del overlord: `review record --kind preflight\|bundle --operator <name>`. El escenario graba y dispone los dos recibos por CLI antes de `advance`. | `5dfadb40` | 6 passed, 3 skipped (los 3 `test_agent_scenarios` con modelo, por `DESKOPS_AGENT_E2E`; ya existían) |
| 2 | `…::test_reference_solutions[stuck-task-gate]` | FAIL en el setup: `deskops advance task task-ship-notes` | la misma (`6afc78b0`) | el setup graba y dispone preflight y bundle antes de `advance` | `5dfadb40` | 6 passed, 3 skipped (los 3 `test_agent_scenarios` con modelo, por `DESKOPS_AGENT_E2E`; ya existían) |
| 3 | `…::test_checks_need_the_work[stuck-task-gate]` | FAIL en el mismo paso del setup | la misma | la misma | `5dfadb40` | 6 passed, 3 skipped (los 3 `test_agent_scenarios` con modelo, por `DESKOPS_AGENT_E2E`; ya existían) |
| 4 | `test_operator_manual.py::test_operator_manual_runnable_examples_execute_in_order` | FAIL en el bloque 11: "No artifact.ritual file found for selector 'ritual-manual-ritual'". En el sandbox, con los bloques 1-10 y luego línea por línea, fallaban `show ritual`, `board`, `repository`, `faq-doc`, `step` e `inbox-note`; pasaban `atom`, `pill` y `materialization`. | Es código. `b2673b36` (CC35b) resuelve `show`/`edit` de las superficies trackeadas solo por el store (`deskops/doc_access.py:613`, `if not _tracked_surface(...)`). Pero `create_artifact` trackeaba al crear solo `_TRACKED_ON_CREATE = {atom, pill, materialization}` (`93cc1943`, CC30). Los demás `add` dejaban el archivo sin trackear. | `create_artifact` usa `create_doc` (que crea y trackea) en toda superficie trackeada. Línea en el CHANGELOG. La primera corrida «después» pasó el bloque 11 y cayó en el bloque 20, que estaba tapado: «Gate ritual-execution is blocked … rule-activation-task-docs», por `6afc78b0` (CC32), igual que los fallos 1-3. El manual graba y dispone un recibo preflight humano (`--operator`, decisión B) después del último `edit` del contrato y antes de `advance`, y explica por qué. | `87744b73`, `48a9d8db` | 1 passed (146 s) |
| 5 | `test_doc_readability.py::test_editing_an_unreadable_pill_refuses_instead_of_erasing_it` | FAIL: "No artifact.pill file found" en lugar de "Refusing to rewrite" | Es el test. `b2673b36` (CC35b): el selector ya no ve la pill escrita a mano y sin trackear, así que `edit` falla antes de llegar a la guarda de legibilidad. | Como en un desk real, la pill entra por `desk update --apply` (el include `desk/contexts/pill-*.md`, con track forzado). La aserción no cambia. Verificado en el sandbox: después del apply, `edit` da "Refusing to rewrite …". | `2982bf4c` | 6 passed |
| 6 | `test_packaging.py::test_desk_declaration_and_templates_ship_inside_the_package` | FAIL: `assert (13 == 6)` | Es el test, más un hueco real. `6afc78b0` (CC32) suma 7 semillas `rule-activation-*.md` bajo `desk/lifecycle/`, y el test (`439150d7`, CC31) fijaba 6. Además CC32 no agregó `data/rules/**/*` al package-data de `pyproject.toml`, así que un wheel no llevaba las plantillas de reglas. | El test exige 6 relaciones, 7 reglas y 13 en total, y pide `data/rules/**/*` en `pyproject.toml`. `pyproject.toml` lo declara. Línea en el CHANGELOG. | `8cee03c2` | 6 passed |
| 7 | `test_doctor_model_registration.py::test_init_registers_every_deskops_model` | FAIL: sobra `RuleDoc` en el conjunto | Es el test. `6afc78b0` (CC32) registra el `RuleDoc` de sldb en init (`deskops/lifecycle.py` `ensure_rule_model`, llamado por `write_lifecycle_graph` y por `desk.py:406`). El test (`66f81fff`) no lo esperaba. | El conjunto esperado suma `RuleDoc`, junto a `RelationTypeDoc` y `RelationDoc`. | `ea11da74` | 8 passed |
| 8 | `test_materialization_targets_outside_package.py::test_closeout_verify_accepts_materialization_coverage` | FAIL: `JSONDecodeError`. Con un script de reproducción: rc 1, stdout vacío, stderr "File not found: No artifact.task file found for selector 'task-closeout-test'". | Es el test. `b2673b36` (CC35b): la tarea escrita a mano no estaba trackeada. | El test la trackea con `doc_access.track_created_document(root, TaskDoc, …)`, como hizo la adaptación a7 de CC35b en `test_task_types` y `test_cli`. | `8a37f1d0` | 4 passed |
| 9 | `test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions` | FAIL: `UnresolvedReference(... field='rituals', target='desk/rituals/context-review.md', reason='unknown_path')` | Es el test. El test (`594a8925`) copia el `desk/tasks/Board.md` real pero fija a mano sus pills y rituales. `e80e8c0a` agregó `desk/rituals/context-review.md` a los rituales del Board (línea 34). | Primer arreglo (`d730a065`): `CONTEXT` suma `('RitualDoc', 'context-review', …)`, el conteo de edges sale de `len(CONTEXT)`, y un test nuevo exige que `CONTEXT` cubra lo que enruta el Board real. No alcanzó: el «después» siguió rojo. Causa completa: el Board referenciaba el ritual **por ruta**, y `atom-board-context-uses-portable-document-names` pide nombres trackeados, porque una ruta de un documento del proveedor no resuelve desde un consumidor enlazado (`unknown_path`). Lo confirmé en un sandbox: en el store del proveedor solo resuelve, y como `provider:` desde el consumidor no. Arreglo del dato, por CLI: `deskops edit board Board rituals [..., "context-review"]` (`e78b00b9`). | `d730a065`, `e78b00b9` | 3 passed |
| 10 | `test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path` | FAIL: falta `.pi/skills/use-deskops/SKILL.md` | Es el test. Su skip (`a83970d2`) suponía que `.pi/skills` no existe en un checkout limpio (`.pi/` está en `.gitignore`, línea 10, desde `c3651e48`). Pero `e80e8c0a` trackeó a la fuerza `.pi/skills/deskops-task-lifecycle/SKILL.md`, así que en CI el árbol existe y la copia local no. | Decisión p1: el test supone un archivo local, como dice su docstring y el `.gitignore`. Exige siempre la copia trackeada `.opencode/skills/use-deskops/SKILL.md` y chequea la local de `.pi` solo si el archivo está en disco. Se quitó el `pytest.skip`: antes, cuando faltaba `.pi/skills`, también se saltaba la copia de `.opencode`. | `a1f74fc6` | 2 passed |

Ningún skip ni xfail nuevo: `git diff aef51c78..HEAD` no agrega `pytest.mark.skip`, `pytest.skip` ni `xfail`, y se quitó un `pytest.skip`. Ninguna aserción se relajó. Las que cambiaron (conteos de 6 a 13, el conjunto de modelos, los edges de 11 a `len(CONTEXT)`, `node` como único kind rechazado por `record`) llevan su causa escrita arriba.

### Decisión B (fallos 1-3) tal como quedó

- `deskops review record --kind` acepta `preflight` y `bundle` además de `reproduction`, `goldens` y `owner`. `node` sigue rechazado.
- Para preflight y bundle, `--operator` es obligatorio: sin él, exit 2, el mensaje nombra `--operator` y no se escribe nada.
- El recibo deja visibles `engine: human`, el operador como `actor` y "no model available" en el título y en el `summary`. `dispose` no los pisa: escribe `reason` y `disposition`.
- La salida de texto suma la línea `engine: human; operator: <name>; no model available`.
- Tests nuevos en `tests/test_review_record.py`:
  - sin `--operator` falla sin escribir;
  - el recibo trae los tres datos, también después de `dispose`;
  - un task.code se activa con los dos recibos humanos, sin llamar a `pi`.
- Goldens: `deskops_review_record.txt` y `deskops_review.txt`. Este último cambió porque renderiza la línea de ayuda de `record` y el epílogo del grupo, que nombraba los kinds de `record`.
- Docs:
  - `docs/operator-manual.md`, sección «Cold context reviews»;
  - `docs/quickstart.md`, nueva sección «Review The Contract» antes del primer `advance`. Desde CC32, el quickstart (task.docs) ya no podía activar su tarea sin un recibo preflight.
- Línea en el CHANGELOG.
- Condición (c) del overlord: no se usó para ninguna tarea real del desk.

### Corridas «después» y archivos tocados (p6)

Copia `/dev/shm/deskops-mv` recreada en cada tanda. La primera tanda corrió en `fa06fb3f`.
La segunda corrió en `48a9d8db`, el último commit de código: re-corrió board, manual,
review_record y e2e, y sumó los archivos que tocan los cambios. Los commits posteriores a
`fa06fb3f` solo cambian `deskops/services/review.py`, `desk/tasks/Board.md` y el manual, así que
no afectan a packaging, doctor, skilldrift, readab ni matcov.

| archivo | resultado |
|---|---|
| test_packaging | 6 passed |
| test_doctor_model_registration | 8 passed |
| test_skill_cli_drift | 2 passed |
| test_board_portable_references | 3 passed |
| test_doc_readability | 6 passed |
| test_materialization_targets_outside_package | 4 passed |
| e2e_agent/test_agent_scenarios | 6 passed, 3 skipped (modelo) |
| test_review_record | 21 passed |
| test_operator_manual | 1 passed |
| test_cli | 101 passed |
| test_command_registry | 3 passed |
| test_desk_view | 9 passed, 1 skipped (ya existía) |
| test_operational | 10 passed |
| test_transaction | 11 passed |
| test_output_goldens | 7 passed |
| test_cli_grammar | 2 passed |
| test_tracked_selector_resolution | 10 passed |
| test_desk_sync | 8 passed |
| test_activation_rules | 10 passed |

La suite completa no la corrió el worker (p6): la corre el coordinador de proyecto al integrar.

## Desk (p4)

`PYTHONPATH=. python -m deskops desk update --apply --root .` escribió y trackeó los 7
`desk/lifecycle/rule-activation-*.md` como `RuleDoc`. También reescribió los 3 RelationDoc del ciclo de vida
(`execution-task_activates`, `testing-task_hands_to_closeout`, `closeout-task_completes`) con sus
`attributes` de CC31, y tocó `.sldb`: el modelo RuleDoc, el modelo RelationDoc, `store_index`, `store.yaml` y los documentos.
Se commiteó exactamente eso (`65175c6b`). Una segunda corrida dijo "Desk is up to date." y dejó
`git status` idéntico. Logs: `desk-update-apply-1.log` y `desk-update-apply-2.log`.

## Recibos de las tareas en ritual-execution (p5)

Findings tomados con `deskops show task` y `deskops review status` después de instalar las reglas
(`p5-findings-before.log`, `p5-review-status-before.log`).

| tarea | finding tras aplicar las reglas | recibos: los rehace el coordinador tras integrar | finding después |
|---|---|---|---|
| CC30 (task.refactor) | bloqueada: `rule-activation-task-code` (preflight sin recibo intacto; testigo `bundle-1` con anchor `lost`, sin `@sha256`) y `rule-activation-task-refactor` (sin recibo goldens) | ninguno en esta rama: cierre por resolved-by (coordinador), e2 | sin cambio |
| CC33a (task.code) | activable: gate abierto, sin bloqueo (preflight-1 y bundle-1 accepted con `@sha256`, intactos) | ninguno: recibos los rehace el coordinador tras integrar si hiciera falta (e3 c) | sin cambio (activable) |
| CC36 (task.refactor) | bloqueada: igual que CC30 (preflight `lost`, sin goldens) | ninguno: cierre por resolved-by (coordinador), e2 | sin cambio |
| CC37 (task.code) | bloqueada: `rule-activation-task-code`, preflight sin recibo intacto (testigo `bundle-1` `lost`; preflight-2/bundle-2 `changed` según `sldb stores check`, porque el contrato cambió después del pin, d1) | ninguno en esta rama: recibos los rehace el coordinador tras integrar | sin cambio |
| CC38 (task.refactor) | bloqueada: igual que CC30 | ninguno: cierre por resolved-by (coordinador), e2 | sin cambio |
| main-en-verde (task.debug) | bloqueada: `rule-activation-task-debug`, preflight sin recibo intacto (preflight-1 `lost`; preflight-3 `changed` por e1-e3) y sin reproduction | ninguno en esta rama: recibos los rehace el coordinador tras integrar (preflight por pi; reproduction con `review record` y los logs `before-*.log`) | sin cambio |

Por las condiciones e3 (c) del overlord y el cambio de plan del coordinador, ningún recibo de una
tarea real se escribió en esta rama. La única corrida pi que se lanzó, el preflight de CC37, usó el
selector corto `task-cc37` y destapó el bug de abajo. Se deshizo sin commitear: se restauró `.sldb`
y se borraron el ReviewDoc, `desk/reviews/task-cc37/` y el run_dir. Su salida traía 5 ambigüedades nuevas
sobre b2, a4, `deskops/data/rules/`, a5 y el mensaje del validador; se le pasaron al coordinador.
La copia se borró al terminar, como pidió el coordinador: la revisión real la rehace él sobre main.

## Fallo encontrado en el camino, arreglado en la tarea por decisión del coordinador

`deskops review preflight|bundle|record|status <selector>` armaban `review_id`, la carpeta del recibo,
la clave y `subject = f"doc:{model}:{task_id}"` con el selector tal como se escribió. Venía de
GC03 (`9df4c82a`) y de `record` (`293c4dc7`). Con `task-cc37` el recibo quedaba como `review-task-cc37-preflight-1` con subject
`doc:TaskCodeDoc:task-cc37`, que ninguna regla de activación ve. Arreglo (`beeebdaf`):
`ReviewService._resolve_task` devuelve la ruta y el id del frontmatter antes de escribir. Un test con
un selector corto prueba que `record` y `preflight` dejan el id completo en el review id, la ruta y el subject.

## Abierto (p2)

- Recibos de CC33a, CC37 y main-en-verde: los rehace el coordinador sobre main después de integrar
  (corridas pi y disposiciones en un solo lugar). CC30, CC36 y CC38: cierre por resolved-by (coordinador), e2.
- Las 5 ambigüedades del preflight pi de CC37 quedan para el coordinador, en su revisión sobre main.
- El nombre del commit del desk (b6 pedía «main-en-verde: reglas de activación de CC32 en el desk
  (desk update --apply)»). El commit `65175c6b` dice «main-en-verde: desk update --apply instala las
  reglas de activación de CC32 (p4)». No se reescribió la historia.
- No queda ningún rojo sin tarea de los 10.
