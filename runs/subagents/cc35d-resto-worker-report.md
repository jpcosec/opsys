# CC35d resto: informe del worker (cc35d2-worker)

Rama `wt/cc35d-resto`, base `a53bac26`, sin push. Contrato:
`desk/tasks/task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo.md`,
con las decisiones del coordinador B-a a B-e (`~/proyectos/SLDB_1/coord2-ccconfig/cc35d2/bloqueo-1.md`
y sus respuestas) y el cambio de `files` de `deskops/bootstrap.py` a `deskops/cli/commands/core.py`.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/cc35d2/`.

## Verificación previa

- GD27 está en sldb `origin/main` (`b896809d`): `tag_models` aparece en
  `src/sldb/api/stores/store_declaration.py`. El sldb de las corridas, `/dev/shm/sldb-main`,
  está en `3be74f5b` (GD27).
- Copias de los 6 desks en `/dev/shm/cc35d-resto/<desk>`, sacadas con `git archive` de
  `origin/<main>`, porque los main locales de deskops, sldb, spec2viz, pron y graph_ui están atrasados:
  deskops `a53bac26`, sldb `b896809d`, spec2viz `b16c021`, scion `4ead6d0bf`, pron `7f2e308` y
  graph_ui `2e29b37`.

## Lo que se entrega

Commits: `4070eca7` (código y tests), `3872f147` (docs y CHANGELOG), `6cb78d8c` (`root` como
`str`), `e1cb5716` (test de `add atom`, que lee stderr), `bc0f3e92` (`--apply` declara también en el
store que acaba de crear) y el de este informe.

- **e1, la declaración.** `deskops.atom_tags.sync_tag_declaration(root, apply=True) -> bool`
  lleva `desk/atoms/tag-namespaces.yaml` a `.sldb/store.yaml` con la API de declaración de sldb
  (`load_declaration`/`save_declaration`):
  - `tag_namespaces`: uno por namespace del archivo, ordenados. `domain` lleva
    `anchored_by: {model: CrossroadDoc, field: path, value: bare}`;
  - `tag_models: [AtomDoc, ProtoAtomDoc]`.

  El archivo gana: se reescribe solo si la declaración difiere, y una segunda corrida no hace nada.
  Un store sin `store.yaml` (`deskops init` no crea ninguno) parte de `declare_store` de sldb, que
  da la declaración que reproduce su índice, y le suma los tags. La llaman tres comandos:
  - `deskops init` (`core.py`, después de `seed_desk`): imprime
    `Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.`;
  - `deskops desk update`: la línea de divergencia
    `- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml`.
    `--apply` la sincroniza siempre, también en el store que esa misma corrida crea, e imprime
    la misma línea de init si escribió;
  - `deskops atoms add-namespace`.
- **e2 (`domain_tree.py`).** Se borran `require_domain_parents`, `_domain_errors`,
  `missing_parents`, `prefixes` y `_check_atom`.
  - `DomainTree.check` toma los errores de namespace y de padres de la familia de sldb
    (`tag_check`).
  - El padre de un crossroad, que no lleva tags, sale de `tag_tree`: un nodo intermedio sin
    documento.
  - Quedan la creación y el tipado de crossroads y protoatomos, el nombre de archivo, `typed_as` y
    `tree()`.
- **e3 (`atom_tags.py`).** Se borra `validate_atom_tag_namespaces`. `atoms validate` traduce los
  hallazgos de `sldb.api.tag_check` al texto de hoy (`tag_findings`):
  - `Unknown atom tag namespace '<ns>' for tag '<tag>'.`;
  - `no written crossroad for domain path '<path>'`.
- **Puente hasta sldb H4** (q18: create/track evalúan on_write), marcado así en el código.
  `refuse_unplaced_tags` y `refuse_unanchored_domains` rechazan antes de escribir, con el mensaje y
  el exit de hoy. Usan solo datos de sldb: `tag_namespaces`, las anclas de `tag_tree` y
  `TagNamespace.required`.
- **e4.** El conteo da 0 (tabla abajo), así que se siguió.
  - El validador del modelo (`check_atom_tags`, `ATOM_TAG_SEGMENTS_PATTERN`) prohíbe los segmentos
    vacíos (`a..b`, `a.`, `.a`).
  - El eje de carpetas es `tag_folder` de sldb (`axis_folder`), y se borra `axis_folder_relpath`.
  - Ver el desvío 1.
- **e5.** `doc_access.py`, `services/atoms.py` y `cli/commands/atoms.py` usan lo anterior.
  `doctor.py` no necesitó cambios: doctor ya muestra los hallazgos de la familia a través de
  `stores check` (`on_check`).
- **B-b.** Sin store, o con un store que no declara namespaces, deskops no chequea dominios ni
  namespaces. Está documentado en `docs/atoms.md`, `docs/operator-manual.md` y `CHANGELOG.md`.

## Aceptación línea por línea

| Línea (ACCEPTANCE / Validation / Done When) | Evidencia |
|---|---|
| grep de `require_domain_parents`, `_domain_errors`, `validate_atom_tag_namespaces` en `deskops/` vacío | `grep -rn ... deskops/` sale con rc=1 y sin líneas |
| `domain:a.b` sin crossroad falla con el mismo exit y texto | `test_parents_must_be_written_before_their_children` (proto: exit 1 y «Write the parent first: no written crossroad for pizzeria, pizzeria.carta»; crossroad hijo: «no written crossroad for pizzeria»); `test_atom_creation_refuses_an_unwritten_domain` (`add atom`: `Invalid value: Write the parent first: ...` en stderr y exit ≠ 0, como antes) |
| con crossroad (path a.b) ancla por value bare | mismo test: con `crossroad pizzeria` y `pizzeria.carta` escritos, `proto --tag domain:pizzeria.carta` crea; `test_typing_...` y `tree` igual |
| átomo con namespace no declarado da el hallazgo de sldb | `test_an_atom_with_an_undeclared_namespace_is_an_sldb_finding`: `tag_check` da `rules/builtin:tag_namespace:undeclared` y `atoms validate --all` imprime `Unknown atom tag namespace 'undeclared' for tag 'undeclared:value'.` |
| tareas y pills con namespaces no declarados no dan hallazgos (tag_models) | `test_tasks_and_pills_with_undeclared_namespaces_are_not_findings`: una pill (`workspace:desk`, `pill-type:rule`) y una tarea (`workspace:desk`, `artifact:task`) y `tag_check == []` |
| desk update --apply idempotente con la declaración | `test_desk_update_apply_writes_the_tag_declaration_once` (divergencia, apply, segundo apply «Desk is up to date.» con `store.yaml` byte a byte igual, `add-namespace` llega a la declaración); `test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph`; en los 5 desks con store `sync` da `True` y luego `False` |
| goldens de ayuda y salida idénticos | `test_output_goldens` y `test_cli` desde `/dev/shm/deskops-cc35d2`, sin `--update-golden` (tabla de tests). No cambió ningún golden |
| deskops doctor sin hallazgos nuevos en los 6 desks | ver «Doctor antes y después» |
| tests de los archivos tocados verdes | tabla de tests |
| CHANGELOG y docs | `CHANGELOG.md` («Changed»), `docs/atoms.md` («Who checks the namespaces and the domain parents»), `docs/operator-manual.md` |
| e7: lo que falta en sldb, como hipótesis | sección «Hipótesis para sldb» |
| 4 pasos en clon limpio | los corre el coordinador; `bash scripts/ci-knowledge-check.sh .` en el worktree da rc=0 (doctor «healthy, with 4 alert(s)», `stores check` PASS 496 documentos) |

## Conteo de e4 y tag_models

- `e4-count.log`: 544 documentos de `desk/atoms` en los 6 desks, 1537 tags con namespace, **0 con
  un segmento vacío**.
- `tag_models = [AtomDoc, ProtoAtomDoc]` (B-d). En los 6 desks no hay ningún ProtoAtomDoc y el
  único CrossroadDoc, `crossroad-knowledge-management` de deskops, no lleva tags. La regla del grep
  daría solo `[AtomDoc]`. Se agrega ProtoAtomDoc porque el protoatomo existe para colgar de un
  dominio: sin él, la familia no cubriría `atoms proto --tag domain:a.b` ni `atoms validate --all`
  sobre protoatomos, que hoy sí se chequean. CrossroadDoc queda fuera: no lleva tags, y su padre se
  lee de `tag_tree`.
- Namespaces por zona del desk, para ver por qué hace falta `tag_models`:
  - en átomos: `system`, `topic`, `layer`, `domain`, `pattern` y un `workspace`;
  - fuera de átomos: `workspace`, `pill-type`, `artifact`, `source`, `task`, `language`,
    `source-atom` y `type`, que ningún registro declara.

## Líneas antes y después (`wc -l`)

| Archivo | Antes | Después |
|---|---|---|
| deskops/domain_tree.py | 331 | 311 |
| deskops/atom_tags.py | 150 | 318 |
| deskops/doc_access.py | 944 | 941 |
| deskops/services/atoms.py | 869 | 860 |
| deskops/cli/commands/atoms.py | 268 | 271 |
| deskops/cli/commands/doctor.py | 178 | 178 (sin tocar) |
| deskops/models/atom.py | 143 | 153 |
| deskops/data/desk_declaration.yaml | 247 | 247 (sin tocar) |
| deskops/cli/commands/desk.py | 490 | 507 |
| deskops/cli/commands/core.py | 55 | 61 |
| CHANGELOG.md | 194 | 195 |

`atom_tags.py` crece porque recibe la sincronización (e1), el puente hasta H4 y la traducción de
los hallazgos. `domain_tree.py` pierde la lógica de padres.

## Doctor antes y después

Los logs están en la carpeta de logs: `doctor-before-*.log`, `doctor-after-*.log`,
`doctor-declared-*.log`, `doctor-built-*-deskops.log`, `family-static.log`.

| Desk | Antes (línea base) | Después, código nuevo sin declarar | Con la declaración aplicada |
|---|---|---|---|
| deskops | exit 0, 5 alertas | idéntico | idéntico sin índice. Con índice (`stores build`) aparece **1 error**: `AtomDoc:atom-desk-is-document-data-only` lleva `workspace:desk` (B-e). Con `atoms add-namespace workspace` (desde la copia) vuelve a ser idéntico a la línea base |
| sldb | exit 1 (seeds del lifecycle desactualizados y alertas) | idéntico | idéntico |
| spec2viz | exit 1 (seeds del lifecycle desactualizados) | idéntico | idéntico |
| scion | exit 1 (seeds desactualizados, modelos sin registrar) | idéntico | idéntico |
| pron | exit 1 (sin store ni estructura de desk) | idéntico | no aplica (sin store, `sync` da False) |
| graph_ui | exit 1 (seed `closeout-task_completes` desactualizado) | idéntico | idéntico |

- Los errores previos de 5 desks son preexistentes y no los toca este nodo.
- Las copias de `git archive` no traen el índice (`.sldb_cache` está en gitignore), así que el
  hallazgo solo aparece con `stores build`. Ese build tardó más de 18 minutos en la copia de sldb
  con la máquina cargada y se cortó.
- Para sldb, spec2viz, scion y graph_ui, lo que la familia puede reportar se contó leyendo los
  archivos (`family-static.py`): ningún tag de átomo con namespace no declarado y ningún `domain:`
  sin crossroad. El único hallazgo de los 6 desks es el `workspace:desk` de deskops. **Es esperado
  y lo resuelve el commit de desk del coordinador (B-e).**
- La declaración no se escribió en el `.sldb/store.yaml` de este worktree: lo hará
  `desk update --apply` del operador, después de su `add-namespace workspace` (que con este
  cambio ya sincroniza la declaración).

## Tests

Todos se corrieron de a uno, con la guarda pgrep, `MemoryMax=2G`, desde
`/dev/shm/deskops-cc35d2` (worktree desechable) y con `PYTHONPATH=<raíz>:/dev/shm/sldb-main/src`.
Logs: `pytest-<archivo>.log`.

| Archivo | Resultado | Commit |
|---|---|---|
| tests/test_atom_tags.py | 9 passed | 6cb78d8c |
| tests/test_atoms_cli.py | 4 passed | 6cb78d8c |
| tests/test_atom_folder_axis.py | 13 passed | 6cb78d8c |
| tests/test_model_contract_snapshot.py | 2 passed (hashes sin cambios) | 6cb78d8c |
| tests/test_domain_tree.py | 9 passed (49 s) | bc0f3e92 |
| tests/test_desk_sync.py | 8 passed (79 s) | bc0f3e92 |
| tests/test_legacy_task_states.py (goldens de `desk update`) | 33 passed | bc0f3e92 |
| tests/test_operator_manual.py | 1 passed (156 s) | bc0f3e92 |
| tests/test_lifecycle_end_to_end.py (salida de init) | 5 passed | bc0f3e92 |
| tests/test_cli.py | 101 passed (177 s) | bc0f3e92 |
| tests/test_output_goldens.py | 7 passed (324 s), sin `--update-golden`, sin diff en `tests/fixtures` | bc0f3e92 |

En la corrida de 6cb78d8c fallaron dos tests, y los dos se corrigieron:
- `test_domain_tree::test_atom_creation_refuses_an_unwritten_domain`: el test buscaba en stdout
  el error que `add atom` imprime en stderr, como siempre. Corregido en e1cb5716.
- `test_desk_sync::test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph`:
  `--apply` no declaraba los tags en el store que él mismo creaba. Corregido en bc0f3e92.

Después de esos dos commits se volvieron a correr los archivos tocados. Los cuatro de la primera
fila corrieron sobre 6cb78d8c; los commits posteriores no tocan lo que esos archivos ejercitan.
`tests/test_view.py` no se corrió: no usa nada de lo cambiado. Su fallo conocido con el store
construido (`test_a_store_without_the_viewdocs_is_an_error_envelope`) es preexistente y lo
arregla bd453c47 (CC35c), según el coordinador.

- La primera tanda corrió desde el worktree en el SSD y falló al importar `tag_check`/`tag_folder`.
  La causa es que los tests anteponen `../sldb/src` a `sys.path`, y el checkout hermano de sldb
  (main local `1d475bcd`) no tiene GD27. Desde `/dev/shm` ese hermano no existe y manda
  `/dev/shm/sldb-main`. En el clon limpio del coordinador, el sldb hermano tiene que tener GD27.

## Hipótesis para sldb (las abre el coordinador; no se escribió en sldb)

- **H4 (q18):** que `create_document` y `track_document_file` evalúen `on_write`, la familia
  `builtin:tag_namespace` incluida. Con eso, el puente de deskops (`refuse_unplaced_tags` y
  `refuse_unanchored_domains`) desaparece.
- **H5:** que `declare_store` (`sldb stores declare --write`) conserve `tag_namespaces` y
  `tag_models`. Hoy `_kept` solo guarda `generate` y `derived`, así que regenerar `store.yaml` con
  `stores declare --write` borraría la declaración de tags. `desk update --apply` la repone, pero
  mientras tanto la familia no corre.
- **H6:** una forma pública de leer la evaluación estructurada de la familia (namespace, tags,
  missing), en vez de parsear `Finding.what` («`<clause> (seen: <json>)`»). deskops lo parsea en
  `tag_findings`, apoyándose en el formato documentado de rules.md §4.
- **H7 (preexistente, informativa):** la familia solo ve documentos indexados. Un átomo escrito a
  mano no tiene hallazgos hasta que se trackea, y uno editado se evalúa sobre la proyección
  indexada. deskops lo documenta; si sldb quisiera evaluar los archivos del glob declarado sin
  trackear, es su decisión.

## Desvíos

1. **e4, dónde va la prohibición.** El TaskDoc dice «ATOM_TAG_PATTERN prohíbe segmentos vacíos».
   El patrón está en el esquema JSON del campo, y cambiarlo cambia el hash de contrato de AtomDoc y
   ProtoAtomDoc, que los 6 stores registran: haría falta migrarlos («contract changed» en doctor).
   Por eso la prohibición va en el validador del modelo (`check_atom_tags`, con
   `ATOM_TAG_SEGMENTS_PATTERN`), que no entra al contrato. `test_model_contract_snapshot` sigue
   verde con los hashes de siempre. Si se prefiere el patrón, es una línea más la migración de
   stores.
2. **`folder_axis` no se declara** (queda false). El eje es `atom_folder_axis` de
   `desk/config.json`, y `config.local.json` puede pisarlo por máquina, así que el `store.yaml`
   commiteado dependería de la máquina.
3. **Store sin `store.yaml`:** `sync_tag_declaration` lo crea con `declare_store` de sldb, más los
   tags. Es lo que deja la declaración en un desk recién creado con `deskops init`.
4. **Salida de `deskops init`:** suma la línea
   `Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.`. Ningún
   golden de salida la cubre: los tests de init (`test_cli.py`, `test_lifecycle_end_to_end.py`)
   solo buscan «Initialization complete.».
5. **`files` contra lo entregado:** `deskops/cli/commands/doctor.py` y
   `deskops/data/desk_declaration.yaml` están en `files` y no se tocaron. Según la regla
   «files = entrega», el coordinador puede podarlos del TaskDoc.
6. **Atom de la regla de docs:** AGENTS.md pide capturar en un átomo de `desk/atoms/` la regla
   nueva de docs («sldb chequea namespaces y padres; sin store no hay chequeo») antes de escribir
   el doc. El worker no escribe en `desk/`: queda para el operador del desk.
7. **Nombre del informe:** la disposición de pi del TaskDoc fija
   `runs/subagents/cc35d-resto-worker-report.md`, y la sección Entrega del brief dice
   `cc35d2-worker-report.md`. Se usó el del TaskDoc.
8. **`DomainTree.tree()`** (`atoms tree`) sigue leyendo crossroads y documentos de los archivos,
   sin pasar por `tag_tree`. Es una vista: no chequea nada, funciona sin store y su golden
   (`atoms_tree`) queda igual.
