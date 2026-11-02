# Resumen del Executor de WS12

Fecha: 2026-11-01. Entregable: `desk/drawer/plans/workspace-documental/contratos/operaciones.md` (729 líneas según `wc -l` al cierre, 13 secciones en el orden de la TaskDoc). Este resumen es el único otro archivo escrito. Sin commits, sin revisiones, sin tests, sin CLI de escritura.

## Qué se hizo y qué no se ejecutó

Todo es lectura. Se usó `sed`/`grep`/`cat`, `git` de solo lectura (`rev-parse`, `status`, `diff --stat`, `ls-files`, `check-ignore`, `log`), y dos scripts de Python de solo lectura: uno importó `deskops.cli.registry` (con `PYTHONDONTWRITEBYTECODE=1`) para listar las 113 entradas de `command_registry()` con su bandera `mutates`; la primera importación se hizo sin esa variable, por lo que pudo regenerar archivos `.pyc` bajo `deskops/**/__pycache__` (ignorados por git; no se construyó `DeskopsOperations`, así que no se tocó `.deskops.log`); otro cargó `dag.yaml` con `yaml` para calcular qué tarea `requires` qué gate. **No se ejecutó** ningún test, ninguna orden de deskops o sldb que escriba, ni `build_plan.py`, `validate_plan.py`, `context_review.py` ni `deskops atoms validate`. Todas las pruebas citadas se leyeron, no se corrieron. El contrato lo dice así en 1.4.

## Resolución por sección (líneas en `operaciones.md`)

| Sección | Línea | Resolución |
|---|---|---|
| 1. Alcance y estado | 5 | Qué fija y qué no; commits observados (deskops `826ca4a0`, sldb `77bd6d00`, graph_ui `134a665`, spec2viz `10df4f0`, pron `e1e9df0c`) y contraste con WS02–04/WS11; convenciones COMP/LEC/NOAC/HUE, ALOG, ASC, MIG; gates |
| 2. Matriz | 54 | 65 filas: lecturas (R), diagnósticos por efectos (D), mutaciones de deskops (W), sldb (S), graph_ui (U) y operaciones faltantes (X); cobertura de las 96 hojas del registry (2.7, línea 157) |
| 3. Campos protegidos | 193 | Método derivado de modelos, lifecycle y operaciones con dueño; tabla por modelo y operación; obligación del adaptador (3.2) |
| 4. Adaptador | 250 | Canal público por operación o hueco; regla de capa lista (4.3, línea 285) |
| 5. Coordinador y modo manual exclusivo | 295 | Definición operativa, formas de comprobarla, respuesta ante falta de evidencia, sin mecanismo nuevo |
| 6. Precondición de escritura | 347 | Tres cosas distintas (6.1), representación elegida (6.3), qué verifica WS45 (6.5), fuente en bruto (6.6) |
| 7. Captura | 400 | Comparación de cinco opciones; ninguna cumple con prueba real; protoátomo con su canal y su hueco de origen |
| 8. Ack y respuesta local | 434 | Ack existe pero no está disponible para la UI (tabla de condiciones); respuesta local es hueco |
| 9. Git, cierre, fallos parciales, permisos | 462 | Git, guardar, cierre/promoción, fallos parciales por operación, permisos, canales de closeout fuera del servidor UI, correspondencia de evidencia para WS27.2, lectura Git para WS27.1 |
| 10. Recepción por delta | 544 | Reglas y tabla de los 26 IDs de `G_WRITE_CONTRACT`, con repo, receptor, efecto, cobertura, recibo y gates |
| 11. Ramal E | 590 | Una sección por delta (WS34.1, WS34.2) con política, clasificación, actor y momento; sin valor numérico |
| 12. Huecos | 621 | 20 filas (HO-01 a HO-19 y HO-11b) con clase, dueño y productor |
| 13. Trazabilidad | 650 | 25 frases de la aceptación, T-P03.1, `promotion-notes.md`, remisiones de `navegacion.md` |

## Cada frase de la aceptación de WS12 y dónde quedó

Detalle completo con sección en `operaciones.md` 13.1 (línea 652). Resumen: (1) G_WRITE_POLICY registrado: 1.2 y 1.5. (2) Whitelist por operación, campo, canal, actor, revisión, Git y efectos: secciones 2 y 3. (3)–(7) Recibo por delta, receptor P01, campos e intake que no esperan Changes, modelos, Scion ni raw-source, evaluación por ID y G_CLOSEOUT: 9.6 y sección 10. (8) Raw-source con WS20/G_SOURCE y G_SLDB_WRITE: 6.6, 10.2. (9)–(12) Representación de la precondición, tres conceptos, sin CAS por reflejo, productor WS45: 6.1 a 6.5. (13)–(16) Captura a drawer y protoátomo, `message send` + `promote` no aprobado, productor Deskops explícito: sección 7. (17) Lock de UI y otro coordinador: 5.5 y 5.6. (18) Solo contrato y enlaces: 1.2. (19)–(20) Contraste y matriz con huecos asignados: 1.3, 2, 12. (21)–(24) Requisito de API faltante solo para el productor, elección justificada de la representación, receptor P01 en deltas de deskops, definición del hueco de workflow: 10.2, 6.3, 10.1, 7.1. (25) Ramal E: sección 11.

## Conteos y decisiones del contrato

Matriz (65 filas): COMP 38, LEC 13, NOAC 6, HUE 8 (tras la corrección de abajo; antes 39/12/6/8). Ninguna fila está aceptada por acta. Los conteos se recalcularon con un script de lectura sobre la propia tabla.

Representación de la precondición: **before-image por valor (`expected`, 409)** para toda escritura de payload por campos desde la UI, por `changes[]` de `POST /save`. Motivo: es la única precondición que existe en un escritor público con rechazo sin cambios, 409 observable y pruebas en dos repos (`SL:tests/test_serve.py::test_batch_save_stale_expected_conflict:213`; `GU:tests/test_mindmap_persistence.py::test_conflict_and_untrack_preserves_file:54`). El token `version` se publica pero ningún escritor lo consume (la docstring de `document_serialization.py:25-28` promete lo contrario). No hay precondición compartida entre escritores. Para raw-source (6.6) se fijan requisitos observables sobre el texto íntegro, sin mecanismo.

## Decisiones de producto no cubiertas

**Ninguna de producto.** El contrato no improvisa ninguna. Quedan **tres puntos técnicos que root debe asignar o decidir**, expuestos como huecos y no resueltos:

1. **HO-05, baja de un RelationDoc**: `sldb /save` borra el archivo y graph_ui local solo destrackea (tests citados). WS19.2 depende de cuál se adopta. Es una pérdida de datos potencial, por eso no lo resolví.
2. **HO-07, canal de edición de campos para documentos con contenido no declarado**: `/save` tiene precondición pero no rechaza borrar contenido que el modelo no declara; `deskops edit` lo rechaza pero no tiene precondición. Ningún canal reúne ambas. Si root exige ambas para WS19.1, falta un productor (sldb o deskops).
3. **HO-11, captura directa a drawer**: ninguna opción tiene prueba real; el DAG prevé un productor Deskops explícito antes de WS25.2 y no existe ese nodo. El valor por defecto que fijé es «no disponible» (7.4).

Dos propuestas del contrato que root puede reemplazar: la representación del origen de una captura (7.2: reutiliza la gramática `ruta[::localizador]` en `provenance`/`references`, con el tipo derivado de la ubicación) y la regla de capa lista (4.3).

## Huecos sin productor en el DAG (con dueño)

HO-03 (mecanismo de afirmación y evidencia del modo manual exclusivo; graph_ui y deskops), HO-04 (precondición compartida; sldb), HO-05 (baja de RelationDoc; sldb y graph_ui), HO-06 (escritores sin precondición, forma legacy de `/save`; sldb), HO-07 (guarda de contenido no declarado; sldb o deskops), HO-09 (respuesta local; deskops), HO-10 (atribución del actor humano; salvo la decisión humana de WS33.2), HO-11 (captura a drawer; deskops), HO-11b (origen en protoátomo; deskops), HO-12 (enrutar un TaskDoc existente con precondición; deskops), HO-15 (guardas de `Origin` y contención de `path`/`store`; graph_ui y sldb), HO-18 (operación de decisión humana; deskops). HO-19 (valor del timeout) no es un nodo: lo fija una corrección documental de este contrato al preparar WS34.1 y WS34.2. HO-17 depende de WS05, que no existe.

## Qué leí

Completos, en el orden pedido: la TaskDoc de WS12; `preflight-disposition.md`; `review-source.md` desde «Tras ese cierre queda autorizada SOLO WS12» hasta el final; el nodo WS12 de `dag.yaml` y los gates G_WRITE_CONTRACT, G_UI_WRITE, G_SLDB_WRITE, G_CLOSEOUT, G_SOURCE, G_PAYLOAD_PRECONDITION (más G_WRITE_POLICY, G_SCION, G_EXEC, G_HUMAN_READ); `navegacion.md` (secciones 0, 1, 3, 11, 12, 13 en texto; las demás por búsqueda) y `navegacion-aprobacion.md`; `decisiones.md` y `root-decision-20261101.md`; `promotion-notes.md`; los nodos WS19, WS19.1, WS19.2, WS20, WS21, WS25, WS25.1, WS25.2, WS26, WS26.1, WS26.2, WS27, WS27.1, WS27.2, WS28, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2, WS34, WS34.1, WS34.2, WS36, WS39, WS42, WS43, WS44, WS45 (alcance y aceptación).

Código abierto: de deskops, `operations.py` entero, `cli/registry.py` (por script y por tramos), `cli/main.py` (tramo del sandbox), `cli/model_introspection.py`, `cli/commands/{operations,closeout,message,promote,drawer,issue,retire,atoms,core,doctor,graph,drift,materialize}.py`, `runtime.py` (parcial), `services/{tasks,closure,closeout_gates (parcial),drawer,issues (parcial),atoms (encabezados y tramos)}.py`, `lifecycle.py`, `doc_io.py`, `domain_tree.py`, `models/*.py` (campos), `desk/lifecycle/*.md`, `task_lifecycle.yaml`, `runtime/{supervise,scion}.py` (tramos). De sldb: `cli/serve/{save_routes,save_plan,save_single,docs_routes,docs_create_route,routes,auth,fields_routes,document_routes}.py`, `api/documents/{payload_save,payload_save_steps,create_document,document_serialization}.py`, `api/stores/{open_store,store_check,scan_cache}.py`, `api/edges/edge_reading.py`, `api/actor.py`, `store/{ops,migration}.py`, `store/io/lock.py`, `cli/commands/{serve,store_check,store_check_apply,fields_save}.py` y los tests de `test_serve.py` y `test_serve_auth.py` por nombre y por tramos. De graph_ui: `deskops_routes.py`, `persistence.py`, `sldb_adapter.py`, `views_routes.py`, `serve.py` (tramos de lectura, escritura y workers) y los tests `test_mindmap_deskops.py`, `test_mindmap_persistence.py`, `test_mindmap_endpoints.py` (nombres y tramos). De pron: `kernel.py` (guarda) y `payload_editor.py`. Auditorías: `deskops.md` (encabezado, universo y resumen; la tabla A1 no se leyó fila por fila, el código sí), `infraestructura.md` (secciones 2 y 4 por grep), `ui.md` (filas de WS19 a WS42), `user-flows.md` y `vistas.md` (por grep de lo que toca escritura).

## Qué no leí

- `auditoria/deskops.md` tabla A1 fila por fila, y los cuerpos de `infraestructura.md` fuera de las secciones de conflictos y escritura.
- Los cuerpos de `drift_check_knowledge_surfaces`, `faq`, `repo whoami`, `runtime status/attach`, `desk replace/update`, `repo register/remove`, `bootstrap`, `graph build/reflect`, `materialize`, `atoms reorganize` (filas LEC), y los tests `test_desk_replace.py`, `test_desk_sync.py`, `test_repo_identity.py`, `test_atom_folder_axis.py`, `test_doctor_model_registration.py`.
- spec2viz: no se abrió.
- El diálogo y los componentes de UI de graph_ui; `frontends/workspace/` (excluido por instrucción).
- Los argv de historia de git en sldb (`document_history.py`, `text_history.py`).

## Qué no pude verificar

- **Runtime de cualquier cosa.** Nada se ejecutó: ni la frescura de la carga de `expected` ante una edición externa, ni que `open_store` migre en una lectura concreta, ni el andamiaje de `atoms validate`, ni los efectos de `doctor` sobre la caché de escaneos del usuario. Son lectura estática y así están rotulados.
- Si un desk con `.deskops.log` versionado (sldb, spec2viz) se ensucia por una lectura: solo `git ls-files` y el `git status` de sldb lo hacen consistente, sin atribuir el cambio a una orden.
- Qué ocurre si un candidato de drawer creado por `create_document` queda rastreado y luego `add task` crea una tarea con el mismo id (colisión en el store): no se abrió.
- La API real de Scion (no hay `auditoria/scion.md` ni `scion-probe.md`; WS05 y WS44 no existen): la sección 11 no puede apoyarse en ella.
- El canal de validación de materializaciones que WS42 usará («API pública SLDB»): no se abrió; queda para su TaskDoc.
- Que las 20 filas de huecos tengan productor aceptado: solo se comprobó que los IDs existen en `dag.yaml`.
- El árbol de deskops estaba sucio al despacho (dos notas de inbox modificadas, dos archivos sin seguir ajenos); no se tocó. Una nota de inbox sin seguir (`20261029-213633-unclear-advance-to-superseded-no-cambia-status.md`) trata de `advance`, y no se leyó.

## Revisión del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01, sin Executor. Leí §1 y §5 a §7 completos y la estructura del resto. **No leí completas las secciones 2 a 4 ni 8 a 13**: las cubren los tres Testers. Comprobé por grep y lectura: `expected` solo en `save_plan.py:50,58` entre escritores de sldb; `doc_version` sin consumo en guardado; `/api/workers` con `workers: []` y `error`; guarda de `Origin` local en `serve.py:431`; `.deskops.log` versionado en sldb y spec2viz. No edité el contrato.


## Corrección tras Testers

Contrato congelado en `92ed7ed6`. Cada hallazgo se verificó abriendo la fuente antes de decidir. Los números de línea son de `operaciones.md` tras la corrección salvo que se indique.

| # | Hallazgo (Tester) | Veredicto | Evidencia abierta | Cambio |
|---|---|---|---|---|
| 1 | 1.3: commit `826ca4a0` distinto del HEAD `92ed7ed6` (A, C) | Falso | `92ed7ed6` es el commit del propio contrato, posterior al despacho; `preflight-disposition.md` fija el HEAD de despacho | Nota en 1.3 que lo aclara |
| 2 | 1.5: `G_SOURCE` sí está en `requires` (A) | Real | `dag.yaml:1462-1472` (variante editable de WS21) | 1.5 corregido |
| 3 | R02: `ARTIFACT_MODELS` tiene 10 entradas, líneas 61-72 (A) | Real | `operations.py:61-72` | R02 corregido |
| 4 | `from_drawer`: la guarda está en `drawer.py:155-163` (A) | Real | `drawer.py:150-165` | Cita corregida |
| 5 | X01: el grep de `reply` no da «prosa en scion.py» (A) | Real | `grep -rn "reply\|in_reply_to\|thread" deskops --include=*.py`: sin salida | Frase eliminada |
| 6 | «Ningún estado editable por payload» presentado como propiedad (A) | Real | `operations.py:277-278`, `tasks.py:184-187`, `specs/compiler.py:40`, `payload_save.py:16` | 3.1 dice que hoy el código sí lo permite y que es una regla para la UI |
| 7 | 5.1: cita `dag.yaml:1306` (B) | Real | `dag.yaml:1327-1329` | Cita corregida |
| 8 | 5.6: hay un segundo lock entre procesos, el del journal (B) | Real | `sldb/store/journal/lock.py:14-27`, `append.py:27` | 5.6 corregido |
| 9 | 6.3: «única precondición» y pron sin precondición (B) | Real | `pron/kernel/kernel.py:49-63`, `kernel/actions/*_verb.py` (`_guard`), `sexpr/execution/action_executor.py:75` | Acotada a «por valor en los escritores que la UI alcanza»; fila de pron separada. **La representación elegida no cambia**: la UI no pasa por el kernel de pron, su token es interno de la jugada y no se publica; sí indica que un token `hash_c` es viable (se anota para HO-04) |
| 10 | 6.4: lista de «sin precondición» incluye órdenes con guarda de estado o gate (B) | Real | `tasks.py:179-191`, `operations.py:284-300`, `message.py:172-173`, `closure.py:540` | 6.4 distingue «sin `expected` ni CAS» de las guardas de estado y de gate |
| 11 | 7.1: cita `dag.yaml:723` (B) | Real | `dag.yaml:777-778` | Cita corregida |
| 12 | 7.3 B: «no crea tarea activa: Ídem A» (B) | Real | `docs_routes.py:105-112`, `operations.py:list_tasks` | Condicionado a que el adaptador fije el `path` |
| 13 | 9.4: `promote` COMP sin prueba de restauración (B) | Real | `test_inbox_promote_cli_gaps.py:120-139,153-160` no fuerzan fallo | Baja a LEC en 9.4 (la fila W11 ya era NOAC) |
| 14 | 9.5: `Origin` solo actúa si el header llega (B) | Real | `deskops_routes.py:96-98`, `serve.py:382-384,431-435` | 9.5 corregido y declarado como hallazgo de seguridad en HO-15 |
| 15 | 10.1/WS43: prueba «de tests/» (C) | Real | `dag.yaml:2815-2822` | WS43 exceptuado: acta y commit de cierre |
| 16 | 10.2/WS20: `G_SOURCE` como consumido (C) | Real | `dag.yaml:44-49`, `1390-1397` | Pasa a «produce» |
| 17 | HO-19: formato de productor (C) | Real | No existe nodo | «sin productor en el DAG» más la nota |
| 18 | 13.1: falta la frase `dag.yaml:769` (C) | Real | `dag.yaml:769` | Fila 21b |
| 19 | 13.2: «cada delta cita 5.7» (C) | Real | 10.2 solo cita 5.7 en WS19.1 | Regla en 10.1 y texto de 13.2 corregidos |
| 20 | 13.3: `stores check`, WS33.2/WS32.x, WS39 no constan en `promotion-notes.md` (C) | Real | `grep "stores check"` en `promotion-notes.md`: sin salida; la fuente es `preflight-disposition.md` y `20261101-ws09-correccion/preflight-input.md:60`; los otros dos vienen de `dag.yaml` | Las tres filas reatribuidas |
| 21 | 13.4: §3.2 generalizado (C) | Real | `navegacion.md:93` | Texto exacto de §3.2 y aviso de MIG |
| 22 | Mi barrido: D02 COMP sin test de la rama de andamiaje | Real | `test_cli.py:245-272`, `test_doctor_model_registration.py:130` | D02 pasa a LEC |
| 23 | Mi barrido: «único timeout de graph_ui» | Real | `serve.py:100,111,124,175`, `workspace_routes.py:471` | Reescrito |
| 24 | Mi barrido: segundo ack y fallo a mitad de U01 sin test | Real (rótulo) | no hay test de segundo ack ni de fallo a mitad | Marcados [L] en W13 y U01; el estado de la fila no cambia |

Reales: 23. Falsos: 1 (el commit). Filas de la matriz que cambiaron de estado: D02 (COMP a LEC). Conteos nuevos de 2.7: COMP 38, LEC 13, NOAC 6, HUE 8 (65 filas). La representación elegida no cambió. No se ejecutó nada; solo lectura y edición de estos dos archivos.

## Revisión del Supervisor de la corrección

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Evidencia de los Testers v1 en `renovacion-1/`. Leí el informe del Executor y una parte del diff. El cotejo de la corrección lo hacen los Testers v2.

## Ajuste del Supervisor tras Testers v2

Claude Opus 5.5, pane `w3Y:p1`, sin Executor. Evidencia v2 en `renovacion-2/`: B PASS; A y C FAIL. Reales y corregidos: §4.1 «único timeout», que el Executor dijo corregir y seguía; U02, evidencia de la búsqueda; §10.1, regla de prueba generalizada; gates de seis agregados, contra `requires` de `dag.yaml`; §13.4, efectos «rotulados» pese a R09, R10 y D04.
