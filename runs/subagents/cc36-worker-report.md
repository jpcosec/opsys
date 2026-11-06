# CC36 — informe del worker

Nodo CC36 del plan `deskops-como-config`: las plantillas del desk pasan a datos del paquete
(`deskops/data/templates/`, `deskops/data/desk_declaration.yaml`) que deskops rinde en proceso y
entrega a `sldb.api.scaffold_store`; `desk update --apply` trackea con los includes declarados.
Worktree `deskops-wt-cc36`, rama `wt/cc36` sobre `50acb477`. Sin push.

## Commits

1. `3140c6b5` CC36: golden del scaffold (init y desk update --apply) con el código de main.
2. (este commit) CC36: plantillas del desk como datos escritos por el scaffold de sldb.

## Aceptación, línea por línea

1. **Golden igual antes y después.** `tests/fixtures/golden/scaffold/init.json` y `update.json`
   se capturaron en `3140c6b5` con el código de main (`pytest tests/test_scaffold_golden.py
   --update-golden`); desde entonces no se tocaron (`git diff 3140c6b5 -- tests/fixtures/golden/scaffold`
   vacío). `tests/test_scaffold_golden.py`: 3 passed en `3140c6b5` y 3 passed al final.
   `test_a_second_desk_update_apply_changes_nothing` cubre la segunda corrida de
   `desk update --apply` (stdout exacto `Desk is up to date.` y árbol de `desk/` idéntico).
   El desk viejo de (b) es `tests/fixtures/golden_desk` copiado a `tmp_path` (e1); el reporte
   son las líneas de stdout normalizadas (`<root>`, `<owner-store>`) y ordenadas, porque el orden
   de las líneas `Tracked …` y de la lista `Untracked desk documents` seguía un `set`.
2. **Grep vacío.** `grep -rn '_write_if_missing\|scaffold_desk\|guess_model_for_path' deskops/`
   no devuelve nada. El cuarto patrón, `_template(`, sí devuelve tres líneas ajenas a este nodo:
   `deskops/cli/commands/runtime.py:21,70` (`RuntimeCLI._template`, el subcomando
   `deskops runtime template`) y `deskops/runtime/scion.py:314` /`runtime.py:83`
   (`materialize_scion_template`). Son de GC03/scion, fuera de los `files` del TaskDoc y no son
   plantillas del desk; no las toqué. Las diez `*_template` de `workspace.py` (`_config_`, `_board_`,
   `_pills_`, `_phase_`, `_execution_`, `_testing_`, `_closeout_`, `_drawer_`,
   `_atom_tag_namespaces_`, `_runtime_pi_deepseek_flash_`) no existen más:
   `grep -rn '_config_template\|_board_template\|_pills_template\|_phase_template\|_execution_template\|_testing_template\|_closeout_template\|_drawer_template\|_atom_tag_namespaces_template\|_runtime_pi_deepseek_flash_template' deskops/` vacío.
3. **Copia del desk de deskops en /dev/shm (c7).** Script `cc36/c7.sh` (en
   `~/proyectos/SLDB_1/coord2-ccconfig/cc36/`): copia `desk/`, `.sldb/`, `sldb/` y los
   `runs/subagents/*/run.md` trackeados a `/dev/shm/cc36-c7/SLDB_1/deskops-wt-cc36`, enlaza los
   stores hermanos, corre `python -m deskops desk update --root <copia>` (dry-run) y borra la
   copia. Salida con main: `c7-baseline-main.txt`; con CC36: `c7-after-cc36.txt`; `diff` vacío.
   (Las dos líneas que ambos reportan, `Copied deskops models` y `Legacy task lifecycle … graph
   missing`, son artefactos de la copia: el store copiado registra los modelos directamente y el
   owner store es el del worktree. No hay `Untracked desk documents` ni `Missing desk structure`
   en ninguno de los dos.) `/dev/shm` queda limpio.
4. **Goldens de ayuda y salida.** `tests/test_output_goldens.py` y `tests/test_cli_help_examples.py`
   verdes sin `--update-golden` (tabla abajo); `git status` no muestra cambios en
   `tests/fixtures/golden/help/` ni `tests/fixtures/golden/output/`.
5. **Tests de a uno.** Corridos los 84 archivos `tests/test_*.py`, uno por vez, con el comando de
   máquina (`TMPDIR=/dev/shm … systemd-run … pytest -q -p no:cacheprovider tests/<archivo>.py`).
   Logs en `~/proyectos/SLDB_1/coord2-ccconfig/cc36/tests/` y resumen en `tests-summary.txt`.
   Ver tabla abajo.
6. **Líneas de `workspace.py`:** 885 antes, 696 después.
7. **CHANGELOG:** una entrada en `## [Unreleased]` / `### Changed`.

## Mapa plantilla → archivo / semilla

Declaración: `deskops/data/desk_declaration.yaml` (`folders`, `seeds`, `include`), validada como
`sldb.api.StoreDeclaration` al leerla.

| Antes (`workspace.py` en main) | Ahora | Semilla |
|---|---|---|
| `_config_template` :247 | `data/templates/config.json` | `desk/config.json`, `file`, if_missing (f1) |
| `_board_template` :303 (BoardDoc) | payload en `desk_declaration.yaml` | `desk/tasks/Board.md`, `document {model: BoardDoc, name: board-001}`, `track: false` |
| `_pills_template` :333 | `data/templates/contexts/pills.md` | `desk/contexts/pills.md`, `file` |
| `_phase_template` :351 | `data/templates/rituals/phase.md` | `desk/rituals/phase.md`, `file` |
| `_execution_template` | `data/templates/rituals/execution.md` | `desk/rituals/execution.md`, `file` |
| `_testing_template` | `data/templates/rituals/testing.md` | `desk/rituals/testing.md`, `file` |
| `_closeout_template` :~398 | `data/templates/rituals/closeout.md` | `desk/rituals/closeout.md`, `file` |
| `_drawer_template` :423 | `data/templates/drawer/README.md` | `desk/drawer/README.md`, `file` |
| `_atom_tag_namespaces_template` :430 | `data/templates/atoms/tag-namespaces.yaml` | `desk/atoms/tag-namespaces.yaml`, `file` |
| `_runtime_pi_deepseek_flash_template` :463 (RuntimeProfileDoc) | payload en `desk_declaration.yaml`, sin `system_prompt` | `desk/runtimes/runtime-pi-deepseek-flash.md`, `document {model: RuntimeProfileDoc, name: runtime-pi-deepseek-flash}`, `track: false`; `system_prompt` lo inyecta `seed_desk` desde `deskops.services.review.SYSTEM` (f3) |
| `subdirs` de `scaffold_desk` :170 | `folders` | `desk/tasks, contexts, rituals, atoms, roles, inbox, reviews, drawer, runtimes` (mismo orden) |
| carpetas de `doc_access.ensure_workspace` :146 | `folders` | `desk/materializations, steps, registry, faq` (e2); `desk/atoms` ya estaba |
| `guess_model_for_path` (`cli/commands/desk.py` :104) | `include` | `BoardDoc desk/tasks/board-*.md`, `PillDoc desk/contexts/pill-*.md`, `RitualDoc desk/rituals/ritual-*.md`, `AtomDoc desk/atoms/atom-*.md`, `ProtoAtomDoc desk/atoms/proto-*.md`, `RoleDoc desk/roles/*.md`, `RepositoryDoc desk/registry/*.md`, `StepDoc desk/steps/*.md`, `DeskFAQDoc desk/faq/*.md` |

Los archivos de `data/templates/` se generaron llamando a las funciones de main con el nombre
literal `{desk_name}`, así que sus bytes son los de antes con un solo reemplazo (e3,
`str.replace`). Empaquetado: `pyproject.toml` package-data suma `data/templates/**/*` y
`data/desk_declaration.yaml` (c6); `tests/test_packaging.py::test_desk_declaration_and_templates_ship_inside_the_package`
lo comprueba y además que `desk_format` de la plantilla es `CURRENT_DESK_FORMAT`.

## Código nuevo en `deskops/workspace.py`

- `desk_declaration(name) -> StoreDeclaration`: lee la declaración, la valida, rinde cada
  semilla para `name` y devuelve `folders` + semillas `text` + `include`.
- `seed_desk(target_path, *, apply=True) -> DeskScaffoldResult` (f2): `scaffold_store(target_path,
  declaration=…, apply=…)`; `created_paths` = `ScaffoldReport.created` absolutizados (carpetas
  primero, luego semillas, en orden de declaración, el mismo que tenía `scaffold_desk`).
  Lo llaman `InitCLI`, `desk install`, `desk update --apply`, `doctor --repair`,
  `doc_access.ensure_workspace` y `migrate_desk`.
- `desk_seed_text(name, path)` y `default_ritual_text(ritual_id, name)`: el ritual sale de la
  semilla `desk/rituals/<estado>.md` de la declaración (c5); `lifecycle.py` no cambia.
- `pending_desk_includes(root) -> [(model, path)]` y `apply_desk_includes(root)`: la lectura y la
  escritura de los includes declarados (`sldb.api.stores.declared_files`, `declared_includes.tracked_rows`,
  `apply_declaration.apply_includes`). `desk update` reporta `Untracked desk documents` con la
  primera y trackea con la segunda, imprimiendo `Tracked <path> as <Model>.` como antes.
- `_write_or_patch_config` queda sin rama de creación (f1); `migrate_desk` llama a `seed_desk` y
  luego al parche.

## Qué quedó como código del caso y por qué

- `inspect_desk`, `classify_desk`, `migrate_desk`, `ensure_target_directory`,
  `_write_or_patch_config` (c5): clasificación y migración, no plantilla. `_write_or_patch_config`
  podría ser una semilla `managed` parcial solo si sldb parcheara JSON campo a campo; no lo hace,
  así que queda (anotado, no cambiado).
- `desk update`: la detección de `Missing desk structure` sigue siendo la lista de cinco rutas de
  antes (Board, drawer/, reviews/, phase.md, runtime). No la cambié a `scaffold_store(apply=False)`
  porque la salida del dry-run es la que c7 compara contra main; es un candidato obvio para
  cuando el reporte del dry-run pueda cambiar.
- `doctor._check_structure` y sus `_IGNORED_MODELED_NAMES`: fuera del alcance (el doctor mantiene
  su propio chequeo de tres rutas); solo cambió la llamada de reparación.
- `desk_markdown_docs`/`modeled_desk_markdown_docs` siguen en `workspace.py` (los usa el doctor);
  `desk.py` ya no los importa.
- La FAQ (e5): nada cambia; `deskops/data/faq.md` sigue siendo el respaldo y no es semilla.

## Hipótesis y desvíos

- **H1 (desvío de c4/f3, el único de fondo).** Las semillas `document` de sldb se resuelven con
  `load_registered_model(store_path, …)`: necesitan un store `.sldb` con el modelo registrado
  (`scaffold_store(..., apply=False)` sobre un directorio sin store falla con `No store_index.yaml`;
  probado). `desk install`, `doctor --repair`, `migrate_desk` y `ensure_workspace` (la primera
  operación de `DeskopsOperations`) corren sin store, y así lo usan decenas de tests. Por eso la
  declaración YAML conserva el Board y el perfil runtime como `document {model, name, payload}`
  (DP3), pero `desk_declaration` rinde **todas** las semillas en proceso con
  `sldb.runtime.validation.render_model_markdown` (el mismo renderer que usaba `_board_template`)
  y se las pasa a `scaffold_store` como `text`. Un solo camino, sin lógica nueva de deskops: el
  renderer es de sldb. Cuando sldb admita un `document` cuyo modelo venga en proceso (una clase
  o un `model_ref` + pythonpath) sin store, la conversión a `text` sobra. Nota para sldb.
- **H2.** `document_bytes` de sldb rinde sin el `\n` final que deskops añade al escribir
  (`write_doc` y los antiguos `_board_template`/`_runtime_*_template`). Si el Board pasara a
  semilla `document` nativa, los bytes diferirían en ese byte frente al golden. Nota para sldb.
- **H3.** `apply_includes` no está exportado en `sldb.api` (el brief dice `sldb.api.apply_includes`);
  se importa de `sldb.api.stores.apply_declaration`. Tampoco hay un dry-run de `apply_includes`:
  `pending_desk_includes` repite su filtro (`declared_files` − `tracked_rows`, archivo existente)
  para el reporte. Nota para sldb: exportar `apply_includes` y una `pending_includes`.
- **H4 (globs frente a `guess_model_for_path`).** Las reglas usan el prefijo del `id_pattern` de
  cada modelo (`board-`, `pill-`, `ritual-`, `atom-`, `proto-`) y no `*.md`, por dos razones:
  (a) `desk/rituals/*.md` haría que `apply_includes` volviera a trackear `execution.md` y los otros
  tres rituales del ciclo de vida bajo el nombre del stem, cuando `ensure_lifecycle_graph` los
  trackea como `ritual-execution` etc.; (b) `desk/contexts/*.md` y `desk/atoms/*.md` reportarían
  `pills.md`, `README.md` y `crossroad-*.md` (CrossroadDoc) en el desk de deskops, rompiendo c7.
  Diferencia con antes: un `desk/contexts/foo.md` o `desk/atoms/foo.md` sin prefijo ya no se
  trackea solo; en los seis desks no existe ninguno (`deskops add` siempre escribe el prefijo).
  `inbox/`, `runtimes/` y `lifecycle/` no tienen regla: antes `guess_model_for_path` conocía
  `inbox`, pero la detección de `desk update` nunca los listaba (no son carpetas modeladas), así
  que trackearlos ahora sería comportamiento nuevo. Tampoco hay regla para tareas: las trackea
  `migrate_task_types`, como antes.
- **D1.** `deskops init` crea ahora también `desk/materializations/`, `desk/steps/`,
  `desk/registry/` y `desk/faq/` (vacías) e imprime cuatro líneas `Wrote …` más; antes las creaba
  `ensure_workspace` en la primera operación. Es lo que e2 pide (una sola declaración); el golden
  `init.json` lista archivos con sha256, como dice c3, y no cambia.
- **D2.** `ensure_workspace` ya no llama a `ensure_default_namespaces`: la semilla
  `desk/atoms/tag-namespaces.yaml` la vuelve redundante (ya lo era, porque `scaffold_desk` corría
  antes). La función sigue en `atom_tags.py`, la usa `cli/commands/atoms.py`.
- **D3.** Si `apply_includes` falla, `desk update --apply` imprime `Error: could not track the
  declared desk documents: …` y sale 1; antes seguía con el resto de archivos tras un
  `Failed to track …`. sldb trackea en bloque, no por archivo.
- **D4.** `tests/test_desk_sync.py::test_guess_model_treats_extra_boards_in_tasks_as_boards`
  pasó a dos tests: `test_declared_includes_treat_extra_boards_in_tasks_as_boards`
  (`pending_desk_includes` ve `board-*.md` como BoardDoc y no `Board.md` ni `task-*.md`) y
  `test_declared_includes_cover_what_desk_update_used_to_guess` (las nueve reglas).
- **Fallas previas en main, no de este nodo (sin tocar):**
  `test_board_portable_references::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`
  (la conocida) y `tests/test_atom_folder_axis.py` (3 tests de `atoms reorganize`):
  `deskops/services/atoms.py:174` usa `folder_axis_value` sin importarlo
  (`NameError`, viene del squash de CC30 `93cc1943`; `services/atoms.py` es idéntico a main).
- **Para el coordinador.** `deskops/lifecycle.py` y `deskops/bootstrap.py` están en `files` del
  TaskDoc y no hacían falta tocarlos; `deskops/doc_access.py` y `pyproject.toml` sí. Si el cierre
  exige `files` = entrega, hay que podar esos dos con `deskops edit task` (no lo hice: el desk lo
  opera el coordinador).

## Tests, uno por archivo (84 archivos)

79 archivos verdes, 5 con fallas, todas previas a este nodo (ver arriba y abajo). Resumen completo en `~/proyectos/SLDB_1/coord2-ccconfig/cc36/tests-summary.txt`, logs por archivo en `cc36/tests/`.

Los exigidos por la aceptación:

- `test_scaffold_golden.py`: 3 passed, 1 warning in 12.60s
- `test_desk_sync.py`: 8 passed, 1 warning in 66.12s (0:01:06)
- `test_packaging.py`: 6 passed, 1 warning in 7.21s
- `test_lifecycle_graph.py`: 15 passed, 1 warning in 23.84s
- `test_doctor_alerts.py`: 5 passed, 1 warning in 19.02s
- `test_doctor_model_registration.py`: 8 passed, 1 warning in 38.43s
- `test_doctor_unmodeled_surfaces.py`: 4 passed, 1 warning in 9.27s
- `test_cli.py`: 101 passed, 2 warnings in 131.04s (0:02:11)
- `test_cli_help_examples.py`: 11 passed, 1 warning in 31.52s
- `test_output_goldens.py`: 7 passed, 1 warning in 330.43s (0:05:30)
- `test_domain_tree.py`: 4 failed, 1 passed, 1 warning in 5.87s **(falla previa en main)**
- `test_federated_models.py`: 2 passed, 1 warning in 13.61s
- `test_operational.py`: 10 passed, 1 warning in 20.92s
- `test_promotion_nesting.py`: 2 passed, 1 warning in 3.58s
- `test_materialization_contract.py`: 5 passed, 2 warnings in 2.05s

Con fallas (ninguna de este nodo):

- `test_atom_folder_axis.py`: 3 failed, 10 passed, 2 warnings in 16.01s
- `test_board_portable_references.py`: 1 failed, 1 passed, 2 warnings in 5.37s
- `test_domain_tree.py`: 4 failed, 1 passed, 1 warning in 5.87s
- `test_operator_manual.py`: 1 failed, 1 warning in 108.85s (0:01:48)
- `test_skill_cli_drift.py`: 1 failed, 1 passed, 1 warning in 0.04s

- `test_domain_tree.py` (4) y `test_operator_manual.py` (bloque 26, `deskops atoms crossroad`): `deskops/domain_tree.py:223` llama a `self.ops._write_new_doc`, que CC30 movió a `services/atoms.py` (`AttributeError`); ambos archivos idénticos a main.
- `test_skill_cli_drift.py`: espera `.pi/skills/use-deskops/SKILL.md`, que no está en git (en main solo existe `.pi/skills/deskops-task-lifecycle/SKILL.md`).
- `test_atom_folder_axis.py` (3) y `test_board_portable_references.py` (1): ver «Hipótesis y desvíos».
