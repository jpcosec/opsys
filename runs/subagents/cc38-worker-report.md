# CC38 worker report: invariantes de documento al modelo

Nodo CC38 del plan `deskops-como-config`, rama `wt/cc38` sobre `origin/main 93cc1943` (CC30 integrado). TaskDoc: `desk/tasks/task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests.md`. Fecha: 2026-11-06.

Principio aplicado (DK6): una invariante de UN documento es un validador pydantic de su modelo en `deskops/models/`, que sldb aplica en toda vía de escritura; una invariante ENTRE documentos es una RuleDoc, aquí solo inventariada y asignada; el test prueba que el modelo rechaza el caso malo.

## Qué cambió

- `deskops/models/atom.py`: `check_slug_id`, `check_atom_tags`, `domain_paths`; `AtomDoc` valida `id` (`atom-<slug>`) y `tags` (forma `namespace:value` y domain path de cada `domain:`). `ATOM_TAG_PATTERN` es la única fuente del patrón (`atom_tags.TAG_PATTERN` deriva de él).
- `deskops/models/crossroad.py`: `crossroad_id`, `check_domain_path`, `CROSSROAD_PREFIX`; `CrossroadDoc` valida `path` (domain path) y que `id == crossroad_id(path)`.
- `deskops/models/protoatom.py`: `PROTO_PREFIX`; `ProtoAtomDoc` valida `id` (`proto-<slug>`), `tags` (forma y domain path) y un solo `domain:`.
- `deskops/models/task.py`: `TaskDoc.title` no vacío (`Task title cannot be empty`).
- `deskops/models/validation.py` (nuevo): `validation_messages` (una línea por error, con el texto propio del validador), `InvalidDocument(ValueError)`, `validated(model, payload)`, `model_errors` y `check_document(model, text)` (payload crudo + líneas que el modelo rechaza). Es el envoltorio de p5: el servicio extrae el mensaje del validador, no reescribe el chequeo.
- `deskops/atom_tags.py`: `validate_atom_tag_namespaces` queda reducida a la consulta del registro (CC33); la rama de forma del tag se borró.
- `deskops/domain_tree.py`: `require_domain_parents` y `_domain_errors` reducidas a los padres escritos (CC33); `create_crossroad`, `create_protoatom`, `type_protoatom` construyen el modelo primero (`validated`) y ya no repiten chequeos; `_check_*` reportan las líneas del modelo (`check_document`) junto con las de nombre de archivo, registro, padres y `typed_as`; `domain_paths`/`crossroad_id`/prefijos se importan del modelo. Llama `doc_access` directo (ver desvíos).
- `deskops/services/atoms.py`: `_is_valid_atom_slug` y el chequeo de pregunta borrados; `create_atom_from_source`, `split_atom` y `merge_atom` validan el payload con el modelo antes de escribir; `_validate_atom_path` lista las líneas del modelo y sigue con las demás (nombre de archivo, registro, provenance).
- `deskops/doc_access.py`: `create_artifact` valida el payload compilado con el modelo antes de escribir (misma línea de error de antes para `add atom`).
- `deskops/services/tasks.py`: `create_task_bundle` valida el payload compilado con el modelo de tipo antes de escribir.
- `deskops/specs/compiler.py`: el chequeo de título vacío se borró (autorizado por el coordinador); el `KeyError` por `title` ausente queda (forma del payload crudo).
- `tests/test_model_validators.py` (nuevo): un `ValidationError` por validador y los cuatro casos de sldb en un desk temporal bajo `/dev/shm`. `tests/test_specs.py:73` migrado al modelo.
- `CHANGELOG.md`: una entrada en `## [Unreleased]` / `### Changed`.

## INVENTARIO

Clasificación según p4/p11: **modelo** (de un documento: se decide con los campos del payload) → validador pydantic en `deskops/models/`; **CC32** / **CC33** (entre documentos: necesita otro documento o archivo, la ruta o el nombre del archivo, o el store) → RuleDoc, solo se inventaría; **fuera de DK6** (mecánica de lectura/escritura del store, ruido estructural, campos ilegibles, parseo de frontmatter) → queda en el código. Líneas de main `93cc1943` (antes del cambio). Ningún chequeo gobierna la activación o el avance de una tarea, así que ninguno va a CC32: los de entre documentos son campos referenciados (registro de namespaces, crossroads, nombre de archivo, destino de `typed_as`, provenance) y van a CC33.

| # | Chequeo | Dónde vivía (main) | Clasificación | Destino / razón |
|---|---|---|---|---|
| 1 | id de átomo con forma `atom-<slug>` | `services/atoms.py:772 _is_valid_atom_slug`, usado en `:251` (create), `:333` (split), `:387-389` (merge), `:755` (validate) | modelo | `AtomDoc._id_follows_the_slug_convention` (`models/atom.py`, vía `check_slug_id`). Texto unificado `atom id must follow slug convention atom-<slug>: <id>`: conserva como prefijo el que fija `test_atoms_cli.py:72` (p15) y el `: <id>` de create/split/merge (que no fijaba ningún test). `_is_valid_atom_slug` borrada. |
| 2 | tag con forma `namespace:value` | `atom_tags.py:134-136` (en `validate_atom_tag_namespaces`, mixto) | modelo (parte de un documento de un chequeo mixto, p14) | `AtomDoc._tags_are_namespaced` y `ProtoAtomDoc._tags_are_namespaced` (`check_atom_tags`), mismo texto `Invalid atom tag '<tag>'. Expected namespace:value.`. La rama de formato se borró de `validate_atom_tag_namespaces`; el `pattern` de `AtomTag` se conserva (esquema JSON que lee `cli/model_introspection.py`). |
| 3 | namespace del tag declarado en `tag-namespaces.yaml` | `atom_tags.py:137-139` (resto de `validate_atom_tag_namespaces`) | CC33 (otro archivo: el registro) | Queda en `validate_atom_tag_namespaces`, reducida a esta parte y sin renombrar (p14); texto fijado por `test_atom_tags.py:75`. Exenta del grep (p10). |
| 4 | valor de un tag `domain:` es un domain path | `domain_tree.py:82-84` (`require_domain_parents`, mixto) y `:325` (`_domain_errors`, mixto) | modelo | `check_atom_tags` en `AtomDoc`/`ProtoAtomDoc`: texto `Invalid domain path '<v>': use lowercase segments separated by dots.` (el de `require_domain_parents`, que veía el usuario al crear; `_domain_errors` decía `invalid domain path '<v>'`, sin test ni golden). Borrada de ambas funciones; `_domain_errors` solo filtra los valores que el modelo ya rechazó para no inventar padres. |
| 5 | todo prefijo de un domain path tiene crossroad escrito | `domain_tree.py:85-91` (`require_domain_parents`), `:327` (`_domain_errors`), `:291-293`, `:311`, `:322` | CC33 (otros documentos: los crossroads) | Queda en `require_domain_parents` y `_domain_errors`, reducidas a esta parte (p14). Exentas del grep. |
| 6 | id de protoatom con forma `proto-<slug>` | `domain_tree.py:131-133` (`create_protoatom`) | modelo | `ProtoAtomDoc._id_follows_the_slug_convention`, mismo texto `Protoatom id must follow slug convention proto-<slug>: <id>`. Borrado del servicio. |
| 7 | un protoatom cuelga de un solo `domain:` | `domain_tree.py:136-137` (`create_protoatom`) y `:309-310` (`_check_protoatom`) | modelo | `ProtoAtomDoc._hangs_from_one_place`, texto el de creación `A protoatom hangs from one place in the domain tree: use a single domain:<path> tag.` (`_check_protoatom` decía `a protoatom takes a single domain:<path> tag`, sin test ni golden). Borrado de ambas. |
| 8 | `path` del crossroad es un domain path | `domain_tree.py:119-120` (`create_crossroad`) | modelo | `CrossroadDoc._path_is_a_domain_path` (`check_domain_path`), mismo texto. Borrado del servicio; el `pattern` de `DomainPath` se conserva (esquema). |
| 9 | id del crossroad = `crossroad-` + path con `.`→`--` | `domain_tree.py:287-288` (`_check_crossroad`) | modelo | `CrossroadDoc._id_names_the_path`, mismo texto `crossroad id must be <id>`. `crossroad_id` vive ahora en `models/crossroad.py`. Borrado de `_check_crossroad`. |
| 10 | contenido del crossroad no vacío | `models/crossroad.py:47-52` | modelo (ya lo era) | Sin cambio. Nuevo test de `ValidationError`. |
| 11 | pregunta 5WH1+ en el vocabulario | `services/atoms.py:254-256` (`create_atom_from_source`), duplicado de `AtomQuestion` | modelo (ya lo era: enum) | Duplicado borrado; el modelo responde con el texto del enum de pydantic (el texto viejo `Unsupported atom question` no lo fijaba ningún test ni golden; el CLI no lo alcanza). `test_atom_tags.py:51` ya prueba el modelo. |
| 12 | título de tarea no vacío | `specs/compiler.py:43-44` (`compile_task_spec`), fijado por `tests/test_specs.py:73` | modelo | `TaskDoc._title_is_written`, mismo texto `Task title cannot be empty` (autorizado por el coordinador, `specs/compiler.py` agregado a files). Borrado del compilador; `KeyError` por `title` ausente se queda: es de forma del payload crudo, no del modelo. `test_specs.py:73` migrado a `ValidationError` sobre el modelo (p16: armaba el payload para probar la invariante). |
| 13 | nombre de archivo = id (`filename must match atom id` / `crossroad id` / `protoatom id`) | `services/atoms.py:753`, `domain_tree.py:289-290`, `:303-304` | CC33 (la ruta o el nombre del archivo, p4b) | Queda. |
| 14 | `provenance` resolvible (URL o ruta existente) | `services/atoms.py:766-768`, `_provenance_is_resolvable :778` | CC33 (otro archivo / filesystem) | Queda. |
| 15 | destino de `typed_as` existe | `domain_tree.py:312-314` | CC33 (otro documento) | Queda. |
| 16 | crossroad duplicado / documento ya existente | `domain_tree.py:124-125`, `:216-217` (`FileExistsError`) | fuera de DK6 | Mecánica de escritura (no sobrescribir). Queda. |
| 17 | protoatom ya tipado (`typed_as` presente) | `domain_tree.py:155-156` | fuera de DK6 | Precondición de la operación `type`, no invariante del documento (un stub con `typed_as` es válido). Queda. |
| 18 | un solo valor del eje de carpetas (`folder_axis_value`) | `atom_tags.py:104-117`, usado en `services/atoms.py:174` y `doc_access.atom_doc_path` | CC33 (necesita `desk/config.json`: el eje) | Queda. |
| 19 | documentos editados / movidos / sin trackear / desaparecidos / desconocidos | `cli/commands/doctor.py:71-85` (`_check_documents`) | fuera de DK6 (p4c/p11: estado de tracking del store) | Queda. |
| 20 | el modelo no lee su propio documento | `cli/commands/doctor.py:106-118` (`_unreadable`), `doc_access.write_doc :187-196` | fuera de DK6 (p4c: campos ilegibles por el modelo) | Queda. |
| 21 | ruido estructural / claves de frontmatter no declaradas | `doc_access.write_doc :201-210` | fuera de DK6 (p4c: ruido estructural) | Queda. |
| 22 | campos propiedad del flujo rechazados en `edit` | `doc_access.edit_artifact_field :608-616` | fuera de DK6 | Política de la vía `deskops edit` (quién escribe el campo), no invariante del payload; los de ciclo de vida son de CC37 (p8). Queda. |
| 23 | parseo de frontmatter a mano (`frontmatter_id`, `_task_route_summary`, `workspace._frontmatter_task_type`) | `doc_access.py:404`, `:662`, `workspace.py:689` | fuera de DK6 (p4c: parseo de frontmatter) | Queda. El prefijo `task-` que exige `_task_route_summary :677` filtra rutas de repos registrados (no es invariante de `TaskDoc`: deskops nunca lo exige al crear). |
| 24 | artefacto renderizado declara `source_atoms` o `provenance` | `services/closure.py:926-937`, `:948` | CC33 (lee otro archivo: el artefacto y su fuente hermana) | Queda. |
| 25 | referencia apunta a un documento existente (`reference_points_to_atom`, `_reference_points_to_existing_route`) | `services/atoms.py:68`, `services/closure.py:854` | CC33 (otros documentos) | Queda. |
| 26 | tipos de tarea registrados en el store (`registered_task_types`), rutas trackeadas (`_tracked_task_paths`) | `services/tasks.py:41`, `doc_access.py:382` | fuera de DK6 (índice del store, p11) | Queda. |

Aciertos del grep de p3 (`grep -rnE "pytest\.raises\((ValueError|ValidationError)" tests/`, 20 aciertos en 6 archivos):

| Acierto | Entra | Razón |
|---|---|---|
| `test_atom_tags.py:51` (pregunta desconocida) | #11 | Ya prueba el modelo (enum); se conserva. |
| `test_atom_tags.py:59` (tag sin namespace) | #2 | Ya prueba el modelo; se conserva. |
| `test_atom_tags.py:75` (namespace desconocido) | #3 | Entre documentos (registro), CC33; se conserva. |
| `test_atom_tags.py:90` (`add_namespace` duplicado) | descartado | Chequeo sobre el registro YAML, que no es un documento modelado. |
| `test_cli.py:2781`, `test_desk_paths.py:58,77,91,106,137` | descartados | Resolución de selectores (ambigüedad, vacío), no payload de un documento. |
| `test_review_doc.py:111,117,123,143` | descartados | Ya prueban validadores de `ReviewDoc` (modelo). |
| `test_scion_runtime.py:47,55,102,127,129` | descartados | Configuración de harness y búsqueda de `RoleDoc`, no invariantes de payload. |
| `test_specs.py:73` (título vacío) | #12 | Migrado al modelo. |

## Aceptación, línea por línea

1. **Inventario completo, con clasificación y destino**: sección INVENTARIO (26 chequeos + los 20 aciertos del grep de p3).
2. **Grep de los nombres del inventario en `deskops/` vacío salvo CC32/CC33 y fuera de DK6 (p10)**:
   ```
   $ grep -rn "_is_valid_atom_slug\|Unsupported atom question\|Task title cannot be empty\|Invalid atom tag\|Invalid domain path\|hangs from one place\|crossroad id must be\|slug convention" deskops/ --include=*.py
   deskops/models/crossroad.py:28   Invalid domain path          (validador)
   deskops/models/crossroad.py:77   crossroad id must be         (validador)
   deskops/models/task.py:126       Task title cannot be empty   (validador)
   deskops/models/protoatom.py:69   hangs from one place         (validador)
   deskops/models/atom.py:44        slug convention              (validador)
   deskops/models/atom.py:57        Invalid atom tag             (validador)
   deskops/atom_tags.py:61          "Invalid atom tag namespace registry" (otro mensaje: registro YAML ilegible, no es el chequeo)
   deskops/cli/registry.py:1352, deskops/models/protoatom.py:47  textos de ayuda/descripción, no chequeos
   ```
   Siguen en el código, exentos: `validate_atom_tag_namespaces` (#3), `require_domain_parents` y `_domain_errors` (#5), `_check_crossroad`/`_check_protoatom`/`_check_atom` y `_validate_atom_path` (reducidos a #13, #14, #15, #3 y #5), `folder_axis_value` (#18), `doctor._check_documents` y `_unreadable` (#19, #20), y los helpers de #21-#26.
3. **Un test de `ValidationError` por validador nuevo** (`tests/test_model_validators.py`): `test_atom_id_follows_the_slug_convention`, `test_atom_tags_are_namespaced`, `test_atom_domain_tag_is_a_domain_path`, `test_protoatom_id_follows_the_slug_convention`, `test_protoatom_tags_are_namespaced_domain_paths`, `test_protoatom_hangs_from_one_place`, `test_crossroad_path_is_a_domain_path`, `test_crossroad_id_names_its_path`, `test_crossroad_content_is_written` (ya existía el validador), y `test_specs.py::test_task_spec_compiler_is_the_one_task_normalization` para `TaskDoc.title`. `test_services_report_the_validators_own_line` fija el envoltorio de p5. Los tests de servicio con `pytest.raises(ValueError)` se conservaron (p16): todos verdes.
4. **Los cuatro casos de sldb**: sección siguiente, con comando, payload y salida; además son tests (`test_sldb_fields_update_rejects_an_atom_id_off_the_slug_convention`, `test_sldb_fields_update_rejects_a_crossroad_path_that_is_not_a_domain_path`, `test_sldb_docs_update_rejects_an_atom_with_a_malformed_tag`, `test_sldb_docs_update_rejects_a_crossroad_whose_id_does_not_name_its_path`) sobre un desk temporal en `/dev/shm` (`TMPDIR=/dev/shm`).
5. **`doctor` y `stores check` en los 6 desks antes y después**: sección «Los 6 desks». Sin hallazgos nuevos en deskops, sldb (los cambios que aparecen son de otras sesiones), scion y pron; **spec2viz y graph_ui tienen 82 átomos existentes que el validador de id rechaza** (listados abajo; decisión del dueño, p7).
6. **Goldens idénticos**: `tests/test_output_goldens.py` 7 passed (355 s) y `tests/test_cli_help_examples.py` 11 passed, sin `--update-golden`.
7. **Tests de los archivos tocados verdes, de a uno** (`TMPDIR=/dev/shm`, `systemd-run --scope -p MemoryMax=2G`): 46 archivos, todos verdes salvo la falla previa conocida `test_board_portable_references::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`. Entre ellos: `test_model_validators` 14, `test_domain_tree` 5, `test_atoms_cli` 4, `test_atom_tags` 5, `test_atoms_split` 3, `test_atoms_merge` 5, `test_atoms_create_from_source` 3, `test_atoms_transactions` 2, `test_atom_folder_axis` 13, `test_desk_paths` 10, `test_cli` 101, `test_specs` 5, `test_review_doc` 13 (+1 xfail), `test_output_goldens` 7, `test_cli_help_examples` 11, `test_task_types` 16, `test_doc_io` 8, `test_doc_readability` 6, `test_doctor_model_registration` 8, `test_doctor_alerts` 5, `test_doctor_unmodeled_surfaces` 4, `test_operational` 10, `test_closeout_gates` 7, `test_lifecycle_graph` 15, `test_inbox_promote_cli_gaps` 20, `test_desk_sync` 7, `test_desk_replace` 7, `test_desk_view` 9 (+1 skip), `test_review_command` 12, `test_message_delivery` 6, `test_migrate_desk_stores` 16, `test_model_templates` 14, `test_closeout_atomless` 15, `test_scion_runtime` 13, y los demás importadores de `deskops.models` (`test_atom_materialization`, `test_composition`, `test_extension_points`, `test_federated_models`, `test_materialization_contract`, `test_promotion_nesting`, `test_registry_robustness`, `test_repo_identity`, `test_role_materialization`, `test_taskdoc_read_without_overlay`, `test_graph_atom_trace`).
8. **CHANGELOG**: entrada en `## [Unreleased]` / `### Changed`.

## Los cuatro casos de sldb (p13, p17)

Sobre una copia del desk de deskops en `/dev/shm/cc38-desk-copy` (`cp -a desk .sldb`), con `--pythonpath` al worktree; los archivos quedaron idénticos (`diff` contra el worktree) y `git status` del worktree no cambió. Los cuatro rechazan con exit 1.

```
$ sldb fields update docs/AtomDoc/atom-001-self-described-store-layout/id '"bad-atom"' --store /dev/shm/cc38-desk-copy/.sldb --pythonpath <worktree>
Unexpected: 1 validation error for AtomDoc
id
  Value error, atom id must follow slug convention atom-<slug>: bad-atom [type=value_error, input_value='bad-atom', input_type=str]
[exit=1]

$ sldb fields update docs/CrossroadDoc/crossroad-knowledge-management/path '"Bad.Path"' --store /dev/shm/cc38-desk-copy/.sldb --pythonpath <worktree>
Unexpected: 1 validation error for CrossroadDoc
path
  Value error, Invalid domain path 'Bad.Path': use lowercase segments separated by dots. [type=value_error, input_value='Bad.Path', input_type=str]
[exit=1]

$ sldb docs update atom-001-self-described-store-layout '{"id": "bad-atom", "title": "Self-described store layout", "five_wh_one_plus": "what", "answer": "x", "tags": ["system:sldb"]}' --store /dev/shm/cc38-desk-copy/.sldb --pythonpath <worktree>
Unexpected: 1 validation error for AtomDoc
id
  Value error, atom id must follow slug convention atom-<slug>: bad-atom [type=value_error, input_value='bad-atom', input_type=str]
[exit=1]

$ sldb docs update crossroad-knowledge-management '{"id": "crossroad-knowledge-management", "path": "Bad.Path", "title": "Knowledge management", "content": "x"}' --store /dev/shm/cc38-desk-copy/.sldb --pythonpath <worktree>
Unexpected: 1 validation error for CrossroadDoc
path
  Value error, Invalid domain path 'Bad.Path': use lowercase segments separated by dots. [type=value_error, input_value='Bad.Path', input_type=str]
[exit=1]
```

Las dos vías aplican el validador (`render_checked` → `render_model_markdown` construye el modelo). Observación para sldb (no bloquea): el rechazo sale por el canal `Unexpected:` del CLI (`SystemExit` con el texto) en vez de un `SLDBPayloadSaveError`/`SLDBValidationError` con el mensaje del validador.

## Los 6 desks, antes y después (p7)

Solo lecturas: `deskops doctor --root <desk>` (con el deskops del worktree) y `sldb stores check --store <desk>/.sldb`; `git -C <desk> status --porcelain` antes y después. Salidas completas en el scratchpad de la sesión; resumen:

| Desk | doctor + stores check antes → después | git status |
|---|---|---|
| `deskops-wt-cc38` | idénticos (healthy, 4 alertas de ruido estructural; PASS 294 docs) | solo mis archivos de código; `desk/` y `.sldb/` sin cambios |
| `sldb` | difieren por actividad ajena concurrente (aparecieron `runs/subagents/20261106-215629/`, `…-220351/`, alertas `anchors/doc_lost` y `store_hash`); ningún hallazgo de validación de modelo | igual salvo esos `runs/` ajenos |
| `spec2viz` | doctor idéntico; `stores check` directo desde el worktree **cae**: `Unexpected: 1 validation error for AtomDoc … atom-ast-compilers-for_whom` (ver abajo) | sin cambios |
| `scion` | idénticos | sin cambios |
| `pron` | idénticos | igual salvo una nota de inbox ajena (`20261106-185857-…`) |
| `graph_ui` | doctor idéntico; `stores check` directo desde el worktree **cae**: `Unexpected: 1 validation error for AtomDoc … atom-actionssection-for_whom` | sin cambios |

**Documentos existentes que el validador nuevo rechaza (82)**: ids con `_` en el slug (`…-for_whom`, `…-how_not`), que ya violaban la convención `atom-<slug>` de deskops (`atoms validate` los reportaba como `atom id must follow slug convention atom-<slug>`), pero que hasta ahora el modelo aceptaba.

- `spec2viz` (16): `desk/atoms/atom-{ast-compilers,cli-entrypoint,deskops-bridge,intermediate-representation,multi-backend-renderers,pydantic-models,schema-validator,spec-loader}-{for_whom,how_not}.md`.
- `graph_ui` (66): `desk/atoms/atom-{actionssection,canvassidebar,commandmenu,creationsection,dataprovider,edgeinspector,editorengine,editorlifecycle,encodingrules,encodingsection,filterssection,graphcanvas,graphdata-contract,graphprovider,graphstore,kgdb,kgdb-to-ui,l1app,l2canvas,l3content,layoutstrategies,nodeinspector,projectionviewstore,python-backend,react-editor,reviewworkbenchspa,schemaregistry,staticfixtures,structuralauditor,uistore,viewsection,viewssection,vitedevserver}-{for_whom,how_not}.md`.

Efecto cuando CC38 llegue a main (el deskops instalado): en esos dos desks `sldb stores check` cae con `Unexpected: 1 validation error for AtomDoc` (en vez de listar los documentos inválidos como hallazgo) y `deskops doctor` reportará `SLDB store check crashed`. Hoy `doctor` no lo muestra porque su subproceso `sldb stores check` importa el deskops instalado (main, sin los validadores); sldb carga el modelo desde el cwd o `--pythonpath`, no desde `PYTHONPATH`. No corregí nada (los desks no son míos). Requiere decisión del dueño: (a) renombrar esos átomos por deskops a `…-for-whom`/`…-how-not` (y sus referencias), o (b) admitir `_` en la convención de slug de deskops (cambia `slugify` y la regla que `atoms validate` ya aplicaba). Hasta entonces el nodo queda entregado con esta línea de p7 abierta.

## Hipótesis y desvíos

- **Regresión de CC30 en `domain_tree.py` (fallo previo en main)**: `test_domain_tree.py` fallaba en `93cc1943` (4 de 5) porque `DomainTree` llamaba `ops._write_new_doc`, `ops._track_created_document` y `ops._remove_created_file`, que la fachada de CC30 ya no tiene (`AttributeError`, `atoms crossroad/proto/type` devolvían exit 3). Autorizado por el coordinador: `DomainTree` usa `doc_access` directo (`write_new_doc`, `track_created_document`, `remove_created_file`, `read_doc`, `atom_doc_path`, `ensure_workspace`, `desk_root`) y ya no construye `DeskopsOperations`.
- **Regresión de CC30 en `services/atoms.py`**: `reorganize_atoms` usaba `folder_axis_value` y `axis_folder_relpath` sin importarlos (`NameError`, exit 3; `test_atom_folder_axis.py` 3 fallos en main). Agregué los dos imports. Al margen de eso, `test_atom_folder_axis` no se vio afectado por los validadores.
- **`Task title cannot be empty`** (p3, `test_specs.py:73`): el chequeo vivía en `deskops/specs/compiler.py`, fuera de los files originales; el coordinador autorizó agregarlo. Movido a `TaskDoc.title` con el mismo texto; el `KeyError` por `title` ausente queda en el compilador (forma del payload crudo, no del modelo). `create_task_bundle` valida el payload compilado con el modelo de tipo antes de escribir, así el CLI sigue viendo una línea (`add task` ya tenía su propia guarda de vacío en `cli/main.py:86`).
- **Un validador, un texto (p5/p9/p15)** donde el mismo chequeo tenía dos textos: id de átomo (`atom id must follow slug convention atom-<slug>: <id>`, prefijo fijado por `test_atoms_cli.py:72`, sufijo de create/split/merge), domain path (`Invalid domain path '<v>': use lowercase segments separated by dots.` en vez del `invalid domain path '<v>'` de `atoms validate --all`), un solo `domain:` (`A protoatom hangs from one place…` en vez de `a protoatom takes a single domain:<path> tag`). Ningún test ni golden fijaba los textos abandonados.
- **Envoltorio de `ValidationError` (p5)**: los servicios reportan la línea del validador (`InvalidDocument`), así `atoms crossroad … --content "   "` imprime `Error: a crossroad must describe its children: content cannot be empty` en vez del volcado multilínea de pydantic que imprimía antes; `atoms validate` lista las líneas del modelo (`model validation failed: <campo>: <msg>` para los errores propios de pydantic, la línea tal cual para los validadores) y **sigue** con nombre de archivo, registro y provenance sobre el payload crudo (`check_document`), donde antes cortaba en el primer error del modelo. `read_crossroads` ya no cuenta como escrito un crossroad cuyo id no nombra su path (antes sí, porque esa regla no estaba en el modelo).
- **Pregunta 5WH1+**: el duplicado de `create_atom_from_source` se borró; el texto `Unsupported atom question '<q>'.` no lo fijaba ningún test ni golden y el CLI no lo alcanza; el modelo responde con el mensaje del enum.
- **`pattern=` de `AtomTag` y `DomainPath`** se conservan junto a los validadores: `cli/model_introspection.py` lee el patrón del esquema JSON y quitarlo cambiaría el contrato del modelo que sldb indexa (`contract-moved`). Los validadores corren en `mode="before"` y producen el texto viejo; el patrón queda como documentación del esquema.
- **`check_slug_id` importa `doc_access.slugify` de forma perezosa**: la forma de slug está definida una sola vez en `doc_access` (que importa los modelos); mover `slugify` a `deskops/models/` habría tocado `doc_access` más allá de «quitar chequeos movidos».
- **sldb**: no se escribió nada en `~/proyectos/SLDB_1/sldb`. Dos notas para el coordinador (p6 manda `deskops message send --to sldb`, pero el brief prohíbe escribir en sldb; quedan anotadas): (1) `sldb stores check` cae con `Unexpected: …` ante un documento que el modelo rechaza, en vez de reportarlo como hallazgo por documento (ya hay una nota de inbox del 2026-10-31 sobre resiliencia ante documentos inválidos); (2) `fields update` y `docs update` rechazan bien pero por el canal `Unexpected:` del CLI.
- `pyflakes` no está en el venv; los módulos tocados se importaron y ejecutaron en los tests.
- Nada se tocó en `desk/` ni en `.sldb/` (`git status --porcelain desk .sldb` vacío). No se hizo push.
