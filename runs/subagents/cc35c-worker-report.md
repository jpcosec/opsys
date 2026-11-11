# CC35c: informe del worker

Nodo CC35c del plan `deskops-como-config`. Trata las referencias entrantes con `referrers` y `rewrite_references` de sldb, dentro de la transacción, y las menciones en prosa como `MentionPattern`.
Rama `wt/cc35c`. Se rebasó dos veces sobre origin/main, y las dos entraron limpias:

1. `797b89fe` (NONTERM): toca `task_lifecycle.py`, `workspace.py` y otra sección del manual.
2. `0eb4f36b` (ADV): toca `doctor_findings.py`, `lifecycle.py`, `cli/commands/doctor.py` y otras secciones del manual y del CHANGELOG.

Ninguno de los dos toca archivos de este nodo, así que no hubo choques que resolver.

Después del segundo rebase volvieron a correr, desde /dev/shm: `test_lifecycle_seed_drift` (8), `test_lifecycle_graph` (9), `test_atoms_merge` (7), `test_retire_cli` (13), `test_inbox_promote_cli_gaps` (21), `test_closeout` (59), `test_output_goldens` (7) y `test_cli` (101). Todos verdes.

Doctor volvió a correr en los 6 desks, con base `0eb4f36b` contra HEAD. ADV agrega hallazgos de semillas desactualizadas: deskops pasa a 13 y exit 1. Aun así, la salida de la base y la de HEAD son idénticas byte a byte en los 6 desks (`doctor-before-adv/` y `doctor-after-adv/`). `ci-knowledge-check.sh .` da exit 0 (`ci-knowledge-check-final.log`).

## Qué cambió

- **`deskops/services/references.py` (nuevo).** Lee y reescribe las referencias entrantes de un documento con piezas de sldb sobre el grafo del desk armado en proceso (`desk_graph(root)`, DO8). No usa `sldb.api.project_graph(store)`.
  - `referrers_of` usa `resolve_target` y `find_hits` de `sldb.api.edges.referrers`. Los campos salen del índice de aristas del store y las menciones, de los `MentionPattern` del grafo.
  - `rewrite_referrers` reescribe los campos con `rewrite_references(store, target, replacement, transaction=tx)` y las menciones con `rewritten_line` y `replace_text(..., transaction=tx)`. Todo corre dentro de la `desk_transaction` de quien llama.
  - `dangling_referrers` y `alert_dangling` sirven a drawer remove y closeout.
  - Un desk sin store no tiene campos ni transacción: usa solo las menciones del grafo y escribe archivos planos, como hace `doc_access`.
- **`deskops/services/atoms.py`.** delete y split listan los referrers con `referrers_of`. merge reescribe con `rewrite_referrers` dentro de la misma `desk_transaction` que escribe el átomo destino y el stub. Se borraron `_find_inbound_atom_references`, `_rewrite_inbound_atom_references` y el método `_reference_points_to_atom`, que solo usaban esas dos.
- **`deskops/services/retire.py`.** Una sola `desk_transaction` hace `rewrite_referrers(path, None)`: quita la entrada de los campos declarados (`pills` del Board y de cada tarea). En esa misma transacción quita los bullets del drawer Board (issue cerrado) y hace `delete_doc`. Una mención en prosa nunca se reescribe y bloquea sin `--force`. Se borraron `_inbound_references`, `_board_pill_updates`, `_handled_boards`, `_write_board`, `_pill_reference_matches`, `_REFERENCE_SURFACES` y `_REFERENCE_FILES`.
- **`deskops/services/drawer.py`, `remove_entry` (b3).** Lee los referrers dentro de la transacción, después de quitar los bullets `- \`<stem>\``. Por cada archivo que sigue nombrando la entrada imprime `alert: <entrada> still referenced by <archivo>` en stderr. No reescribe y no cambia el exit.
- **`deskops/services/closure.py`, `_close`.** Es el camino común de commit, supersede, retire, resolved-by y close_auto. Lee los referrers de la tarea antes de borrarla, deja fuera el Board si la ruteaba y avisa igual que drawer remove después del commit. No reescribe.
- **`deskops/graph/desk_graph.py`.** Dos `MentionPattern` junto a `ATOM`:
  - `ATOM_ID`: `atom:atom-<slug>` como token entero, con target `{0}`. Entra en `SECTION_MENTIONS`, delante de `ATOM`, y en `LINE_MENTIONS` (todas las líneas de task e issue, sin las tareas del drawer).
  - `DRAWER_BULLET`: `` - `tasks/<id>.md` `` o `` - `<id>` ``, con target `{kind}:{id}`. Entra en `LINE_MENTIONS` para `drawer_board`.
- **`docs/operator-manual.md`** (secciones drawer remove, retire y atoms merge/delete/split) y **`CHANGELOG.md`** (Changed).

## Aceptación, línea por línea

| Línea | Evidencia |
|---|---|
| `grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/` vacío | Vacío en HEAD; ver la sección [Grep de aceptación](#grep-de-aceptación). Las funciones nuevas se llaman `referrers_of` y `rewrite_referrers` para no contener la subcadena `_inbound_references`. |
| retire de una pill la quita del Board y de las tareas en una sola transacción (a5, b4) | `tests/test_retire_cli.py::test_retire_removes_a_pill_from_the_board_and_two_tasks_in_one_transaction`: un desk `init` con la pill en el Board y en dos tareas. Se cuenta que se abre una sola `desk_transaction` exterior; Board y tareas quedan sin la pill; `sldb stores check` da PASS. |
| un fallo forzado no cambia nada | `test_retire_failing_midway_leaves_the_desk_and_store_unchanged`: `delete_doc` falla después de que se reescribieron el Board y las tareas, y los bytes de `desk/` y `.sldb/` quedan idénticos. |
| atoms merge reescribe menciones `atom:<id>` en prosa, las dos formas (b1) | `tests/test_atoms_merge.py::test_atoms_merge_rewrites_both_mention_forms[False/True]`, en un desk sin store y en uno con store. `atom:atom-source-guidance` en la prosa de una tarea pasa a `atom:atom-target-guidance`, y `` `atom-source-guidance` `` bajo `## Related Atoms` pasa a `` `atom-target-guidance` ``. El caso existente `test_atoms_merge_rewrites_only_whole_atom_tokens` (`-bar`, `.extended`, `xatom:`) sigue verde. |
| drawer remove avisa por cada referrer colgante (b3) | `tests/test_inbox_promote_cli_gaps.py::test_drawer_remove_alerts_each_reference_it_leaves_behind`. El stderr es exactamente una línea por el drawer Board (bullet en forma de ruta) y otra por `desk/tasks/task-ref.md` (`## Related Tasks`). Exit 0 y nada reescrito. |
| goldens de ayuda y salida idénticos | `test_output_goldens` desde `/dev/shm/deskops-cc35c`, sin `--update-golden`; ver [Tests](#tests). No se tocó ningún archivo de `tests/fixtures/golden/`. |
| tests de los archivos tocados verdes | Ver [Tests](#tests). |
| deskops doctor sin hallazgos nuevos en los 6 desks | Ver [Doctor](#doctor): las salidas antes y después son byte a byte idénticas. |
| líneas antes y después | Ver [Líneas](#líneas). |
| CHANGELOG | Hay una entrada en `### Changed`. |
| `bash scripts/ci-knowledge-check.sh .` | Exit 0 en el worktree (log en `coord2-ccconfig/cc35c/ci-knowledge-check.log`): `graph missing` da "No missing graph references found.", y drift solo trae los hallazgos de consulta de siempre. |
| 4 pasos en clon limpio | Los corre el coordinador (a8). |

### Grep de aceptación

```
$ grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/
$ echo $?
1
```

## Tests

Cada archivo corrió de a uno con la guarda `pgrep`, `systemd-run MemoryMax=2G` y `PYTHONPATH=<raíz>:/dev/shm/sldb-main/src`, desde `/dev/shm/deskops-cc35c`. Los logs están en `coord2-ccconfig/cc35c/tests/`.

Corrieron desde /dev/shm y no desde el worktree por esto: 17 archivos de `tests/` anteponen `ROOT.parent / "sldb" / "src"` en `sys.path`. Desde el worktree eso es `~/proyectos/SLDB_1/sldb` (main `1d475bcd`), atrasado y sin GD22 ni GD27. Desde /dev/shm no hay `sldb` hermano y se usa `/dev/shm/sldb-main`.

| archivo | resultado |
|---|---|
| `test_add_task_from_drawer` | 3 passed, 1 warning in 10.59s |
| `test_atom_folder_axis` | 13 passed, 2 warnings in 16.94s |
| `test_atoms_cli` | 4 passed, 2 warnings in 4.99s |
| `test_atoms_merge` | 7 passed, 2 warnings in 11.30s |
| `test_atoms_split` | 3 passed, 2 warnings in 2.92s |
| `test_board_portable_references` | 3 passed, 2 warnings in 5.47s |
| `test_cli` | 101 passed, 2 warnings in 182.70s (0:03:02) |
| `test_cli_grammar` | 2 passed, 1 warning in 1.71s |
| `test_closeout` | 59 passed, 2 warnings in 22.38s |
| `test_closeout_atomless` | 15 passed, 1 warning in 31.79s |
| `test_closeout_declared_evidence` | 19 passed, 1 warning in 65.29s (0:01:05) |
| `test_closeout_evidence_receipts` | 5 passed, 2 warnings in 18.86s |
| `test_closeout_gates` | 3 passed, 2 warnings in 7.07s |
| `test_closeout_resolved_by` | 19 passed, 2 warnings in 6.33s |
| `test_closeout_rules` | 12 passed, 2 warnings in 33.44s |
| `test_closeout_skill_links` | 3 passed, 2 warnings in 0.71s |
| `test_closeout_test_paths` | 31 passed, 1 warning in 0.11s |
| `test_command_registry` | 3 passed, 1 warning in 1.09s |
| `test_graph_atom_trace` | 2 passed, 2 warnings in 0.63s |
| `test_graph_cli` | 18 passed, 2 warnings in 6.37s |
| `test_graph_declared_edges` | 6 passed, 2 warnings in 1.32s |
| `test_graph_extract_docs` | 2 passed, 2 warnings in 0.64s |
| `test_graph_extract_edges` | 3 passed, 2 warnings in 0.68s |
| `test_graph_extract_sources` | 16 passed, 2 warnings in 0.71s |
| `test_graph_missing_existing_files` | 7 passed, 1 warning in 0.57s |
| `test_graph_store_index_not_nodes` | 3 passed, 2 warnings in 0.64s |
| `test_inbox_promote_cli_gaps` | 21 passed, 2 warnings in 17.66s |
| `test_large_doc_materialization` | 3 passed, 2 warnings in 1.33s |
| `test_legacy_task_states` | 33 passed, 2 warnings in 64.30s (0:01:04) |
| `test_lifecycle_end_to_end` | 5 passed, 2 warnings in 94.50s (0:01:34) |
| `test_materialization_contract` | 5 passed, 2 warnings in 2.03s |
| `test_materialization_targets_outside_package` | 4 passed, 1 warning in 38.10s |
| `test_operational` | 8 passed, 1 warning in 29.06s |
| `test_output_goldens` | 7 passed, 1 warning in 328.58s (0:05:28) |
| `test_retire_cli` | 13 passed, 2 warnings in 80.90s (0:01:20) |
| `test_role_materialization` | 6 passed, 2 warnings in 1.64s |
| `test_transaction` | 11 passed, 2 warnings in 34.13s |

Hay 37 archivos y todos están verdes. Los nuevos son `test_atoms_merge`, `test_retire_cli` y `test_inbox_promote_cli_gaps`. Los demás usan lo que cambió: closeout (`_close`), el grafo del desk, drawer, retire, el CLI y los goldens. `test_cli` y `test_output_goldens` corrieron sin `--update-golden`.

## Doctor

Corrió `deskops doctor` en solo lectura (sin `--repair`) en `~/proyectos/SLDB_1/{deskops,sldb,spec2viz,scion,pron,UIs/graph_ui}`. Antes corrió con el código base (`f21ab5c8`) y después con HEAD. El `git status --porcelain` de cada desk es el mismo antes y después de cada corrida. Las capturas completas están en `coord2-ccconfig/cc35c/doctor-before/` y `doctor-after/`.

| desk | hallazgos antes | exit antes | después (HEAD final `2f5a1682`) |
|---|---|---|---|
| deskops | 10 | exit=0 | idéntico byte a byte |
| sldb | 18 | exit=1 | idéntico byte a byte |
| spec2viz | 7 | exit=1 | idéntico byte a byte |
| scion | 5 | exit=1 | idéntico byte a byte |
| pron | 5 | exit=1 | idéntico byte a byte |
| graph_ui | 8 | exit=1 | idéntico byte a byte |

Los errores que ya había (spec2viz, scion, pron y graph_ui con modelos sin registrar; sldb con modelos que no se importan; pron sin estructura) son anteriores a este nodo y no cambian.

### Grafo

Se compararon las extracciones del grafo, `extract_declared_edges`, en los 6 desks reales, base contra HEAD, porque los dos patrones nuevos agregan aristas:

| desk | aristas | missing |
|---|---|---|
| deskops | 228 → 238 (+10 `drawer-bullet`, Board del drawer → tareas del drawer) | 11 → 11 |
| sldb | 297 → 297 | 11 → 11 |
| spec2viz | 258 → 258 | 0 → 0 |
| scion | 5 → 5 | 0 → 0 |
| pron | 0 → 0 | 0 → 0 |
| graph_ui | 20 → 20 | 6 → 6 |

`ATOM_ID` no agrega aristas en ningún desk real: la forma `atom:atom-` aparece en un solo lugar, el frontmatter de una pill.

## Líneas

`wc -l`, base `f21ab5c8` y después (HEAD):

| archivo | antes | después | Δ |
|---|---|---|---|
| `deskops/services/atoms.py` | 869 | 794 | -75 |
| `deskops/services/retire.py` | 233 | 157 | -76 |
| `deskops/services/drawer.py` | 282 | 290 | +8 |
| `deskops/services/closure.py` | 1489 | 1494 | +5 |
| `deskops/services/references.py` | 0 | 225 | +225 |
| `deskops/graph/desk_graph.py` | 212 | 225 | +13 |
| `deskops/atom_references.py` | 91 | 91 | 0 |

## Hipótesis para sldb

- **H-a (b2).** `referrers(store, target)` y `rewrite_references(...)` no ven menciones en un proyecto cuyo grafo se arma en proceso.
  - Por qué: leen el grafo de `store.yaml` (`optional_graph` → `project_graph(store)`), y deskops no declara `project_graph`. Su `closed_document` es código (DO8; nota H2 de CC33c en sldb `61e9c7a9`).
  - Qué hace deskops mientras: compone `resolve_target` + `find_hits` y `rewrite_references` (campos) + `rewritten_line` + `replace_text` (menciones). Eso repite el bucle `_write`/`_planned_text` de `rewrite_references.py` (unas 20 líneas en `_rewrite_mentions`).
  - Propuesta: un parámetro `graph: ProjectGraph | None` (o `config`) en `referrers` y `rewrite_references`. Cuando entre, `_rewrite_mentions` se borra y las dos funciones de `references.py` llaman a la API pública. Con H2 resuelta (declarar `project_graph` en store.yaml), también.
  - Desk mínimo que lo reproduce: `deskops init` en tmp_path, un átomo `atom-a` y `desk/tasks/task-ref.md` con "Depends on atom:atom-a." `sldb.api.referrers(store, "atom-a")` devuelve `[]`; `find_hits(location, target, desk_graph(root))` devuelve la mención en `desk/tasks/task-ref.md:3`.
- **H-b.** `rewrite_references` no admite excluir fuentes.
  - En atoms merge, el átomo destino y el stub los escribe merge. deskops los excluye de las menciones, pero no puede excluirlos de los campos. Hoy `AtomDoc` no declara campos de referencia, así que no pasa.
  - Propuesta: `excluded_sources=`.
- **H-c.** Una mención de línea (`LineMentions`) también lee el frontmatter, salvo los campos de `skipped_frontmatter_fields`. Así, un campo declarado (`pills: [desk/contexts/pill-x.md]`) aparece dos veces en `find_hits`: como `schema` y como `mention`.
  - deskops descarta las menciones del frontmatter de un documento trackeado (`_in_frontmatter` en `references.py`).
  - Propuesta: que `find_hits` no devuelva como mención una línea del frontmatter que ya es un hit `schema` del mismo documento.

## Desvíos

1. **Imports de GD22 diferidos** en `references.py`, como ya hacía `services/replace.py` con `replace_text`. Así, importar deskops no depende del sldb que tenga delante: con el sldb hermano atrasado (ver Tests), un import arriba del módulo rompía la importación de `deskops.cli.main` en 17 archivos de tests.
2. **retire ya no rechaza por menciones que el grafo no ve.**
   - Antes, cualquier archivo de `desk/`, `docs/`, README o AGENTS que contuviera el stem o la ruta bloqueaba el retire.
   - Ahora solo bloquean las menciones que capturan los `MentionPattern` del desk, por ejemplo `SOURCE_PATH` en tareas e issues, o una sección Related de cualquier superficie. Un archivo que no es documento trackeado ni nodo del grafo (una nota de `desk/logbook/`) no tiene referrers.
   - `test_retire_refuses_while_referenced_unless_forced` pasó del caso logbook + `docs/guide.md` a una pill nombrada por su ruta en la prosa de una tarea.
   - Además, la ruta seguida de un punto final de oración no la captura `SOURCE_PATH` (su lookahead `(?![\w/.-])`, de CC33c); no se cambió para no mover aristas.
3. **retire en un desk sin store no toca el Board**, porque no hay índice de campos. Se quitó de `test_board_portable_references.py` la aserción sobre `_pill_reference_matches`, la función borrada; el resto del test sigue igual y pasa.
4. **Menciones en frontmatter** (H-c): deskops las cuenta como campo en documentos trackeados.
5. **Atom para docs/:** no se capturó un átomo nuevo en `desk/atoms/` antes de cambiar `docs/operator-manual.md`, porque el brief prohíbe escribir en `desk/` salvo lo que escriba deskops por el nodo. El cambio del manual describe el comportamiento del CLI, no una regla nueva de workflow.
6. `RetireResult.boards` (lo que imprime `Unrouted from <file>`) ahora lista también las tareas de las que se quitó la pill, además del Board. La CLI no cambió.
