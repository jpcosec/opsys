# CC33c worker report: graph y drift leen el grafo de proyecto de sldb (GD21)

Worker: cc33c-worker (robocop2). Rama `wt/cc33c`, base `91cb77db`. No hay diferencias de código respecto de `ba982a45` (b12): entre los dos commits solo cambian 2 documentos del drawer.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/cc33c/`.

Commits (sin push):

1. `0571d23d` CC33c: graph neighbors|missing|reflect y drift leen el grafo de proyecto de sldb (GD21). Es la implementación y la adaptación de los tests.
2. `53924790` CC33c: se borra tests/graph_oracle_v1 tras la comparación verde con el oráculo (b5). Toca solo tests y CHANGELOG, sin código de producción (b18).
3. Este informe.

## Qué cambió

- `deskops/graph/view.py` (nuevo).
  - `project_graph_view(root)` arma nodos y aristas planas desde `desk_graph(root)`, es decir, `ProjectGraph(root, desk_graph_config())` de sldb.
  - `graph_neighbors(view, id)`.
  - `read_graph_file(path)` lee un archivo que se pasa explícitamente con `--graph`.
- `deskops/graph/export.py` (nuevo). `graph build` sigue escribiendo el mismo GraphSnapshot KGDB y su hermano NetworkX, tomados del mismo grafo de sldb. Lo exigen los goldens `graph_snapshot.kg.json` y `graph_snapshot.nx.json`.
- `deskops/graph/snapshot.py`: borrado.
  - Se van `read_graph_neighbors`, `read_graph_snapshot`, `default_snapshot_read_path` y el fallback a `LEGACY_SNAPSHOT_PATH`.
- `deskops/cli/commands/graph.py`.
  - `neighbors` y `reflect` sin `--graph` leen el grafo vivo y no necesitan un build previo.
  - `missing` sin `--graph` ya leía el grafo declarado.
  - Con `--graph` se sigue leyendo ese archivo, con la misma gramática y los mismos mensajes.
- `deskops/graph/checks.py`. `find_atom_reference_violations` ya no hace `rglob`: lee el frontmatter de los documentos del grafo (`extract_doc_nodes`) que están bajo `desk/` y `docs/`.
- `deskops/graph/self_reflection.py`. `drift_check_knowledge_surfaces` lee `project_graph_view(root)` en lugar del snapshot de runtime (b10).
- `deskops/cli/commands/drift.py`: sin cambios (b10/b16). Por sí mismo no lee `snapshot.py` ni hace `rglob`. Lo que hacía las dos cosas era la función a la que llama en `self_reflection.py`, y esa sí se migró. La salida de drift es idéntica en los 6 desks.
- Ninguna parte de deskops invoca el CLI `sldb graph project` (b17).

## Aceptación, línea por línea

| Línea | Estado | Evidencia |
|---|---|---|
| neighbors y missing iguales al oráculo v1 sobre el desk real (a3/b5/b12) | OK | `oracle-compare-ba982a45.log`: copia en /dev/shm de `ba982a45` con `.sldb/`, código `0571d23d`, comparación como conjuntos. 618 nodos iguales, 296 triples `(source, target, role)`, 0 nodos con neighbors distintos, missing 0 = 0 (mismos campos de cada finding). También sobre `91cb77db` (`oracle-compare.log`): 619 nodos, 296 triples, 0 diferencias. |
| tests/graph_oracle_v1/ borrado después de la comparación (b18) | OK | Commit `53924790`, posterior a la comparación verde. `tests/closeout_graph_oracle.py` conserva solo `transitions_from_v1`, que no depende de `graph_oracle_v1`. `test_closeout_gates` deja de comparar contra el full scan y conserva las aserciones de cada caso del gate. |
| grep de rglob en deskops/graph/ vacío | OK, sin excluir nada | `grep -rn rglob deskops/graph/` devuelve exit 1, sin salida. Ver la nota de b15 más abajo. |
| goldens de ayuda y salida idénticos | ver tabla de tests | `test_output_goldens` y `test_cli_help_examples` corridos sin `--update-golden`. Además, `graph build` sobre el desk real da un `deskops.kg.json` y un `self_reflection_findings.json` idénticos byte a byte antes y después (`before/`, `after/`). |
| deskops doctor sin hallazgos nuevos en los 6 desks (b13) | OK | `desks.sh before`/`after`: `doctor` en deskops, sldb, spec2viz, scion, pron y graph_ui, sobre copias con cwd neutro. La salida es idéntica en los 6. El código base `91cb77db` es el mismo que el de `ba982a45`. |
| líneas de graph/ antes y después (b11) | OK | Tabla abajo. |
| CHANGELOG | OK | Una entrada nueva en Changed, y se actualizó la entrada de a4 con la decisión. |
| 4 pasos del workflow en clon limpio | lo corre el coordinador | — |

### Capturas CLI antes y después (deskops con el código de main frente a la rama, en copias de los 6 desks)

`missing`, `drift`, `doctor`, `build` y `reflect` dan salidas idénticas en los 6 desks. La única diferencia es `graph neighbors` sin un `graph build` previo:

- Antes daba `Error: graph snapshot not found: .../deskops.kg.json` con exit 1.
- Ahora da exit 0, y la salida es exactamente la que antes daba tras `graph build` (verificado con diff en los 3 ids).

Es el cambio buscado: neighbors lee el grafo de sldb, no un artefacto.

### Tablas wc -l (b11)

| archivo | antes | después |
|---|---|---|
| deskops/graph/__init__.py | 1 | 1 |
| deskops/graph/atom_trace.py | 45 | 45 |
| deskops/graph/checks.py | 232 | 226 |
| deskops/graph/desk_graph.py | 212 | 212 |
| deskops/graph/export.py | — | 98 |
| deskops/graph/self_reflection.py | 433 | 429 |
| deskops/graph/snapshot.py | 364 | — (borrado) |
| deskops/graph/view.py | — | 183 |
| **deskops/graph/ total** | **1287** | **1194** |
| deskops/cli/commands/graph.py | 167 | 163 |
| deskops/cli/commands/drift.py | 29 | 29 (sin cambio, b10) |
| tests/graph_oracle_v1/ (4 archivos) | 1210 | — (borrado) |
| tests/closeout_graph_oracle.py | 93 | 38 |

`git diff --stat 91cb77db HEAD`: 19 archivos, +412 / −1859 (sin contar este informe).

## Tests (de a uno, con guarda pgrep, MemoryMax=2G)

| Archivo | Resultado |
|---|---|
| test_graph_snapshot | 10 passed |
| test_graph_cli | 18 passed |
| test_graph_checks | 4 passed |
| test_graph_self_reflection | 2 passed |
| test_graph_missing_existing_files | 7 passed |
| test_graph_atom_trace | 2 passed |
| test_graph_declared_edges | 6 passed |
| test_graph_extract_docs / _edges / _sources | 2 / 3 / 16 passed |
| test_closeout_gates (closeout_graph_oracle) | 3 passed |
| test_atom_reference_convention | 6 passed |
| test_board_portable_references | 3 passed |
| test_materialization_contract | 5 passed |
| test_task_policy_leaks | 7 passed |
| test_role_materialization | 6 passed |
| test_ci_integration | 2 passed |
| test_atoms_cli | 4 passed |
| test_atom_folder_axis | 13 passed |
| test_runtime_initializer | 3 passed |
| test_atoms_create_from_source | 3 passed |
| test_materialization_targets_outside_package | 4 passed |
| test_cli_grammar | 2 passed |
| test_command_registry | 3 passed |
| test_cli_help_examples | 11 passed |
| test_output_goldens (copia /dev/shm de HEAD `53924790`, sin `--update-golden`) | 7 passed |
| test_cli (copia /dev/shm de HEAD `53924790`) | 101 passed |
| test_lifecycle_end_to_end::test_deleting_the_drawer_entry_leaves_the_task_valid (único nodo que usa `graph missing`; el archivo entero pasa los 900 s) | 1 passed |

Logs: `t1-*.log`, `t2-*.log`, `t3-*.log` y `t4-*.log` en `coord2-ccconfig/cc33c/`.

Fixtures nuevas y CC37: las de los tests nuevos (`task-live.md`, `task-source.md`) son tareas sin frontmatter. No son payloads `TaskDoc` con estado de ciclo de vida, así que el validador de CC37 no interviene.

## a4 / b14 / b15

`project_graph` sobre la copia de `ba982a45` no crea nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json` (`oracle-compare-ba982a45.log`; la excepción oculta 4 findings). Por eso se aplicó b15 tal cual:

- `declared_target_is_a_file` y `tests/test_graph_missing_existing_files.py` quedan intactos; solo se actualizó el docstring con la decisión.
- Se avisó al coordinador con la evidencia, y aceptó.
- Nota: `declared_target_is_a_file` nunca tuvo `rglob`. El único `rglob` de `deskops/graph/` estaba en `find_atom_reference_violations` y ya no está. Por eso el grep queda vacío sin necesidad de excluir esa función.

## b4 (closeout)

El enlace atom/materialization del closeout (`closeout_gates.py`, `build_closeout_graph_context`) ya leía `desk_graph`, nunca `snapshot.py`. No se tocó `closure.py` ni `closeout_gates.py`.

## Hipótesis para sldb (el coordinador las abre en el drawer de sldb)

1. **Nodos para archivos que no son documento.** El grafo de proyecto no tiene nodo para un archivo existente que no cae en ninguna `FileRule` (un `.yaml` del drawer) o que está excluido (`tests/fixtures/*.json`), aunque un documento lo declare como target. Opciones:
   - que `DeclaredFileTargets` o una regla «target declarado existente → nodo `file`» lo cubra en sldb;
   - o que deskops amplíe sus `FILE_RULES`, lo que cambiaría el conjunto de nodos del grafo.

   Mientras tanto, la excepción `declared_target_is_a_file` queda en deskops.
2. **`project_graph` declarable.** `sldb.api.project_graph(store)` exige `project_graph` en `store.yaml` (si falta, da `SLDBStoreError: ... declares no project_graph`). La configuración del desk no se puede declarar como dato porque:
   - `closed_document` (un issue cerrado es historia) es un callable;
   - `fields_by_kind` y `fields_by_model` se derivan de los modelos de deskops en tiempo de importación.

   Hipótesis: `closed:` por superficie (sldb ya lo anuncia como reemplazo) que exprese «sección Status = closed», y una forma declarativa de derivar los campos desde `__references__` y `__containment__` de los modelos registrados.
3. **Export del grafo de proyecto como GraphSnapshot.** No existe un `ProjectGraph → GraphSnapshot`. Por eso `deskops/graph/export.py` mantiene la forma KGDB de `graph build`. Si sldb lo ofreciera, ese módulo se reduciría a una llamada.
4. **`snapshot_load` de sldb** no sirve para leer los grafos simples de `--graph` (el fixture `static_desk_source_graph.json`): pierde `kind` y las aristas de primer nivel. Por eso `read_graph_file` queda en deskops.

## Desvíos

- **DO8 (aceptado por el coordinador), b2/b17.** Se usa `ProjectGraph(root, desk_graph_config())` de `sldb.api.edges.project_graph`, igual que `desk_graph.py` y el closeout, y no `sldb.api.project_graph(store)`. El store de deskops no declara `project_graph`, declararlo está fuera de los archivos permitidos (`.sldb/store.yaml`), y `closed_document` no es expresable como dato (hipótesis 2).
- **`--graph <path>` sigue leyendo un archivo de grafo.** La gramática del CLI y los goldens de ayuda no cambian. El texto de ayuda de `neighbors` («defaults to the root runtime snapshot») queda como está para no tocar el golden, aunque el default ahora es el grafo vivo del root.
- **`graph build` conserva su forma KGDB** (`export.py`, 98 líneas). Es una serialización, no una construcción del grafo. La exige el golden `graph_snapshot.kg.json` (hipótesis 3).
- **b18.** El commit de implementación `0571d23d` llevaba un test nuevo mal escrito: `test_the_project_graph_view_is_what_the_built_snapshot_reads_back` esperaba el id `task:task-source`, y una tarea sin `id` en el frontmatter se identifica por su ruta. La corrección de la aserción entró en `53924790`, que solo toca tests y CHANGELOG. No se reescribió la historia.
- **Tests de closeout.** Borrar el oráculo obligó a editar `tests/test_closeout_gates.py` y `tests/closeout_graph_oracle.py`, que son del área de closeout (CC33a/b). Solo se quitaron las comparaciones contra el full scan: las aserciones de cada caso del gate y el oráculo de transiciones siguen.
- **Docs fuera de los archivos permitidos.** `docs/operator-manual.md:755` muestra `graph neighbors ... --graph .deskops/graph.json`, que sigue siendo válido. No hay ninguna doc que exija `graph build` antes de `neighbors`, así que no hizo falta cambiar docs.
