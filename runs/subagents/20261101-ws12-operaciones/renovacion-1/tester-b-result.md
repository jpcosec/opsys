## Datos del supervisor (no lectura propia)

- `tester-facts.log`: `HEAD deskops: 92ed7ed6`; `sldb: 77bd6d00`; `UIs/graph_ui: 134a665`; `spec2viz: 10df4f0`; `pron: e1e9df0`.
- `sha256 operaciones.md: f91227ec…35f27`; los cuatro chequeos del supervisor salen `exit 0`.
- No ejecuté nada: los PASS de tests significan «existe y su cuerpo se leyó», no «se corrió».

## Lectura propia

Abrí `operaciones.md` §§5–9 completas y, con esas rutas relativas, `deskops/{operations,doc_io,workspace,domain_tree}.py`, `deskops/services/{tasks,closure,closeout_gates,drawer,atoms}.py`, `deskops/cli/commands/{message,closeout,runtime,doctor}.py`, `deskops/runtime/scion.py`, `tests/{test_message_cli,test_inbox_promote_cli_gaps,test_domain_tree,test_doc_io,test_atoms_transactions,test_operational,test_closeout,test_lifecycle_end_to_end}.py`, `../sldb/src/sldb/{cli/serve/save_plan,cli/serve/save_routes,cli/serve/save_single,cli/serve/docs_routes,api/documents/payload_save,api/documents/create_document,api/documents/document_serialization,store/io/lock,store/journal/lock,store/ops}.py`, `../UIs/graph_ui/frontends/mindmap/{deskops_routes,persistence,serve,views_routes,sldb_adapter}.py` y sus tests.

## §5 Política de coordinador

| # | Afirmación | Evidencia real | Veredicto |
|---|---|---|---|
| 5.1-1 | P03: con otro coordinador escribiendo, lectura/handoff | `decisiones.md`, fila P03 | PASS |
| 5.1-2 | T-P03: lock solo UI no basta | `decisiones.md`, fila T-P03 | PASS |
| 5.1-3 | T-P03.1: WS12 define, no fija lock/detección, ausencia no declara exclusividad | `root-decision-20261101.md`, punto 3 | PASS |
| 5.1-4 | Cita de WS19.1 en `dag.yaml:1306` | La frase «modo manual exclusivo (P03)» está en `dag.yaml:1329`; 1306 es el inicio del nodo | **FAIL** |
| 5.2-1 | «Escritor» incluye UI/CLI/agente/coordinador/editor/git | Normativa; coherente con `dag.yaml:753-757` | PASS |
| 5.2-2 | Modo exclusivo afirma conjunto de escritores, no un lock | Normativa | PASS |
| 5.3-F1 | Patrón de configuración confiable existe para aliases; no hay campo/lectura de exclusividad | `navegacion.md:89-96`; grep `exclusiv` en `deskops/**/*.py`, `sldb/**/*.py`, `GU/**/*.py`: solo grupos argparse y prosa de Scion | PASS |
| 5.3-F2a | `runtime workers` y `/api/workers`; error devuelve lista vacía con `error` | `runtime.py:157-182,199-211` (incluye `cwd`); `serve.py:156-193` | PASS |
| 5.3-F2b | `revision`/`expected` detectan cambio ocurrido, no escritor presente | `deskops_routes.py:113-116`; `save_plan.py:50` | PASS |
| 5.3-F2c | `store.lock` advisory no bloqueante; solo índices | `SL/store/io/lock.py:27-51`; `payload_save_steps.py:87` | PASS |
| 5.3-F2d | `git status`/`rev-parse` no distinguen autor | Normativa; sin cita de código | PASS |
| 5.3-F3 | Autoridad compartida probada no existe | Ver 6.1-C y 6.4 | PASS |
| 5.3-Scion | Plantilla Scion dice «the only writer of that desk/», no es señal consultable | `scion.py:204-216` | PASS |
| 5.4-1 | Sin F1 → lectura/handoff | Normativa | PASS |
| 5.4-2 | F1 + evidencia contraria → handoff, no reintenta | Normativa | PASS |
| 5.4-3 | F1 + error/lista vacía → falta de evidencia | `serve.py:172-193` devuelve `workers: [], error`; coincide | PASS |
| 5.4-4 | F1 sin evidencia contraria: whitelist con recibo; muestra «declarado…», no «exclusivo comprobado» | Normativa; no declara exclusividad por ausencia | PASS |
| 5.4-5 | Evidencia posterior: no revierte, bloquea siguiente | Normativa; sin mecanismo fijado | PASS |
| 5.5 | Handoff hasta autoridad compartida probada; prueba no existe | 6.4; búsquedas sin `expected` compartido | PASS |
| 5.6-1 | `DeskRoutes.lock` RLock; `adapter.lock` RLock; `SAVE_LOCK` RLock de proceso; `DocTransaction` usa diccionario de proceso | `deskops_routes.py:21,86`; `sldb_adapter.py:80`, usado en `persistence.py:70`; `save_routes.py:23`; `doc_io.py:247-250` | PASS |
| 5.6-2 | Grep `flock/fcntl/lockfile/filelock/O_EXCL` en `DK/deskops/**/*.py`: sin coincidencias | Grep propio | PASS |
| 5.6-3 | `test_serialized_advances...:94` prueba dos HTTP en el mismo proceso, no CLI/agente | `GU/tests/test_mindmap_deskops.py:94-104` | PASS |
| 5.6-4 | «El único lock de archivo entre procesos es el de sldb y cubre solo la actualización de índices» | Hay además `journal_lock` con `fcntl.lockf`: `SL/store/journal/lock.py:14-27`, usado en `SL/store/journal/append.py:27` | **FAIL** |
| 5.7 | Obligación de prueba por consumidor | Normativa | PASS |
| 5.8 | No fija formato/vigencia/umbral/lock/API; HO-03 | Normativa; coherente con T-P03.1 | PASS |

## §6 Precondición de escritura

| # | Afirmación | Evidencia real | Veredicto |
|---|---|---|---|
| 6.1-A1 | `expected` compara payload en `save_plan.py:50,58`; graph_ui local en `persistence.py:101-102`; remoto reenvía | Código leído | PASS |
| 6.1-A2 | Compara contra la carga runtime del servidor, no contra el texto del archivo | `save_routes.py:38`; `save_plan.py:50` | PASS |
| 6.1-A3 | Tests 409/obsoleto y lote create/update/delete | `SL/tests/test_serve.py:187-226,213-225`; `GU/tests/test_mindmap_persistence.py:54-64` | PASS |
| 6.1-B1 | `version` publicado en `/graph` y `/docs*`; es `hash_d` | `document_serialization.py:8-9,24-32`; `test_serve.py:66,84-85,616-626` | PASS |
| 6.1-B2 | `revision` = sha256(Board+TaskDoc); `viewRevision` | `deskops_routes.py:79`; `persistence.py:84` | PASS |
| 6.1-B3 | En pron, `expected_hash` por `hash_c` | `PR/kernel/kernel.py:38,49-63` | PASS |
| 6.1-B4 | `version` no se lee al guardar | Grep en `save_routes/save_plan/save_single/payload_save`: sin `version`; único `hash` es journal `payload_save.py:49` | PASS |
| 6.1-B5 | Docstring promete token devuelto; `save_plan` compara payload | `document_serialization.py:25-28` vs. `save_plan.py:50` | PASS |
| 6.1-B6 | `revision`/`viewRevision` solo los compara graph_ui | `deskops_routes.py:114`; `persistence.py:84`; `serve.py:295` | PASS |
| 6.1-B7 | Hay prueba de publicación, no de uso como precondición | Tests citados; grep sin uso de `version` al guardar | PASS |
| 6.1-C1 | No hay precondición compartida; `expected` solo en `save_plan.py:50,58` | Grep en `SL/api` y `SL/cli` | PASS |
| 6.1-C2 | Sin `etag/if_match/content_hash` como precondición en deskops | Grep propio | PASS |
| 6.2-1 | Markdown se escribe antes del lock de índices | `payload_save.py:47-48`; `payload_save_steps.py:76,87` | PASS |
| 6.2-2 | Comparación antes de escritura e índices | `save_plan.py:50`; `save_routes.py:38` | PASS |
| 6.2-3 | `SAVE_LOCK` serializa un `sldb serve`; otro proceso puede escribir entre comparar y escribir | `save_routes.py:23,28-31`; `payload_save.py:47-48` | PASS |
| 6.2-4 | graph_ui local refresca antes de comparar | `persistence.py:72-77` | PASS |
| 6.2-5 | `sldb serve` abre el store al arrancar | No abrí `infraestructura.md:51`; el contrato lo atribuye a infraestructura | No verificado |
| 6.2-6 | `save_document_payload` no rechaza contenido no declarado; `create_document` y `track_document_file` sí | Grep: `create_document.py:60-61`; `track_document_file.py:47-48`; `payload_save.py` sin esas llamadas | PASS |
| 6.2-7 | `deskops edit` rechaza borrar contenido no declarado | `operations.py:1297-1327`; `test_doc_io` no; `test_cli.py::test_edit_task_refuses_to_erase_undeclared_content:1246` | PASS |
| 6.2-8 | Ningún canal reúne precondición y guarda (HO-07) | Síntesis de lo anterior | PASS |
| 6.3-1 | «Es la única precondición que existe en un escritor público» | `PR/kernel/kernel.py:49-63` tiene `expect/_guard` por `hash_c`, usado por `change/add/remove/clean/forget` (`kernel/actions/*_verb.py:31,37`; `sexpr/execution/action_executor.py:75`) | **FAIL** |
| 6.3-2 | Responde a WS19.1/WS19.2 | Normativa | PASS |
| 6.3-3 | No fuerza token ni algoritmo; `version` existe pero no se consume | Ver 6.1-B4 | PASS |
| 6.3-4 | Alcance honesto: no coordina con CLI/agentes | Normativa; coherente con §5 | PASS |
| 6.3-5 | Filas legacy/S07/deskops/views de la tabla de escritores | `save_single.py:13-20` sin `expected`; `payload_save.py` sin precondición; `views_routes.py:56-66`; pero la fila «pron say/eval/MCP: no tienen precondición» contradice `kernel.py:52-56` | **FAIL** (fila pron) |
| 6.4-1 | No afirma frescura/atomicidad/C; P03 no cambia | Normativa | PASS |
| 6.4-2 | «Órdenes que escriben sin precondición (W02–W06, W13, W19–W21, S07)» | W05 rechaza `complete` (`tasks.py:178-180`); W06 PE idempotencia (`operations.py:284-300`); W13 PE `closed` (`message.py:172-173`); W19 ejecuta `verify` (`closure.py:391-395,540-559`); W20 exige ref/estado; W21 exige estado/ref | **FAIL** (literal; son guardas de estado/gate, no `expected`) |
| 6.5 | WS45 debe ensayar (a) frescura, (b) dos peticiones, (c) `version` | Normativa; tests base `test_serve.py:187,213` | PASS |
| 6.6-1 | Fuente en bruto: before-image del texto íntegro; requisitos (i)-(vi) | Normativa; `payload_save_steps.py:76-77` tiene `source_hash/hash_c` | PASS |
| 6.6-2 | X08 hueco, WS20 productor, `G_SOURCE`/`G_SLDB_WRITE` | `dag.yaml` y contrato, coherentes | PASS |

## §7 Captura a drawer y protoátomo

| # | Afirmación | Evidencia real | Veredicto |
|---|---|---|---|
| 7.1-1 | Cita del criterio del DAG en `dag.yaml:723` | La frase «falta conducta de workflow… preservar origen, no crear tarea activa y controlar colisiones» está en `dag.yaml:777-778`, no en 723 | **FAIL** |
| 7.1-2 | «Prueba real» = test en `tests/` del repo dueño, citado | `preflight-disposition.md` y §1.4 | PASS |
| 7.1-3 | No aprueba opción ni crea API/modelo | Normativa | PASS |
| 7.2-1 | Gramática `ruta[::localizador]` o URL; `provenance` en ProtoAtom; `references` en TaskDoc | `atoms.py:540-546,731-742`; `protoatom.py:48`; modelo TaskDoc | PASS |
| 7.2-2 | Ningún test prueba conservación/mostrado tras recargar | Grep `provenance` en `tests/test_domain_tree.py`: sin coincidencias | PASS |
| 7.3-A1 | `create_document` no comprueba existencia (50), rastrea después (51), `track` falla si ya estaba rastreado (ops 33-37) | Código leído | PASS |
| 7.3-A2 | Candidato bajo drawer no está en Board ni `list tasks`; test 105 solo cubre DrawerService; `create_task_bundle` rastrea con `force=True` | `operations.py:301-311` (globs `desk/tasks/task-*.md`); `doc_io.py:92,121`; `test_inbox_promote_cli_gaps.py:105` | PASS |
| 7.3-B1 | 409 por nombre/archivo; tests 634/658; origen y drawer sin prueba; `path` del cliente sin contención | `docs_routes.py:31,66,105-112`; `test_serve.py:634,658` | PASS |
| 7.3-B2 | «No crea tarea activa: Ídem A» | Si el cliente manda `path: desk/tasks/task-x.md`, `docs_routes.py:112` lo acepta y `list_tasks` lo enumera (`operations.py:301-311`); la fila no condiciona esa columna a fijar el `path` | **FAIL** |
| 7.3-C | DrawerService pierde origen (`why` apunta a nota borrada), colisión 110-112, no crea tarea activa con tests 92/105, exige nota previa | `drawer.py:110-112,246-274`; tests 92,105 | PASS |
| 7.3-D | `message send`+`promote`: origen perdido, no transacción común, nombre por timestamp, sin prueba de composición; «No aprobada» | `dag.yaml:758-760` dice literalmente que no queda aprobado | PASS |
| 7.3-E | Wrapper Deskops no existe | Grep y §4.2 | PASS |
| 7.3-Res | Ninguna opción cumple tres propiedades con prueba real; HO-11 sin productor en DAG | Síntesis | PASS |
| 7.4 | Default: captura a drawer no disponible; WS25.2 no la simula | Normativa; coherente con 7.3 | PASS |
| 7.5-1 | W14 con COMP `test_parents...:58` | `tests/test_domain_tree.py:58` existe y crea el proto | PASS |
| 7.5-2 | Colisión `FileExistsError` sin test | `domain_tree.py:214-218` | PASS |
| 7.5-3 | X03: ni CLI ni `create_protoatom` aceptan `provenance` | `domain_tree.py:129`; `models/protoatom.py:48` | PASS |
| 7.6 | Productor/prueba antes de WS25.2 | Normativa | PASS |

## §8 Ack y respuesta local

| # | Afirmación | Evidencia real | Veredicto |
|---|---|---|---|
| 8.1-1 | `message list/read` R06 COMP | `tests/test_message_cli.py:97,146,221` | PASS |
| 8.1-2 | Ack W13 COMP: cierra, registra `acknowledged_by/at`, reescribe, retrackea, restaura si falla, se niega a repetir | `message.py:161-196`; tests 97,172,199,248 | PASS |
| 8.1-3 | Ack no borra la nota | `message.py:181-186` reescribe, no `unlink` | PASS |
| 8.1-4 | `message send` crea nota nueva en desk destino, puede ser otro desk | `message.py:97-144`; test 154 | PASS |
| 8.2-1 | No hay respuesta local; `InboxNoteDoc` sin hilo; `sender_project` de identidad | `models/inbox.py:37-61`; grep `reply/in_reply_to/thread` en `deskops/**/*.py`: sin coincidencias | PASS |
| 8.2-2 | No se considera respuesta por parecerse | Normativa | PASS |
| 8.2-3 | WS25.1 declara respuesta local no disponible | `dag.yaml:1668-1672` | PASS |
| 8.3-1 | Adaptador graph_ui ausente | Grep de `inbox`/`message` en rutas GU: sin endpoint | PASS |
| 8.3-2 | T-P03.1 F1 sin mecanismo (HO-03) | §5.3 | PASS |
| 8.3-3 | Sin `G_UI_WRITE`/`G_HUMAN_READ` | `dag.yaml` WS25.1 pending; no hay actas | PASS |
| 8.3-4 | Verificación tras recargar posible con R06 | `message read`; test 97 | PASS |
| 8.3-5 | Atribución = identidad del desk, no persona (HO-10) | `message.py:178,193` | PASS |
| 8.3-6 | Errores visibles: `ValueError` ya acusada; `UsageError` ambigüedad; tracking restaura y sale 1 | `message.py:173,186`; `test_message_cli.py:248` (exit 2), `:199` | PASS |
| 8.3-7 | Solo guarda de estado; sin `expected`; acks concurrentes no detectados salvo `closed` | `message.py:172-186` | PASS |
| 8.3-8 | `message send` desde UI debe validar mismo desk; UF08 read-only, WS25.1 sin envío interdesk | `dag.yaml:1662-1664`, `navegacion.md:296` | PASS |

## §9 Git, cierre, fallos, permisos, closeout

| # | Afirmación | Evidencia real | Veredicto |
|---|---|---|---|
| 9.1-1 | Grep de git en deskops: solo `closure.py` y `closeout_gates.py`; sin `push/tag/stash/checkout/reset` como argv | Grep propio | PASS |
| 9.1-2 | Solo `closure.py` escribe Git; W19–W20 y legacy `close_auto` | `closure.py:458,493,627,632`; grep | PASS |
| 9.1-3 | En sldb, git de lectura en rutas abiertas; argv de historia no abiertos uno a uno | `document_history.py:57-63`; `text_history.py:49-55`; `gitignore_policy.py:34-38`; `stores_build_check.py:87`; el contrato lo declara | PASS |
| 9.1-4 | graph_ui usa `git check-ignore` | `workspace_routes.py:468` | PASS |
| 9.2-1 | Salvo W19/W20, ninguna escritura de 2.3–2.5 hace stage/commit | Grep de git en deskops | PASS |
| 9.2-2 | `closeout commit` hace `git add -A -- .sldb` si hay cambios | `closure.py:446-448` | PASS |
| 9.3-1 | Solo `closeout commit|supersede|retire` cierra; `advance` rechaza terminal y apunta al cierre | `tasks.py:178-219`; `test_inbox_promote_cli_gaps.py:184` | PASS |
| 9.3-2 | `closeout commit` corre `verify` antes y no commitea si falla | `closure.py:391-395,540-559` | PASS |
| 9.3-3 | Cierre borra el TaskDoc; tarea cerrada no queda pendiente | `closure.py:458-470`; `operations.py:301-311` | PASS |
| 9.3-4 | Promoción drawer→activa no existe; solo `add task --from-drawer` | `test_inbox_promote_cli_gaps.py:92`; `dag.yaml` | PASS |
| 9.3-5 | No hay operación que compruebe commits previos; handoff/no disponible | Grep git en `operations.py`, `tasks.py`, `drawer.py`: sin coincidencias | PASS |
| 9.3-6 | Refresco por `show task` y `git log -1 --grep 'Task-Id: <id>'` | `closure.py:46-58` | PASS |
| 9.4-1 | `add task` revierte archivo/tracking/Board | `test_operational.py:34,78` | PASS |
| 9.4-2 | `edit/bind` restaura bytes/store | `test_doc_io.py:104,124,150,167` | PASS |
| 9.4-3 | `atoms split/merge` restaura fuentes/destinos/store | `test_atoms_transactions.py:59,98` | PASS |
| 9.4-4 | `message ack` restaura bytes y store coherente | `test_message_cli.py:199-219` | PASS |
| 9.4-5 | `message send` avisa y no revierte | `message.py:129-135` | PASS |
| 9.4-6 | `promote` COMP «DocTransaction: restaura» con tests `:120,153` | `test_inbox_promote_cli_gaps.py:120-139` prueba untrack; `:153-160` prueba éxito sin store; ninguno fuerza fallo ni restauración | **FAIL** |
| 9.4-7 | `atoms type`: stub después del tipado y fuera de transacción | `domain_tree.py:142-165` | PASS |
| 9.4-8 | `closeout commit`: restaura índice/Board/TaskDoc (501-507); `run.yaml` antes del gate y sin restaurar (320); `git add` con `check=False`; COMP parcial test 462 | `closure.py:320,391-395,446-448,501-507`; `test_lifecycle_end_to_end.py:462` | PASS |
| 9.4-9 | `sldb /save` prevalidación; fallo parcial 500 con `completed`, no revierte | `save_routes.py:80-96`; `test_serve.py:247,262` | PASS |
| 9.4-10 | `save_document_payload` archivo antes de índice | `payload_save.py:47-48` | PASS |
| 9.4-11 | graph_ui local prevalidación; fallo a mitad 500; vista no se escribe | `test_mindmap_persistence.py:45-52`; `persistence.py` | PASS |
| 9.4-12 | `/api/desk/advance` usa `_write_doc`; 409 probado | `deskops_routes.py:113-121`; `test_mindmap_deskops.py:77,94` | PASS |
| 9.5-1 | Sin RBAC; `mutates` solo redirige al sandbox | `main.py:155-182` | PASS |
| 9.5-2 | Token Bearer opcional, apagado por defecto; `hmac.compare_digest`; OPTIONS exento; CORS opcional; tests | `SL/cli/serve/auth.py`; `http_server.py:42`; `test_serve_auth.py:54,66,79` | PASS |
| 9.5-3 | `/api/desk/advance`: «Origin igual al Host», cuerpo ≤8192, JSON, solo `{id,revision}` | `deskops_routes.py:96-112`: el rechazo es `if origin is not None and origin != …`; sin `Origin` pasa | **FAIL** |
| 9.5-4 | `/api/save` local y `/api/views/*`: «Origin», cuerpo ≤5 MB | `serve.py:382-384,431-435`: misma condición; sin `Origin` pasa | **FAIL** |
| 9.5-5 | `/api/save` y `/api/models/*` remotos sin guarda de `Origin` | `serve.py:387-418`: no hay comprobación | PASS |
| 9.5-6 | `/api/views/*`: `store` lo elige el cliente | `views_routes.py:29-33` | PASS |
| 9.5-7 | `/docs/create`: `path` del cliente sin contención | `docs_routes.py:105-112` | PASS |
| 9.5-8 | La whitelist es la capa de permisos; filas sin guarda son HO-15 | Normativa | PASS |
| 9.6-1 | `closeout verify`: JSON en stdout, resumen/alertas en stderr, exit 1 si `ok` falso | `closeout.py:64-73` | PASS |
| 9.6-2 | `commit/supersede/retire` no están en HTTP; no hay commit/cierre desde el servidor UI | Grep de `closeout` en GU y `commit` en `SL/cli/serve`: sin rutas | PASS |
| 9.6-3 | Handoff de cierre y «ningún endpoint ejecuta closeout commit» | Normativa; no hay ruta | PASS |
| 9.6-4 | `G_CLOSEOUT` satisfied para evidencia declarada; vocabulario cerrado | `dag.yaml:33-43`; `closeout_gates.py:23` | PASS |
| 9.7-1 | Resolución de `tests/commit/atom/document/external` | `closeout_gates.py:156-205`; `operations.py:668-675` | PASS |
| 9.7-2 | Tipo desconocido → `unknown_closeout_evidence`; sin campo → alerta + `implicit_code: true` | `operations.py:615,625,716` | PASS |
| 9.7-3 | «Sin JSON» = no verificable; «JSON con `ok:false`» = fallida; `ok:true` sin findings = verificada | `closeout.py:64-73`; `verify_task_closeout` | PASS |
| 9.8-1 | No hay operación pública de diff por tarea (HO-13) | Grep de comandos; sin ruta ni método | PASS |
| 9.8-2 | Verbos git permitidos/prohibidos y precedentes | Normativa; `closeout_gates.py:208-221`; `workspace_routes.py:468` | PASS |

## Comprobaciones solicitadas

| Pregunta | Resultado | Evidencia |
|---|---|---|
| ¿La ausencia de señal declara exclusividad? | No | §5.4 trata error/lista vacía como falta de evidencia; F2a en `serve.py:172-193` |
| ¿El lock de UI se presenta como coordinación? | No; se niega expresamente | §5.6 |
| ¿Se confunden `expected`, token y capacidad compartida? | No en §6.1; sí hay una exageración en §6.3 («única») | 6.1-A/B/C vs. `PR/kernel/kernel.py:49-63` |
| ¿Ningún escritor consume `version`? | Cierto en sldb y rutas abiertas | Grep sin `version` en `save_*`; `document_serialization.py:32` solo publica |
| ¿Comparación de captura exacta opción por opción? | No del todo: B asume drawer pero acepta `path` del cliente | `docs_routes.py:105-112`; `operations.py:301-311` |
| ¿`message send` + `promote` sin aprobar? | Sí | `dag.yaml:758-760`; §7.3-D |
| ¿El ack pasa a disponible por comando parecido? | No; §8.3 separa existencia de disponibilidad | `message.py:161-196`; §8.3 |
| ¿Closeout fuera del servidor UI? | Sí; solo `verify` como lectura | Sin rutas de closeout en GU/SL; `closeout.py:64-73` |

## FAIL y corrección implicada

1. **§5.1, cita `dag.yaml:1306`** — la frase de WS19.1 está en `:1329`. Corregir la línea.
2. **§5.6, «único lock de archivo entre procesos»** — existe también `journal_lock` (`SL/store/journal/lock.py:14-27`; usado en `append.py:27`). Corregir: «hay dos locks de archivo en sldb, índices y journal; ninguno cubre la escritura del documento».
3. **§6.3, «la única precondición que existe en un escritor público» y fila «pron say/eval/MCP: no tienen precondición»** — `PR/kernel/kernel.py:49-63` define `expect/_guard` por `hash_c`, usado por `change/add/remove/clean/forget` (`kernel/actions/*_verb.py:31,37`; `sexpr/execution/action_executor.py:75`). Corregir el alcance: «la única precondición de payload por valor en las rutas HTTP/API de la UI; pron tiene su guard propio por `hash_c`, no compartido».
4. **§6.4, «escriben sin precondición (W02–W06, W13, W19–W21, S07)»** — W05 rechaza `complete` (`tasks.py:178-180`), W06 tiene PE de idempotencia, W13 PE `closed`, W19 ejecuta `verify`, W20/W21 exigen estado/refs. Corregir a «sin precondición por valor `expected`/CAS; con guardas de estado o gate».
5. **§7.1, cita `dag.yaml:723`** — el criterio «falta conducta de workflow… preservar origen…» está en `dag.yaml:777-778`. Corregir la línea.
6. **§7.3-B, «No crea tarea activa: Ídem A»** — `path` es del cliente (`docs_routes.py:105-112`); un `path` bajo `desk/tasks/task-*.md` hace que `list_tasks` lo enumere (`operations.py:301-311`). Corregir: «solo si el adaptador fija el `path` bajo `desk/drawer/tasks/`; sin fijarlo, puede crear una tarea listada».
7. **§9.4, fila `promote` COMP «DocTransaction: restaura»** — `test_inbox_promote_cli_gaps.py:120` prueba untrack y `:153` éxito sin store; ninguno fuerza fallo ni restauración. Corregir a LEC o citar una prueba real de rollback (no existe en lo abierto).
8. **§9.5, filas de `Origin` en `/api/desk/advance`, `/api/save` local y `/api/views/*`** — la guarda solo actúa si el header `Origin` está presente (`deskops_routes.py:96-98`; `serve.py:382-384,431-435`). Corregir: «si llega `Origin`, debe coincidir con `Host`; su ausencia no se rechaza».

## No pude verificar

- El contrato declara `HEAD deskops 826ca4a0`; el supervisor mide `92ed7ed6`. Leí el árbol actual, no el commit declarado; no sé si el código cambió entre ambos.
- No ejecuté ningún test ni comando: no hay prueba de runtime, solo cuerpos de tests leídos.
- No abrí `infraestructura.md:51` (frescura de la carga de `sldb serve`).
- No abrí los artefactos del recibo `G_CLOSEOUT`; solo `dag.yaml:33-43`.
- No abrí uno por uno los argv de historia de git en sldb; el propio contrato lo declara.
- No abrí `spec2viz` ni `navegacion.md` completa (solo los tramos citados).
- No verifiqué hashes de commit por mí mismo; uso los datos del supervisor.

RESULTADO: FAIL
