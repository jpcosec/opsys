# CC31 — informe del worker

Nodo CC31 del plan `deskops-como-config`: el ciclo de vida es un grafo con efectos. Cada
RelationDoc de `desk/lifecycle/` lleva `attributes: {sets: {status}, terminal}` (GO09) y los
seis documentos son semillas `managed` del paquete (`deskops/data/desk_declaration.yaml`,
plantillas en `deskops/data/lifecycle/`); `advance` toma la arista que `sldb.api.edges_holding`
dice que se cumple y aplica sus efectos con `sldb.api.apply_effects`. Worktree
`deskops-wt-cc31`, rama `wt/cc31` sobre `35474b32`. Sin push.

Evidencia grande en `~/proyectos/SLDB_1/coord2-ccconfig/cc31/` (fuera del repo): `k6-dryrun-*.txt`,
`k6-rituals-readonly.txt`, `n7-baseline-doctor-*.txt`, `n7-branch-*.txt`, `goldens/{main,branch,diff}.txt`,
`tests/*.txt`.

## Commits

Un solo commit en `wt/cc31`, «CC31: ciclo de vida declarado: efectos en RelationDoc.attributes y advance por edges_holding». Lo hizo el coordinador del plan con rutas explícitas, porque el worker quedó trabado en el diálogo de auto mode antes de commitear. Su sha, ya rebasado sobre main, está en `~/proyectos/SLDB_1/reports/deskops-como-config-status.md`.

## Aceptación, línea por línea

1. **Desk temporal: `desk update --apply` escribe los RelationDoc con `attributes.sets.status` y
   `terminal`; segunda corrida sin cambios; un RelationDoc sin attributes queda reescrito.**
   `tests/test_lifecycle_graph.py`:
   - `test_the_seeds_declare_the_effects_of_each_transition_and_one_edge_per_ritual`: en el desk
     `lifecycle_desk` (init + `write_lifecycle_graph`), los tres RelationDoc extraen
     `{sets: {status: active}, terminal: false}`, `{sets: {status: ready_for_testing}, terminal: false}` y
     `{sets: {status: closed}, terminal: true}` (`task_completes`); una sola arista sale de cada ritual (n3).
   - `test_desk_update_apply_rewrites_a_relation_doc_without_attributes_and_then_changes_nothing`:
     se escribe la versión anterior (sin la clave `attributes`) de `testing-task_hands_to_closeout.md`;
     `desk update` sale 1 con `- Lifecycle documents to rewrite: desk/lifecycle/testing-task_hands_to_closeout.md`;
     `--apply` imprime `Lifecycle graph: rewrote desk/lifecycle/testing-task_hands_to_closeout.md`, el archivo
     queda byte a byte igual a la plantilla y el grafo vuelve a dar `sets == {status: ready_for_testing}`;
     la segunda corrida imprime exactamente `Desk is up to date.` con el árbol de `desk/lifecycle/` idéntico
     y `deskops doctor` sale 0.
   - `test_write_lifecycle_graph_is_idempotent`: `write_lifecycle_graph` devuelve `[]` sobre un desk ya
     escrito y `desk/lifecycle/` es byte a byte `deskops/data/lifecycle/`.
2. **Efecto declarado: cambiar `sets` con la API de sldb hace que `advance` escriba ese valor sin
   tocar YAML.** `test_changing_sets_on_the_relation_doc_changes_what_advance_writes`: con
   `sldb.api.save_document_payload` se pone `attributes.sets.status: in_review` en
   `execution-task_activates`; `advance_task` deja la tarea en `ritual-testing` con `status: in_review`
   y `history: [task_activates]`; los bytes de `task_lifecycle.yaml` no cambian y no contienen `in_review`.
3. **Greps.** `grep -rn 'sets_status' deskops/` vacío; `LifecycleSpec` queda con `entry_node` y `states`
   (sin `effect`, sin `transitions`); `task_lifecycle.yaml` sin la clave `transitions` (quedan `id`, `version`,
   `source_files`, `entry_node`, `states` con su forma actual, m2). Comprobado también que no queda
   ninguna referencia a `ensure_lifecycle_graph`, `lifecycle_graph_present` ni `lifecycle_migration`
   en `deskops/`, `tests/` ni `docs/`.
4. **k6.** Ver sección propia. Decisión: ningún desk necesita la migración legada; se borran
   `lifecycle.py` :228-298 (`_ensure_ritual_readable`, `_archive_legacy_ritual`) y
   `deskops/lifecycle_migration.py` con sus llamadas en `cli/commands/desk.py` (confirmado por el
   coordinador).
5. **Tests de a uno.**
   Corridos por el worker, de a uno, en cuatro tandas (`~/proyectos/SLDB_1/coord2-ccconfig/cc31/tests*-run.log`), sobre la base `35474b32`, que es anterior a la integración de CC38. El worker quedó trabado en el diálogo de auto mode antes de completar este informe; esta sección, el n7, las líneas y los desvíos los completó el coordinador del plan con esa evidencia.
   - Verdes en la pasada final:
     - `test_lifecycle_graph` 9, `test_lifecycle_end_to_end` 5, `test_promotion_nesting` 2 (con d4), `test_desk_sync` 8, `test_scaffold_golden` 3 (tras recapturar con d3);
     - `test_cli` 101, `test_output_goldens` 7 y `test_cli_help_examples` 11 (sin `--update-golden`), `test_packaging` 6, `test_closeout_gates` 7, `test_closeout` 49, `test_desk_replace` 7, `test_desk_view` 9 (+1 skip), `test_doctor_*`, `test_review_command` 12, `test_review_doc` 13 (+1 xfail);
     - y el resto de `tests/test_*.py`.
   - Rojos previos a esta rama, comparados con main:
     - `test_board_portable_references` (falla conocida);
     - `test_skill_cli_drift` (entorno);
     - `test_atom_folder_axis`, `test_domain_tree` y `test_operator_manual`: regresiones de CC30 que corrige CC38 (`4a1aae81`), que no estaba en la base de la rama.
   - Las corridas del coordinador sobre la rama ya rebasada sobre main (con CC38) están en el informe de estado del plan.
6. **6 desks (n7).**
   - **Corrida del worker** (`n7v2-*.txt` en `~/proyectos/SLDB_1/coord2-ccconfig/cc31/`): copias completas de los 6 desks. La rama reescribe los 3 RelationDoc de cada desk que los tenía viejos («Lifecycle graph: rewrote …»).
     - Diferencias en doctor contra main: alertas de contrato que `--apply` reindexa (menos alertas con la rama).
     - Segunda corrida: «Unregistered models» en spec2viz, scion y graph_ui. Es artefacto de la copia: con la rama, el store dueño de deskops es el del worktree y el store copiado lo enlaza a otra ruta («Skipping model registration … linked elsewhere»). Con main y sin owner store, los registra directamente (control del coordinador `coord/C-main-*-scion.txt`, segunda corrida al día).
     - El desk de deskops de esa corrida no vale: `python -m deskops` corría con el cwd dentro de la copia del repo e importaba el paquete `deskops/` copiado, no el de la rama.
   - **Corrida del coordinador** (`coord/n7c.sh`, cwd neutro y desk de origin/main):
     - Rama: `--apply` rinde, la segunda corrida da «Desk is up to date.», y doctor da healthy con 16 alertas frente a 4 de main sin apply.
     - Las 12 alertas nuevas son `ReviewDoc … subject -> Task…Doc: lost`. Salen igual con main después de `--apply` (`coord/C-main-doctor-after-apply-deskops.txt`: 16 alertas, 12 `lost`), así que son previas y no de CC31.
   - Sin hallazgos nuevos atribuibles a la rama.
7. **Líneas.** `deskops/lifecycle.py`: 406 antes → 267 después. `deskops/lifecycle_migration.py`:
   172 antes → borrado. El objetivo de < 150 no se alcanzó: la parte de "escribir el grafo"
   (`seed_changes`, `tracked_line`, `write_lifecycle_graph`, ~55 líneas) y los docstrings que explican el
   contrato se quedaron en el módulo; `advance` + `transitions_from` + `transitions_holding` son ~70 líneas.
8. **CHANGELOG y docs.** Entrada en `## [Unreleased]` / `### Changed` de `CHANGELOG.md`. Sección
   nueva `### Task lifecycle graph` en `docs/workflow-policy-reference.md` (bajo Core Model, antes de
   Phases). No toqué `desk/atoms/` (la regla "nada a mano en desk/" prevalece; el átomo que materialice
   esta regla queda para quien opere el desk, ver hipótesis).

## Goldens de salida (REGLAS COMUNES 4)

Sobre dos desks de prueba frescos bajo `/dev/shm` (uno con el código de main, `git archive 35474b32`,
otro con la rama), la misma secuencia: `init`, `add task`, `show task`, `next`, `next --why`,
`next --diagram`, `advance` ×3 (el tercero bloqueado), `show task --format json`, el archivo de la tarea,
`desk update` (dry-run) y `doctor`. `goldens/diff.txt`: **diff vacío** (230 líneas idénticas tras
normalizar `<root>` y `<pkg>`). Los goldens de ayuda (`tests/test_output_goldens.py`,
`test_cli_help_examples.py`) se corrieron sin `--update-golden`: ver 5.

## Evidencia de k6 (migración legada)

Con el código de main (worktree en `35474b32`, sin cambios) y sobre copias de `desk/` + `.sldb/` de
los 6 desks bajo `/dev/shm/cc31-k6/` (misma disposición relativa, porque los links entre stores son
relativos; borradas al terminar), `deskops desk update --root <copia>` en dry-run imprimió en los seis:

```
- Legacy task lifecycle: 0 routine/primitive documents to delete, 0 tasks to rewrite, lifecycle graph missing, retired models still registered: none
```

(deskops, sldb, spec2viz, scion, pron, graph_ui; salidas completas en `k6-dryrun-<desk>.txt`.)

- `0 routine/primitive documents`, `0 tasks to rewrite`, `retired models: none` en los seis: nada que
  migrar de `lifecycle_migration.py`.
- `lifecycle graph missing` es artefacto de la copia y no cuenta (n5): el índice de aristas vive en
  `.sldb_cache/` (`sldb.store.layout.runtime_dir` = `cache_dir`), que no se copió; sin índice
  `edges_from` no devuelve nada y `lifecycle_graph_present` da falso. En los desks reales el índice está
  (`deskops/.sldb_cache/edges/RelationDoc/*.yaml`). Las demás líneas de esos dry-run (`Copied deskops
  models`, `Moved model contracts`, `Stale document hashes` de rutas fuera de `desk/`) son también de la
  copia o del estado previo de cada desk, no del ciclo de vida.
- La migración de rituales legados (`_ensure_ritual_readable` / `_archive_legacy_ritual`) solo actúa
  en el apply y solo sobre rituales no trackeados por su id, así que el dry-run no la delata; se verificó en
  modo lectura sobre los seis desks reales (`k6-rituals-readonly.txt`): en deskops, sldb, spec2viz, scion y
  graph_ui los tres rituales round-trip, no tienen secciones no declaradas según `is_unreadable_by_model`
  y están trackeados como `RitualDoc:ritual-<x>`; pron no tiene rituales (su `desk/` solo tiene `inbox/`,
  `desk update --apply` los siembra de la plantilla, legibles). En graph_ui `find_structural_noise`
  reporta `## Step Details` como no declarada (el doctor baseline también lo lista como alerta), pero al
  estar trackeados por id la migración vieja los saltaba.

## Lo que quedó como código del caso y por qué

- **Registro de los modelos de relación de sldb** (`RelationDoc`, `RelationTypeDoc`): un `include` no
  registra modelos. `write_lifecycle_graph` llama a `doc_io.init_relations_in` cuando el store no los
  tiene (hoy `SLDBBootstrap.init_local_store` ya lo hace en `init` y `desk update --apply`).
- **Reindexado tras una reescritura managed**: `sldb.api.scaffold_store` escribe el archivo con
  `tx.write_file` sin rehash del documento trackeado ni rebuild del índice de aristas; `workspace.seed_desk`
  llama a `update_store_indexes_in` cuando hubo `rewritten` y hay store (hipótesis h2 para sldb).
- **Líneas del reporte de `desk update --apply`**: `lifecycle.seed_changes` y `lifecycle.tracked_line`
  producen `Lifecycle graph: wrote/rewrote/tracked …` para mantener el golden `update.json` y la salida
  de `init`; los demás documentos trackeados por includes siguen con `Tracked <path> as <Model>.`.
- **Rituales por id**: expresado como `{model: RitualDoc, paths: [{path, name}]}` (k3). Si un desk
  tuviera un ritual trackeado por su stem (el caso que `ensure_lifecycle_graph` :337-345 re-trackeaba),
  `apply_includes` lo trackea con `force=True` bajo el id; ningún desk de los 6 está en ese caso.
- **RelationDoc por `paths`, no por glob**: el lenguaje de `include` no tiene exclusión y
  `desk/lifecycle/*.md` mezcla los dos modelos; `type-*.md` sí es un glob limpio para RelationTypeDoc.
  Con esto solo los 6 documentos declarados se gestionan y trackean (n4).

## Hipótesis y desvíos

- **d1:** `pyproject.toml` agrega `data/lifecycle/**/*` al package-data (`test_packaging`).
- **d2:** el sexto desk es `~/proyectos/SLDB_1/UIs/graph_ui`.
- **d3:** se recapturó el golden del scaffold. El diff de `init.json` y `update.json` son exactamente los sha256 de los 3 RelationDoc de `desk/lifecycle/` (`runs/subagents/cc31-evidence/scaffold-golden-diff.txt`).
- **d4:** `apply_effects` valida contra el modelo del tipo registrado. Con un tipo vacío, legado o desconocido valida contra `TaskDoc`, no contra `TaskCodeDoc` (`test_promotion_nesting::test_advance_task_keeps_nested_h3_sections_inside_scope`).
- **h1 (sldb):** un `include` no registra modelos; `write_lifecycle_graph` llama a `doc_io.init_relations_in`, que CC35a reemplaza.
- **h2 (sldb):** `scaffold_store` reescribe un archivo `managed` sin rehash ni rebuild del índice de aristas; `seed_desk` llama a `update_store_indexes_in` cuando hubo `rewritten`.
- **Objetivo de líneas:** `lifecycle.py` queda en 267, sin alcanzar el objetivo de < 150 (ver punto 7). El objetivo no es aceptación (m3).
