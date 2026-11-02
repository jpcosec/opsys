## Base de lectura

- **LECTURA PROPIA**: abrí contrato, código y tests en las líneas citadas. No ejecuté tests, git ni CLI de escritura; ningún veredicto implica runtime.
- **DATO DEL SUPERVISOR** (`tester-facts.log`): `HEAD deskops 3dcefa4f`, `sldb 77bd6d00`, `graph_ui 134a665`, `spec2viz 10df4f0`, `pron e1e9df0`; `sha256 operaciones.md 6a58a2f2…8fb5ee`; los cuatro checks de plan salen 0; `1.3 cita 826ca4a0: HEAD del despacho`.

## Sección 1

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 1.1 | `operaciones.md:11-20`; alcance descrito | PASS |
| 1.2 | `dag.yaml:113-121` (`G_WRITE_POLICY: satisfied`); `dag.yaml:122-160` (`G_WRITE_CONTRACT: pending`, `accepted_scope_nodes: []`) | PASS |
| 1.3 | `operaciones.md:28-33`; supervisor confirma despacho `826ca4a0`; sldb/graph_ui/spec2viz/pron coinciden por prefijo. `92ed7ed6` vs HEAD actual `3dcefa4f` no verificable sin git; la fila declara el commit de despacho, no el HEAD vivo | PASS (árbol y `git diff --stat` no verificados) |
| 1.4 | `operations.py:213-222` (`.deskops.log`), `workspace.py:166,251`, `atoms.py:52,109,155,168,195,266,329`; `.gitignore` deskops y graph_ui ignoran; sldb/spec2viz no | PASS |
| 1.5 | `dag.yaml:33-43` (G_CLOSEOUT satisfied), `:51` G_PAYLOAD_PRECONDITION pending, `:44-49` G_SOURCE producido por WS20, `:195-224` G_UI_WRITE 14 IDs, `:1397,2890` G_SLDB_WRITE, `:1462-1472` variante editable de WS21 declara G_SOURCE | PASS |

## Sección 2.1 — Lecturas

| Fila | Evidencia real | Veredicto |
|---|---|---|
| R01 | `operations.py:301`; `test_cli.py:986,998` | PASS |
| R02 | `operations.py:396`, diccionario `61-72` con 10 entradas (9 sin TaskDoc); `test_cli.py:1975` | PASS |
| R03 | `operations.py:412,422`; `lifecycle.py:123-151`; `edge_reading.py:28`; `test_cli.py:1681,1817,1929` | PASS |
| R04 | `operations.py:452`; `test_cli.py:2391,1975` | PASS |
| R05 | `services/tasks.py:98`; `test_cli.py:829,872,911,929` | PASS |
| R06 | `message.py:145,150`; `test_message_cli.py:97,146,221` | PASS |
| R07 | `services/issues.py:354`; `test_issue_cli.py:127` | PASS |
| R08 | `operations.py:602`; `closeout.py:64-79`; `closeout_gates.py:197-220,228-249`; `test_closeout.py:392,418,476,499` | PASS |
| R09 | `core.py:11-16`; `faq` y `repo whoami` no abiertos, como declara | PASS (LEC) |
| R10 | `graph.py:53-106`; `runtime.py:157-182`; `supervise.py:42-66` | PASS (LEC) |
| R11 | `deskops_routes.py:34,41,46,67,79`; `test_mindmap_deskops.py:63,77,109,125` | PASS |
| R12 | `document_serialization.py:8-9,24-32`; `test_serve.py:66,84-85,616`; `test_mindmap_endpoints.py:294` | PASS |

## Sección 2.2 — Diagnósticos

| Fila | Evidencia real | Veredicto |
|---|---|---|
| D01 | `doctor.py:88-104`; `store_check.py:22`; `open_store.py:37-38`; `scan_cache.py:20,60-67`; registry `doctor` 521 / `status` 528 | PASS (LEC) |
| D02 | `doctor.py:52,120,136`; `test_cli.py:245,258`; `test_doctor_model_registration.py:130` | PASS (LEC) |
| D03 | `atoms.py:154-155`; `test_atoms_cli.py:34,47` | PASS (LEC) |
| D04 | `drift.py:20-29`; `test_cli.py:2785,2808`; cuerpo de `drift_check_knowledge_surfaces` no abierto | PASS (LEC) |
| D05 | `store_check_apply.py:11-22`; `store_context.py:21-24` | PASS (LEC) |

## Sección 2.3 — Mutaciones Deskops

| Fila | Evidencia real | Veredicto |
|---|---|---|
| W01 | `operations.py:527,1330-1332`; `closeout_gates.py:77-98`; `compiler.py:35-60`; `model_introspection.py:183-210`; tests citados existen | PASS |
| W02 | `operations.py:271-282,1235,1297`; tests `test_cli.py:1246,1297,1333,1438,1450,1614`; `test_doc_io.py:104` | PASS |
| W03 | `operations.py:271-282`; grep `protected/protegid` en `deskops/**/*.py` sin coincidencias; test 2717 | PASS (NOAC) |
| W04 | `lifecycle.py:154-190`; `tasks.py:172-209`; `task_lifecycle.yaml:27,34,41-42`; tests citados | PASS |
| W05 | `tasks.py:179-191`; `test_inbox_promote_cli_gaps.py:199,211` | PASS (NOAC) |
| W06 | `operations.py:284-300`; `test_cli.py:1495` | PASS |
| W07 | `operations.py:243-269,1343`; tests `test_cli.py:2307,2348,2487,2528,2567,2601`, `test_retire_cli.py:44`, `test_operational.py:13` | PASS |
| W08 | `test_cli.py:1377,1464,2717` | PASS |
| W09 | `operations.py:271-282`; solo `add/list/show board` probado (`test_cli.py:2528`) | PASS (LEC) |
| W10 | `drawer.py:141-181`; `test_inbox_promote_cli_gaps.py:349,363,390` | PASS |
| W11 | `drawer.py:92-139,246-274`; `test_cli.py:659`; `test_inbox_promote_cli_gaps.py:72,92,105,120` | PASS (NOAC) |
| W12 | `message.py:97-137`; `test_message_cli.py:97,154`; `test_message_delivery.py:149,181` | PASS |
| W13 | `message.py:161-187`; `test_cli.py:593`; `test_message_cli.py:172,199,248` | PASS |
| W14 | `domain_tree.py:129-140,214-218`; `test_domain_tree.py:58,138` | PASS |
| W15 | `domain_tree.py:117-127`; `test_domain_tree.py:58` | PASS |
| W16 | `domain_tree.py:142-166`; `test_domain_tree.py:104` | PASS |
| W17 | `atoms.py:258-382,624,688`; tests split/merge/transactions citados | PASS |
| W18 | `atoms.py:195-260,420-524`; `test_atoms_create_from_source.py:20`; `test_atoms_cli.py:77,98` | PASS |
| W19 | `closure.py:72,271,370-538`; tests `test_closeout.py:132,211,370`, `test_lifecycle_end_to_end.py:48,192`, `test_closeout_declared_evidence.py:137` | PASS |
| W20 | `closure.py:140-181,186-260`; `test_closeout.py:755,827,940,1025` | PASS |
| W21 | `issues.py:303-344`; `retire.py:200`; `test_issue_cli.py:88,154`; `test_retire_cli.py:74,116` | PASS |
| W22 | registry `atoms add-namespace`; `test_cli.py:385` | PASS |
| W23 | `atoms.py:102-152`; `test_atom_folder_axis.py` no abierto | PASS (LEC) |
| W24 | `core.py:24-31`; `test_cli.py:124,159,274,346` | PASS |
| W25 | `replace.py:70-90`; `desk.py:285,334`; tests citados no leídos | PASS (LEC) |
| W26 | `graph.py:21-51`; `runtime.py:70-110`; `scion.py:366` | PASS (LEC) |

## Sección 2.4 — Mutaciones sldb

| Fila | Evidencia real | Veredicto |
|---|---|---|
| S01 | `save_plan.py:33-45,63-67`; `save_routes.py:23,70-90`; `actor.py:11-24`; `test_serve.py:187,228,247` | PASS |
| S02 | `save_plan.py:49-54`; `payload_save.py:47-49,55-56`; `payload_save_steps.py:68-96`; `test_serve.py:213,187` | PASS |
| S03 | `save_plan.py:57-60`; `save_routes.py:94-107`; `test_serve.py:1095` | PASS |
| S04 | `save_single.py:13-20`; `test_serve.py:28` | PASS (NOAC) |
| S05 | `docs_routes.py:28-35,55-67,103-109`; `test_serve.py:616,634,645,658,670` | PASS |
| S06 | `docs_routes.py:38-46`; `test_serve.py:682,698,710,727` | PASS |
| S07 | `payload_save.py:16`; `fields_save.py:6-14`; `sldb_adapter.py:286-297`; `payload_editor.py:24-37` | PASS (NOAC) |
| S08 | `create_document.py:22,50-51`; `store/ops.py:33-36` | PASS (NOAC) |
| S09 | `test_serve.py:444-500` (versión 1→2 en `:487`); `test_mindmap_endpoints.py:420,435,469,477` | PASS |

## Sección 2.5 — Mutaciones graph_ui

| Fila | Evidencia real | Veredicto |
|---|---|---|
| U01 | `persistence.py:70,77,84-85,101-102,129-136`; `sldb_adapter.py:299-312`; `test_mindmap_persistence.py:29,45,54,66` | PASS |
| U02 | `serve.py:272-311,387-398,431-434` (rama remota sin guarda de `Origin`); **pero** `grep -i 'whitelist\|allowlist\|protected\|forbidden\|read_only'` en `GU/{serve,persistence,sldb_adapter,views_routes,deskops_routes}.py` da **cero** coincidencias; `deskops_routes.py:49` es la proyección `**{key: payload.get(...)}`, no un match de esos términos | **FAIL** (evidencia de la negación) |
| U03 | `deskops_routes.py:21,86,96-98,103,111,113-116`; `test_mindmap_deskops.py:77,94,109,136` | PASS |
| U04 | `views_routes.py:29-33,56-66`; `sldb_adapter.py:427-434`; `serve.py:382-385` | PASS (LEC) |
| U05 | `test_mindmap_endpoints.py:420,435,469,477` | PASS |

## Sección 2.6 — Faltantes

| Fila | Evidencia real | Veredicto |
|---|---|---|
| X01 | `models/inbox.py:37-61`; `message.py:97-137`; grep `reply\|in_reply_to\|thread` en `deskops/**/*.py`: cero | PASS |
| X02 | `operaciones.md:400-432`; ninguna opción con prueba real | PASS |
| X03 | `domain_tree.py:129-140`; grep `provenance` en `test_domain_tree.py`: cero | PASS |
| X04 | solo `_append_task_to_board` (`operations.py:527`); `edit board tasks` reemplaza entera | PASS |
| X05 | `models/run.py:48-83`; grep `decision/approve`: `graph/self_reflection.py`, `runtime/scion.py` | PASS |
| X06 | `scion.py:12`; `cli/commands/runtime.py` sin subcomando de dispatch/reply | PASS |
| X07 | Igual que X06 | PASS |
| X08 | grep `raw.?source` en `sldb/src/sldb/api`: cero; `payload_save.py:16`; `create_document.py:22` | PASS |

## Sección 2.7

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 2.7 | `registry.py`: 17 agregadores (message, promote, drawer, issue, add, edit, bind, list, show, advance, repo, desk, atoms, graph, drift, closeout, runtime) y 96 hojas; la tabla suma 96 sin duplicados ni faltantes | PASS |

## Sección 3

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 3.1 | `models/base.py:19,36-47`; `lifecycle.py:179-184`; `closure.py:147-148`; `tasks.py:184-187`; `drawer.py:264`; `model_introspection.py:183-210`; el texto declara que hoy el código permite editarlo | PASS |
| 3.2 | `payload_save.py:16` y `persistence.py:70-136` sin filtro; contrato declara el hueco HO-02 | PASS |
| 3.3 TaskDoc `id` | `compiler.py:36`; `operations.py:277-278`; `test_cli.py:1614` | PASS |
| 3.3 TaskDoc `status` | `lifecycle.py:179-180`; `closure.py:147`; `tasks.py:184-186`; `drawer.py:264`; `compiler.py:40` | PASS |
| 3.3 TaskDoc `current_node` | `lifecycle.py:184`; `tasks.py:187`; `compiler.py:60` | PASS |
| 3.3 TaskDoc `history` | `lifecycle.py:181-183`; `closure.py:148` | PASS |
| 3.3 TaskDoc `closeout_evidence` | `closeout_gates.py:23,77-98`; `operations.py:602`; `edit` no valida vocabulario | PASS |
| 3.3 TaskDoc `from_drawer` | `drawer.py:81-90`; guarda en `drawer.py:155-163`; `_tasks_recording` en `:183-196` | PASS |
| 3.3 TaskDoc campos de contenido | `operations.py:271-282`; `test_cli.py:1333` | PASS |
| 3.3 TaskDoc `pills` | `operations.py:284-300`; `test_cli.py:1495` | PASS |
| 3.3 BoardDoc `tasks` | `operations.py:527`; `closure.py:437`; `retire.py:200` | PASS |
| 3.3 BoardDoc `status/current_node/history` | grep `current_node` sin escritura sobre Board; solo TaskDoc | PASS |
| 3.3 BoardDoc `title/scope/...` | `operations.py:271-282` | PASS |
| 3.3 PillDoc `status/current_node/history` | solo `edit pill`; `test_cli.py:2717` | PASS |
| 3.3 PillDoc `what/why/...` | `operations.py:271-282` | PASS |
| 3.3 RitualDoc | `lifecycle.py:204,254,275` | PASS |
| 3.3 RelationDoc/RelationTypeDoc | `desk/lifecycle/*.md`; `lifecycle.py:275-355` | PASS |
| 3.3 InboxNote `status/ack_*` | `message.py:161-187` | PASS |
| 3.3 InboxNote `created_at/sender/target` | `message.py:97-125` | PASS |
| 3.3 InboxNote `kind/title/body` | `message.py:97-125` | PASS |
| 3.3 AtomDoc `id` | `operations.py:277-278`; convención `atom-<slug>` | PASS |
| 3.3 AtomDoc `answer` redirect | `atoms.py:311,371,624,688` | PASS |
| 3.3 AtomDoc `tags/provenance` | `atoms.py:719-742`; `provenance` se comprueba en `validate_atoms` | PASS |
| 3.3 ProtoAtomDoc `typed_as/content` | `domain_tree.py:142-165` | PASS |
| 3.3 ProtoAtomDoc `id/title/content/tags` | `domain_tree.py:129-140` | PASS |
| 3.3 ProtoAtomDoc `provenance` | `models/protoatom.py:48`; sin escritor (X03) | PASS |
| 3.3 CrossroadDoc `id/path` | `domain_tree.py:117-127` | PASS |
| 3.3 MaterializationContractDoc | registry `add/edit materialization` | PASS |
| 3.3 RepositoryDoc | registry `repo register/remove`; W25 | PASS |
| 3.3 DeskFAQDoc/StepDoc | registry `add/edit` | PASS |
| 3.3 RoleDoc/RuntimeProfileDoc | `navegacion.md:387` (UF09) | PASS |
| 3.3 RunDoc | `models/run.py:48-83`; `scion.py:366` | PASS |
| 3.3 Issue | `issues.py:303-344` | PASS |

**Comprobación adicional — «ningún estado editable por payload»**: no se cumple en el código actual; `edit_artifact_field` solo bloquea `id` (`operations.py:277-278`) y `save_document_payload` acepta el payload completo (`payload_save.py:16`). El contrato ya lo declara como límite vigente y como regla de UI (3.1/3.2, HO-02), no como propiedad; por eso no lo marco como FAIL de la fila.

## Sección 4

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 4.1 | `deskops_routes.py:34,41,46,67`; `main.py:124,155-182`; `test_cli.py:3048`; `.mutates` solo en `main.py:124`. **Pero** `serve.py` tiene timeouts en `:100,:111,:124,:175`; afirmar que `:175` es «el único timeout de ese archivo» es falso | **FAIL** |
| 4.2 | Huecos y productores: `HO-02→WS19.1/WS26.1`, `HO-05/WS19.2`, `HO-08/WS20`, `HO-01→WS26.1,WS26.2,WS27.2,WS28,WS25.1,WS25.2,WS42`, `HO-12/HO-09/HO-11` sin productor, `HO-13/WS27.1`, `HO-14/WS26.2`, `HO-16/WS34.1-2`; todos los WS citados existen en `dag.yaml` (`1306,1350,1390,1490,1654,1688,1771,1808,1889,1930,1972,2427,2465,2632,2747,2883,2888`); los HO sin productor no tienen nodo | PASS |
| 4.3 | `operations.py:986` (uso en `:749`); `closure.py:458,46-58`; `phase.md:14-16`; `dag.yaml:1808`; grep `overlap/solap/disjoint` solo `workspace.py:351` | PASS |

## FAIL y corrección implicada

- **§4.1**: la frase «el único timeout de ese archivo» es falsa; `GU/serve.py` tiene `timeout=15` en `:100`, `timeout=15` en `:111`, `timeout=30` en `:124` y `timeout=10` en `:175`. Corrección: eliminar «único» o enumerar los cuatro y aclarar que el de `:175` es el del subproceso de lectura.
- **§2.5 U02**: la evidencia de la negación atribuye un match a `deskops_routes.py:49` para la búsqueda de `whitelist|allowlist|protected|forbidden|read_only`; esa búsqueda da cero coincidencias y la línea 49 es una proyección de claves de lectura, no un filtro. Corrección: declarar «sin coincidencias en esos cinco archivos» y citar `deskops_routes.py:49` solo como proyección, no como resultado del grep.

## No verificado

- Ejecución de tests, `git status/diff/ls-files`, pertenencia de commits y `sha256` del contrato (sin git/hash): incluye la limpieza del árbol de 1.3 y la relación `92ed7ed6`/`3dcefa4f`.
- Cuerpos de W25/W26, `test_atom_folder_axis.py`, `test_projection_views.py`, rama `scaffold_desk` de `doctor --repair`, cuerpo de `drift_check_knowledge_surfaces`, `faq`/`repo whoami`, `spec2viz` y el diálogo/componentes de UI de graph_ui.

RESULTADO: FAIL
