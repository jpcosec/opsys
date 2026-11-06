# Informe del worker: GC03 (deskops review)

Worktree: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`).
Sin commit, sin `git add`, sin push. No se tocó el repo sldb ni `desk/`/`.sldb/` del worktree.

## 1. Archivos cambiados, creados y borrados

Creados:
- `deskops/services/review.py` — servicio del comando.
- `deskops/cli/commands/review.py` — handler `ReviewCLI`.
- `tests/test_review_command.py` — tests nuevos de GC03.
- `tests/fixtures/golden/help/deskops_review.txt`
- `tests/fixtures/golden/help/deskops_review_node.txt`
- `tests/fixtures/golden/help/deskops_review_preflight.txt`
- `tests/fixtures/golden/help/deskops_review_bundle.txt`
- `tests/fixtures/golden/help/deskops_review_status.txt`
- `tests/fixtures/golden/help/deskops_review_dispose.txt`

Cambiados:
- `deskops/cli/registry.py` — registro de `deskops review` y subcomandos.
- `deskops/models/review.py` — `node` en `ReviewKind` y `REVIEW_ID_PATTERN`; comentario del template.
- `deskops/models/runtime_profile.py` — campo opcional `system_prompt`.
- `deskops/workspace.py` — `desk/runtimes/` y siembra idempotente de `runtime-pi-deepseek-flash.md`.
- `deskops/cli/commands/desk.py` — `desk update --apply` detecta el perfil ausente.
- `tests/test_command_registry.py` — comandos mutantes de review.
- `tests/test_cli.py` — el set de subcomandos del help raíz incluye `review`.
- `tests/fixtures/model_contract_hashes.json` — hashes de `ReviewDoc` y `RuntimeProfileDoc`.
- `tests/fixtures/golden/help/deskops.txt` — regenerado (help raíz).
- `CHANGELOG.md` — entrada de `deskops review`.
- `docs/operator-manual.md` — sección "Cold context reviews" y fila en "Verb coverage".

Borrados:
- `tests/test_context_review_helper.py`.

No tocados (fuera de mi encargo):
- `desk/drawer/plans/gates-por-tipo/context_review.py` (sigue en uso por el plan; lo retira el supervisor tras el merge).
- `desk/drawer/plans/workspace-documental/context_review.py` (lo retira el coordinador en main con el CLI).
- sldb y `desk/`/`.sldb/` del worktree.

## 2. Done When → test que lo cubre

| Línea de Done When | Test |
|---|---|
| preflight escribe attempt-1 con los 5 archivos y `review-task-x-preflight-1` (pending, `doc:TaskCodeDoc:task-x`, run_dir e input_sha256 = manifest) | `tests/test_review_command.py::test_preflight_writes_attempt_evidence_and_receipt` — PASA |
| segunda corrida sin cambios no llama al modelo y status dice `reviewed` | `tests/test_review_command.py::test_unchanged_second_run_is_reviewed_and_does_not_call_the_model` — PASA |
| editar goal → status `stale` y la siguiente corrida usa otro sha | `tests/test_review_command.py::test_edited_goal_is_stale_and_next_run_uses_a_new_sha` — PASA |
| bundle incluye rituales del Board, pills y files en orden con `FILE:` | `tests/test_review_command.py::test_bundle_includes_rituals_pills_and_files_in_order` — PASA |
| node sobre gates-por-tipo escribe un ReviewDoc por nodo (subject vacío + subject_ref) | `tests/test_review_command.py::test_node_writes_one_review_doc_per_node` — PASA |
| dispose escribe verdict/reason/disposed_at/disposed_by y una segunda dispose falla | `tests/test_review_command.py::test_dispose_writes_the_verdict_and_a_second_dispose_fails` — PASA |
| tercer intento sobre la misma clave a nivel de plan falla sin `--force` | `tests/test_review_command.py::test_third_good_attempt_on_the_same_key_fails_without_force` — PASA |
| pi falso con exit 1 → `technical_ok false` y verdict `incomplete` | `tests/test_review_command.py::test_transport_failure_leaves_technical_failure_and_incomplete` — PASA |
| CHANGELOG | `CHANGELOG.md` — PASA (entrada añadida) |
| docs/operator-manual.md con la sección `deskops review` | `docs/operator-manual.md` — PASA (sección añadida; `tests/test_operator_manual.py` — PASA) |

Cobertura adicional de las precisiones:
- Perfil `runtime-pi-deepseek-flash` sembrado por init y `desk update --apply`, idempotente y sin pisar perfiles → `tests/test_review_command.py::test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently` — PASA.
- Salida sin `REFORMULACION` es falla de transporte → `tests/test_review_command.py::test_output_without_reformulacion_is_a_transport_failure` — PASA.
- `--force` sin `--reason` es exit 2 → `tests/test_review_command.py::test_force_requires_reason` — PASA.
- `--force --reason` reintenta el mismo input y registra la razón → `tests/test_review_command.py::test_force_with_reason_retries_the_same_input` — PASA.
- Hash de contrato actualizado → `tests/test_model_contract_snapshot.py` — PASA.

La línea del grep de `context_review.py` en `desk/drawer` de deskops no la verifico aquí: depende del retiro que hace el coordinador en main (`deskops retire`/`drawer remove` del script de workspace-documental) y del retiro del script de gates-por-tipo que hace el supervisor tras el merge. En este worktree el script de gates-por-tipo sigue presente a propósito.

## 3. Última línea de pytest de cada corrida

- `tests/test_review_command.py` → `12 passed, 1 warning in 225.38s (0:03:45)`
- `tests/test_model_contract_snapshot.py tests/test_review_doc.py` → `15 passed, 1 xfailed, 1 warning in 93.81s (0:01:33)`
- `tests/test_command_registry.py tests/test_cli_help_examples.py` → `14 passed, 1 warning in 105.87s (0:01:45)`
- `tests/test_packaging.py` → `5 passed, 1 warning in 35.87s`
- `tests/test_runtime_profiles.py tests/test_runtime_initializer.py tests/test_role_materialization.py tests/test_scion_runtime.py tests/test_graph_extract_docs.py tests/test_desk_sync.py` → `42 passed, 1 warning in 265.65s (0:04:25)` (tras corregir el campo `system_prompt`)
- `tests/test_federated_models.py tests/test_migrate_desk_stores.py tests/test_doctor_alerts.py tests/test_doctor_model_registration.py` → `31 passed, 1 warning in 594.63s (0:09:54)`
- `tests/test_lifecycle_graph.py` → `15 passed, 1 warning in 179.44s (0:02:59)`
- `tests/test_cli.py` → `101 passed, 1 warning in 834.09s (0:13:54)`
- `tests/test_operator_manual.py` → `1 passed, 1 warning in 252.82s (0:04:12)`
- `tests/test_output_goldens.py` → `7 passed, 1 warning in 332.91s (0:05:32)`
- `tests/test_output_goldens.py::test_help_goldens --update-golden` → `1 passed, 1 warning in 182.02s (0:03:02)`

El fallo previo de main `tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions` no lo corrí (no es de este nodo); no está en los vecinos listados.

## 4. Hipótesis registradas

1. **Hash de contrato = sha256 del `input.md` de la clave** (precisión 7). Mientras sldb no exponga `__contract__` (GO02), no hay un hash de contrato real: `deskops review` usa el sha del input explícito guardado (preflight: el TaskDoc; bundle: el input completo; node: el bundle del nodo). El ReviewDoc guarda `input_sha256`; el pin `@sha256:<contrato>` lo pondrá sldb cuando exista GO07/GO02.
2. **`subject` sin hash / `__doc_anchors__` inerte.** Antes de GO07, `ReviewDoc.subject` es `doc:<Modelo>:<id>` sin sufijo de hash; `__doc_anchors__ = ["subject"]` queda inerte y `__references__ = []` no fabrica la arista (heredado de GC02, sin cambio aquí).
3. **`--max-attempts` cuenta solo attempts `technical_ok`.** Los fallos de transporte (exit≠0, timeout, sin `REFORMULACION`) no consumen el tope; el mismo input se reintenta con otra invocación (no hay auto-reintento dentro de una corrida, porque las precisiones no lo exigen y la semántica de D9 es "rondas buenas", no "intentos de transporte").
4. **`system_prompt` se modela como `str | None` (default `None`), no `str = ""` literal.** El extractor de sldb devuelve `None` para un campo de frontmatter ausente, y un `str` pydantic lo rechaza; esto habría roto los perfiles escritos a mano que aún no llevan `system_prompt`. Con `str | None` el campo es de verdad opcional y el perfil sembrado lo lleva a `SYSTEM`.
5. **La identidad de `actor`/`disposed_by` es `desk/config.json project_identity`** (con fallback al nombre del directorio cuando es `unknown-project`), igual que `runtime`/`message` resuelven la identidad del operador.
6. **El id de un ReviewDoc de nodo usa el `id` del dag (`deskops-gates-por-tipo`), no el nombre del directorio del plan.** La precisión 10 fija `review-<plan-id>-...`; `<plan-id>` es el campo `id` de `dag.yaml`.

## 5. Lo que no hice y por qué

- **No retiré los scripts de `desk/drawer/plans/`.** El de `workspace-documental` lo retira el coordinador en main con el CLI, y el de `gates-por-tipo` sigue en uso por este plan hasta el merge de GC03 (lo retira el supervisor después). Regla no negociable del encargo.
- **No mandé la nota a sldb** (`deskops message send --to sldb`): la manda el coordinador.
- **No escribí `desk/runtimes/runtime-pi-deepseek-flash.md` en el worktree.** La siembra la ejecuta el CLI sobre desks temporales (probado) y el desk real de deskops lo recibirá cuando el supervisor corra `desk update --apply` tras el merge.
- **No corrí la suite completa** (~1 h, la corre el coordinador). Corrí mis tests nuevos y todos los vecinos listados.
- **No implementé el perfil Scion** detrás de `--engine` (fuera de alcance de este nodo; solo quedó el punto de enganche `--engine`).
- **No verifiqué el grep de `context_review.py` en main**, porque depende del retiro del coordinador (ver §2).
