## Base de lectura

**DATO DEL SUPERVISOR** (`tester-facts.log`): `HEAD deskops 92ed7ed6`, `sldb 77bd6d00`, `UIs/graph_ui 134a665`, `spec2viz 10df4f0`, `pron e1e9df0`; los cuatro checks de plan salen 0.
**LECTURA PROPIA**: código, tests y `dag.yaml` abiertos en las líneas citadas. No ejecuté tests ni git.

## Sección 1

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 1.1 | `operaciones.md:11-20`; commits y gates descritos | PASS |
| 1.2 | `dag.yaml:113-121` (`G_WRITE_POLICY: satisfied`), `dag.yaml:122-133` (`G_WRITE_CONTRACT pending`, `accepted_scope_nodes: []`) | PASS |
| 1.3 | Contrato dice deskops `826ca4a0`; supervisor da `92ed7ed6`. `sldb 77bd6d00`, `graph_ui 134a6653`, `pron e1e9df0c` sí coinciden. `git diff/status` no verificable sin git. | **FAIL** |
| 1.4 | `operations.py:215-219` (`.deskops.log`); `workspace.py:166,251`; `atoms.py:51,109,155,168,195,266,329`; `atoms.py:52` delega; `.gitignore:5` deskops y `:8` graph_ui ignoran; sldb/spec2viz no lo ignoran | PASS |
| 1.5 | `G_CLOSEOUT`: `dag.yaml:1740,1779,1817,1980,2148,2190,2240`; `G_PAYLOAD_PRECONDITION`: `dag.yaml:1270,1314,1358,1438`; `G_SLDB_WRITE`: `dag.yaml:1397,2890`; `G_UI_WRITE` 14 IDs: `dag.yaml:207-221`. Pero `G_SOURCE`: `dag.yaml:1465-1470` la variante editable de WS21 lo declara en `requires`, contra «ninguna tarea lo declara». | **FAIL** |

## Sección 2.1 — Lecturas

| Fila | Evidencia real | Veredicto |
|---|---|---|
| R01 | `operations.py:301`; tests `test_cli.py:986,998` | PASS |
| R02 | `operations.py:396`; `ARTIFACT_MODELS` tiene **10** entradas (`operations.py:61-72`), no 9, y el rango 55-66 es erróneo; test `test_cli.py:1975` | **FAIL** |
| R03 | `operations.py:412,422`; `lifecycle.py:123-151`; `edge_reading.py:28`; tests `test_cli.py:1681,1817,1929` | PASS |
| R04 | `operations.py:452`; tests `test_cli.py:2391,1975` | PASS |
| R05 | `services/tasks.py:98`; tests `test_cli.py:829,872,911,929` | PASS |
| R06 | `message.py:145,150`; tests `test_message_cli.py:97,146,221`; no construye `DeskopsOperations` | PASS |
| R07 | `services/issues.py:354`; test `test_issue_cli.py:127` | PASS |
| R08 | `operations.py:602,711-718`; `closeout.py:_verify`; `closeout_gates.py:208-221,231-249`; tests `test_closeout.py:392,418,476,499` | PASS |
| R09 | `core.py:11-16`; `faq` y `repo whoami` no abiertos, como declara la fila | PASS (LEC) |
| R10 | `runtime.py:157-182`; `supervise.py:44-66`; `graph.py:53-106` | PASS (LEC) |
| R11 | `deskops_routes.py:34,41,46,67,79`; tests `test_mindmap_deskops.py:63,77,109,125` | PASS |
| R12 | `document_serialization.py:8-9,24-32`; `test_serve.py:66,84-85,616`; `test_mindmap_endpoints.py:294` | PASS |

## Sección 2.2 — Diagnósticos

| Fila | Evidencia real | Veredicto |
|---|---|---|
| D01 | `doctor.py:_store_check` lanza `sldb stores check`; `store_check.py:18-29`; `open_store.py:37-41`; `scan_cache.py:20,60-67`; registry `doctor mutates=True`, `status mutates=False` | PASS (LEC) |
| D02 | `doctor.py:_check_structure,_check_models`; `test_cli.py:245,258`; `test_doctor_model_registration.py:119` prueba `--repair` registrando modelos; rama `scaffold_desk` no tiene prueba directa | PASS parcial |
| D03 | `atoms.py:154-155` (`validate_atoms` → `ensure_workspace`); registry `mutates=False`; tests `test_atoms_cli.py:34,47` | PASS (LEC) |
| D04 | `drift.py`; tests `test_cli.py:2785,2808`; cuerpo de `drift_check_knowledge_surfaces` no abierto | PASS (LEC) |
| D05 | `store_check.py:18-29`; `store_check_apply.py:11-18`; `open_store.py:37-41`; `scan_cache.py` | PASS (LEC) |

## Sección 2.3 — Mutaciones Deskops

| Fila | Evidencia real | Veredicto |
|---|---|---|
| W01 | `operations.py:1330-1332` (FileExistsError); `closeout_gates.py:77-98`; `specs/compiler.py:35-60`; `model_introspection.py:183-210`; tests `test_cli.py:701,743`, `test_operational.py:34,58,78`, `test_closeout_declared_evidence.py:244`, `test_add_task_from_drawer.py:29` | PASS |
| W02 | `operations.py:271-282,1297-1327`; tests `test_cli.py:1246,1297,1333,1438,1450,1614`; `test_doc_io.py:104` | PASS |
| W03 | `operations.py:271-282`; grep `protected/protegid` sin coincidencias en `deskops/**/*.py`; tests ajenos en `test_graph_cli.py:106`, `test_migrate_desk_stores.py:100` | PASS (NOAC) |
| W04 | `lifecycle.py:154-190`; `tasks.py:172-209`; `task_lifecycle.yaml:27,34,41-42`; tests `test_cli.py:1817,2017`, `test_operational.py:135`, `test_inbox_promote_cli_gaps.py:184` | PASS |
| W05 | `tasks.py:179-191`; tests `test_inbox_promote_cli_gaps.py:199,211` | PASS (NOAC) |
| W06 | `operations.py:284-300`; test `test_cli.py:1495` | PASS |
| W07 | `operations.py:243-269,1344`; tests `test_cli.py:2307,2348,2487,2528,2567,2601`, `test_retire_cli.py:44`, `test_operational.py:13` | PASS |
| W08 | `operations.py:271-282`; tests `test_cli.py:1377,1464,2717` | PASS |
| W09 | `operations.py:271-282`; solo `add/list/show board` probados (`test_cli.py:2528`); sin test de `edit board` | PASS (LEC) |
| W10 | `drawer.py:141-181`; tests `test_inbox_promote_cli_gaps.py:349,363,390` | PASS |
| W11 | `drawer.py:97-135,246-274`; tests `test_cli.py:659`, `test_inbox_promote_cli_gaps.py:72,92,105,120` | PASS (NOAC) |
| W12 | `message.py:97-135`; tests `test_message_cli.py:97,154`, `test_message_delivery.py:149,181` | PASS |
| W13 | `message.py:172-187`; tests `test_cli.py:593`, `test_message_cli.py:172,199,248` | PASS |
| W14 | `domain_tree.py:129-140,214-218`; tests `test_domain_tree.py:58,138`; sin prueba de id duplicado/provenance | PASS |
| W15 | `domain_tree.py:117-127`; test `test_domain_tree.py:58` (incluye duplicado al final) | PASS |
| W16 | `domain_tree.py:142-166`; test `test_domain_tree.py:104` | PASS |
| W17 | `atoms.py:258-382,624,688`; tests `test_atoms_split.py:54,100`, `test_atoms_merge.py:110,158`, `test_atoms_transactions.py:59,98` | PASS |
| W18 | `atoms.py:195-260,420-524`; tests `test_atoms_create_from_source.py:20`, `test_atoms_cli.py:77,98` | PASS |
| W19 | `closure.py:72,271,370-538`; tests `test_closeout.py:132,211,370`, `test_lifecycle_end_to_end.py:48,192`, `test_closeout_declared_evidence.py:137` | PASS |
| W20 | `closure.py:140-181,186-260`; tests `test_closeout.py:755,827,940,1025` | PASS |
| W21 | `issues.py:303-344`; `retire.py:200`; tests `test_issue_cli.py:88,154`, `test_retire_cli.py:74,116` | PASS |
| W22 | registry `atoms add-namespace`; test `test_cli.py:385` | PASS |
| W23 | `atoms.py:102-152`; `test_atom_folder_axis.py` no abierto | PASS (LEC) |
| W24 | `core.py:InitCLI`; tests `test_cli.py:124,159,274,346` | PASS |
| W25 | `replace.py:81`; `desk.py:284,334`; tests citados no leídos | PASS (LEC) |
| W26 | `graph.py:21-51`; `runtime.py:70-110`; `scion.py:366`; sin abrir cuerpos completos | PASS (LEC) |

## Sección 2.4 — Mutaciones sldb

| Fila | Evidencia real | Veredicto |
|---|---|---|
| S01 | `save_plan.py:31-47,63-66`; `save_routes.py:23,103`; `actor.py:11-24`; tests `test_serve.py:187,228,247` | PASS |
| S02 | `save_plan.py:49-54`; `payload_save.py:44-49`; `payload_save_steps.py:68-96`; tests `test_serve.py:213,187` | PASS |
| S03 | `save_plan.py:57-60`; `save_routes.py:103-107`; test `test_serve.py:1095` | PASS |
| S04 | `save_single.py:13-20`; test `test_serve.py:28` | PASS (NOAC) |
| S05 | `docs_routes.py:28-35,55-72,103-109`; tests `test_serve.py:616,634,645,658,670` | PASS |
| S06 | `docs_routes.py:38-46`; tests `test_serve.py:682,698,710,727` | PASS |
| S07 | `payload_save.py:16`; `fields_save.py:6-14`; `sldb_adapter.py:286-297`; `payload_editor.py:24-37` | PASS (NOAC) |
| S08 | `create_document.py:50-51`; `store/ops.py:36`; `create_document.py:22` docstring | PASS (NOAC) |
| S09 | `test_serve.py:444-500`; `test_mindmap_endpoints.py:420,435,469,477` | PASS |

## Sección 2.5 — Mutaciones graph_ui

| Fila | Evidencia real | Veredicto |
|---|---|---|
| U01 | `persistence.py:70,77,84,101-102,129-136`; `sldb_adapter.py:299-312`; tests `test_mindmap_persistence.py:29,45,54,66` | PASS |
| U02 | `serve.py:272-311` (remote save sin guarda), `serve.py:387-398` precede a `:431-434`; grep sin whitelist/protected | PASS (LEC) |
| U03 | `deskops_routes.py:21,86,98,103,111,113-116`; tests `test_mindmap_deskops.py:77,94,109,136` | PASS |
| U04 | `views_routes.py:56-66`; `sldb_adapter.py:427-434`; `serve.py:382-385` | PASS (LEC) |
| U05 | `test_mindmap_endpoints.py:420,435,469,477` | PASS |

## Sección 2.6 — Faltantes

| Fila | Evidencia real | Veredicto |
|---|---|---|
| X01 | `models/inbox.py:37-61` sin reply/thread; `message.py:97-135` sin vínculo. Pero grep `reply\|in_reply_to\|thread` en `deskops/**/*.py` da **cero** coincidencias, no «solo prosa en runtime/scion.py» | **FAIL** |
| X02 | `drawer.py` no ofrece captura directa; sección 7 sin prueba | PASS |
| X03 | `domain_tree.py:129` sin provenance; grep `provenance` en `test_domain_tree.py` sin coincidencias | PASS |
| X04 | solo `_append_task_to_board` (`operations.py:527`); `edit board tasks` reemplaza | PASS |
| X05 | `models/run.py:48-83` sin decisión; grep solo `graph/self_reflection.py` y `scion.py` | PASS |
| X06 | `scion.py:12` prosa; `cli/commands/runtime.py` sin dispatch/reply | PASS |
| X07 | igual que X06 | PASS |
| X08 | grep `raw.?source` en `sldb/api` sin resultados; firmas reciben payload (`payload_save.py:16`, `create_document.py:22`) | PASS |

## Sección 2.7

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 2.7 | `registry.py` cuenta 17 agregadores y 96 hojas (43 del grupo add/edit/bind/list/show/advance + 53 restantes). Tabla de cobertura suma 96 hojas, sin duplicados ni faltantes. | PASS |

## Sección 3

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 3.1 | `models/base.py:19,36-47` (status en PrimitiveDoc; current_node/history en OperationalArtifactDoc); `lifecycle.py:179-184`; `closure.py:147-148`; `tasks.py:184-187`; `drawer.py:264`; `model_introspection.py:183-210` | PASS con matiz: `status` no lo añade `OperationalArtifactDoc`, viene de `PrimitiveDoc` |
| 3.2 | `save_plan.py` acepta payload completo sin filtro; `persistence.py` no filtra; contrato declara que ninguna capa lo hace cumplir | PASS (declara el hueco HO-02) |
| 3.3 TaskDoc id | `operations.py:277-278`; test `test_cli.py:1614` | PASS |
| 3.3 TaskDoc status | `lifecycle.py:179-180`, `closure.py:147`, `tasks.py:184-186`, `drawer.py:264`, `compiler.py:40` | PASS |
| 3.3 TaskDoc current_node | `lifecycle.py:184`, `tasks.py:187`, `compiler.py:60` | PASS |
| 3.3 TaskDoc history | `lifecycle.py:181-183`, `closure.py:148` | PASS |
| 3.3 TaskDoc closeout_evidence | `closeout_gates.py:23,77-98`; `operations.py:602`; `edit` no valida vocabulario | PASS |
| 3.3 TaskDoc from_drawer | `drawer.py:81-90`; guarda real en `drawer.py:155-163`; la cita 183-196 apunta a `_tasks_recording` | **FAIL** |
| 3.3 TaskDoc campos de contenido | `operations.py:271-282`; tests `test_cli.py:1333` | PASS |
| 3.3 TaskDoc pills | `operations.py:284-300`; test `test_cli.py:1495` | PASS |
| 3.3 BoardDoc tasks | `operations.py:527`; `closure.py:437`; `retire.py:200`; `operations.py:271` | PASS |
| 3.3 BoardDoc status/current_node/history | grep `current_node` solo en tasks/lifecycle/compiler/next_actions/operations; no escritura sobre Board | PASS |
| 3.3 BoardDoc title/scope/... | `operations.py:271-282` | PASS |
| 3.3 PillDoc status/current_node/history | solo `edit pill`; test `test_cli.py:2717` | PASS |
| 3.3 PillDoc what/why/... | `operations.py:271-282` | PASS |
| 3.3 RitualDoc | `lifecycle.py:202-236,254-275`; re-render/archivo de rituales | PASS |
| 3.3 RelationDoc/RelationTypeDoc | `desk/lifecycle/*.md` (`condition`, `source_id`, `target_id`, `relation_type`); `lifecycle.py:275-355` | PASS |
| 3.3 InboxNote status/ack_* | `message.py:172-187` | PASS |
| 3.3 InboxNote created_at/sender/target | `message.py:97-125` | PASS |
| 3.3 InboxNote kind/title/body | `message.py:97-125` | PASS |
| 3.3 AtomDoc id | `atoms.py` valida slug; `create_artifact` usa patrón de spec | PASS |
| 3.3 AtomDoc answer redirect | `atoms.py:311,371,624,688` | PASS |
| 3.3 AtomDoc tags/provenance | `atoms.py:720-742` | PASS |
| 3.3 ProtoAtomDoc typed_as/content | `domain_tree.py:142-166` | PASS |
| 3.3 ProtoAtomDoc id/title/content/tags | `domain_tree.py:129-140` | PASS |
| 3.3 ProtoAtomDoc provenance | `models/protoatom.py:48`; sin escritor (X03) | PASS |
| 3.3 CrossroadDoc id/path | `domain_tree.py:117-127` | PASS |
| 3.3 MaterializationContractDoc | `add/edit materialization` CLI | PASS |
| 3.3 RepositoryDoc | `repo register/remove` | PASS |
| 3.3 DeskFAQDoc/StepDoc | `add/edit` CLI | PASS |
| 3.3 RoleDoc/RuntimeProfileDoc | no verificado contra `navegacion.md §11` | PASS (no verificado) |
| 3.3 RunDoc | `models/run.py:48-83`; `scion.py:366` | PASS |
| 3.3 Issue | `issues.py:303-344` | PASS |

**Comprobación adicional «ningún estado editable por payload»**: **FAIL** en el código actual. `edit_artifact_field` solo bloquea `id` (`operations.py:277-278`), por lo que `edit task status/current_node/history` funciona; `save_document_payload` acepta el payload completo (`payload_save.py:16`). El contrato lo reconoce en W03/3.2/HO-02, pero la propiedad no se cumple hoy.

## Sección 4

| Fila | Evidencia real | Veredicto |
|---|---|---|
| 4.1 | `deskops_routes.py:34,41,46,67`; `main.py:124,155-182`; `test_cli.py:3048`; solo `.mutates` en `main.py:124,155-162` | PASS |
| 4.2 | Canales y huecos: `WS19.1`, `WS19.2`, `WS25.1`, `WS25.2`, `WS26.1`, `WS26.2`, `WS27.1`, `WS27.2`, `WS28`, `WS34.1`, `WS34.2`, `WS39`, `WS42`, `WS20`, `WS45` existen en `dag.yaml`; HO-09/HO-11/HO-12 no tienen nodo productor | PASS |
| 4.3 | `operations.py:986`; `desk/rituals/phase.md:14-16`; `dag.yaml:1808` | PASS |

## FAIL y corrección implicada

- **§1.3**: commit deskops citado `826ca4a0` ≠ HEAD del supervisor `92ed7ed6`. Corregir la fila y declarar el commit real del despacho.
- **§1.5**: `G_SOURCE` sí aparece en `requires` de la variante editable de WS21 (`dag.yaml:1465-1470`). Corregir «ninguna tarea lo declara».
- **§2.1 R02**: `ARTIFACT_MODELS` tiene 10 modelos (`operations.py:61-72`), no 9; rango 55-66 erróneo. Corregir a «9 subjects / 10 entradas» y línea 61-72.
- **§3.3 TaskDoc `from_drawer`**: la guarda de `drawer remove` está en `drawer.py:155-163`; `183-196` es `_tasks_recording`. Corregir la cita.
- **§2.6 X01**: no hay ninguna coincidencia de `reply|in_reply_to|thread` en `deskops/**/*.py`; la frase «solo prosa en runtime/scion.py» es falsa. Eliminarla; el HUE se mantiene.
- **Comprobación «ningún estado editable por payload»**: no se cumple en el código; `edit` y `save_document_payload` aceptan `status/current_node/history`. El contrato debe presentarlo como hueco/HO-02, no como propiedad vigente.

## No verificado

- Ejecución de tests, `git status/diff/ls-files`, hashes de commits y `sha256` del contrato (sin herramientas de git/hash).
- Ramas `scaffold_desk` de `doctor --repair`, cuerpo de `drift_check_knowledge_surfaces`, cuerpos completos de W25/W26, `faq`/`repo whoami`, y `spec2viz`.
- Contraste de `RoleDoc/RuntimeProfileDoc` con `navegacion.md §11`.

RESULTADO: FAIL
