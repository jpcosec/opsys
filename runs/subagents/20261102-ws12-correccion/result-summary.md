# Resultado del Executor: corrección de WS12 tras la revisión root

2026-11-02. Español. Rutas relativas a `/home/jp/proyectos/SLDB_1/deskops`. Autoridad: `runs/subagents/20261102-ws12-correccion/review-source.md` (las decisiones A a E son técnicas de root por delegación, no del usuario ni una aprobación humana).

Escribí solo tres rutas: `desk/drawer/plans/workspace-documental/contratos/operaciones.md` (OP en adelante), `desk/drawer/plans/workspace-documental/dag.yaml` y este archivo. Sin commits, sin build, sin tests, sin CLI que escriba, sin `deskops message`. Todo lo que afirmo sale de lectura estática: no reproduje nada en runtime ni ejecuté ninguna prueba citada. `context_review.py status` (solo lectura) lo corrí tres veces sobre copias en `/tmp` y sobre el árbol real, y no escribe.

## 1. Matriz hallazgo → cambio → productor → consumidor

Las líneas son las de OP tras el parche (778 líneas). Las citas `dag.yaml:N` previas que OP conserva son de la revisión 9 (OP lo declara en 13.5).

| # | Hallazgo o decisión | Cambio en OP (sección: línea) | Productor | Consumidor |
|---|---|---|---|---|
| 1 | §5.7 exigía 409 a canales sin `expected` | 5.7 reescrita por canal: 409 solo en S02/S03/U01 y `revision` de U03 (`:342-354`, ii-a / ii-b); 5.4 fila «otro coordinador» (`:330`); 8.3 fila precondición del ack (`:498`); 5.2 «se admite», no «se prueba» (`:307`) | Ninguno para el 409: no se introduce CAS universal (6.4). La admisión fiable de los canales sin precondición la produce WS48 (ver C) | WS19.1, WS19.2 (con 409); WS25.1, WS26.x, WS28 (sin 409, rechazo o handoff) |
| 2 | S01/S02/§9.4 sobreafirmaban que `/save` prevalida todo el lote | S01 (`:126`): `update_target` devuelve `payload_error` en la posición del `path` y `None` en la del error (`save_plan.py:54`), `prepare_step` solo rechaza un error en segunda posición, `apply_change(update)` no usa `path`, `apply_batch` es secuencial y parcial; los tests de payload inválido (`:247`) cubren `create`. S02 (`:127`). 6.2 (`:386`). 9.4 fila `/save` (`:530`). U01 (`:140`) y fila 9.4 U01 (`:532`): graph_ui local sí valida `update` (`persistence.py:103-115`) | Ninguno. «Gap de sldb capturado»: el aviso al inbox de sldb lo envía el Supervisor; OP lo cita sin workaround | WS19.1, WS19.2 y cualquier lote de `/save`; WS45 (sin cambio de alcance) |
| 3 | W01 y §4.2 confundían CLI `add task` con `create_task_bundle` | W01 (`:95`): CLI `require=True` (`operations.py:26`), API `require=False` (`tasks.py:86`), alerta `closeout_evidence_not_declared`; 3.3 `closeout_evidence` (`:222`); lista blanca (`:250`); 4.2 «Autorar tarea» (`:270`) | No aplica: es una diferencia de garantía por canal; no falta ninguna capacidad | WS26.1 (si usa la API comprueba él mismo que la evidencia llega no vacía) |
| 4 | S05 agrupaba `/docs` con `/docs/create` | S05 (`:130`): `/docs` solo `_KEYS = model/name/payload`, sin `path`; `/docs/create` sí admite `path`; respuestas y tests por ruta (`test_serve_edges_docs.py:63,77` para `/docs`); 9.5 fila `/docs/create` y párrafo (`:541-552`); 7.3 opción B (`:449`); HO-15 (`:690`) | Ninguno: la política de rutas es del adaptador de cada delta (E) | WS46 (fija el `path` de la captura), WS25.2 |
| 5 | §4.3.1: ausencia del archivo no demuestra cierre | 4.3 punto 1 (`:291`): cierre = commit con `Task-Id` y modo real (`Run-Dir` o `Closeout-Mode: manual`); `record`, `superseded` y `legacy-resolved` no cuentan; búsqueda declarada de la consulta pública (no existe); punto 4 (`:294`); 9.3 (`:514,516`) | **Gap del consumidor**: no hay consulta pública de deskops (búsqueda de `Task-Id`, `Closeout-Mode`, `--grep`, `trailers:key`, `index.jsonl` en `DK/deskops/**/*.py`: solo `closure.py` escribe y la ayuda CLI); no se inventa un archivo ni un modelo histórico | WS26.2 (lee git con el argv de 9.8 o declara «no comprobada») |
| 6 | W19: `_close` no garantiza `verify` universal | W19 (`:113`): gate solo si `run_gates` y `task_path.exists()` y `_board_routes` (`closure.py:390-394`); W20 (`:114`): `run_gates=False` (`:169,:252`); 1.5 (`:54`); 6.4 (`:416`); 9.3 (`:514`); 9.6 tabla (`:559`) y «Precondiciones del handoff» (`:565`) | Ninguno: no se reabre G_CLOSEOUT ni se cambia código | WS28 (ejecuta y muestra `verify`, comprueba Board y TaskDoc, no ofrece supersede/retire como verificado) |
| 7 | HO-11/11b: WS25.2 no se cumple declarando no disponible | 7.3 resultado (`:454`), 7.4 (`:458`), 7.5 (`:462`), 7.6 (`:464`); X02/X03 (`:151-152`); 3.3 ProtoAtomDoc `provenance`; 4.2 (`:278-279`); 10.2 filas WS25.2 (`:613`) y WS46 (`:632`); HO-11/11b (`:685-686`) | **WS46** (nuevo, deskops) | WS25.2 (depende de WS46) |
| 8 | HO-10 mezclaba tres planos | 10.1 viñeta «Actor son tres cosas distintas» (`:595`); 8.3 fila atribución (`:496`); HO-10 (`:684`); 10.2 WS25.1 (`:612`) y WS33.2 (`:623`) | WS33.2 existente solo para la decisión humana; ninguno otro | WS25.1 (el ack no se bloquea), WS33.2 |
| A | HO-05 baja de RelationDoc ≠ quitar referencia | HO-05 (`:679`): baja = borrar documento e índice (canal S03); backend local actual no equivalente; 4.2 (`:268`); 3.3 RelationDoc (`:232`); 6.3 `delete` (`:399`); 10.2 WS19.2 (`:608`) | **WS19.2** (existente; texto y aceptación ampliados en `dag.yaml`; sin API ni nodo nuevos) | WS19.2 |
| B | HO-07 tres garantías | S02 (`:127`); 6.2 (`:385`); 6.3 tabla (`:405`); 6.5 «Lo que WS45 no cubre» (`:422`); 6.7 (`:428`); HO-07 (`:681`); 10.2 WS47 (`:633`) | **WS47** (nuevo, sldb, nodo atómico) | WS19.1, WS19.2 (WS21 por WS19) |
| C | HO-03 evidencia de modo manual exclusivo | 5.1 (`:299`), 5.2 (`:307`), 5.3 fila F1, 5.4, 5.7, 5.8 y **5.9 nuevo** (`:360`); 10.1 (`:594`); HO-03 (`:677`); 10.2 fila WS48 (`:634`) | **WS48** (nuevo, graph_ui) | WS19.1, WS19.2, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39, WS42 |
| D | HO-11/11b productor de captura | Igual que el hallazgo 7 | WS46: primero probar composición pública; completar solo lo que falte; sin wrapper ni modelo antes de demostrarlo | WS25.2 |
| E | Origin y diferidos | 9.5 (`:537-552`): controles reales por ruta y qué no prueban; U02 (`:141`); HO-15 (`:690`); HO-04 (`:678`) y HO-06 (`:680`) diferidos por la base manual; HO-09 conserva «no disponible» (`:683`); HO-18 contrastado con WS33.2 (`:693`, X05 `:154`) | Ninguno nuevo: política de rutas, raíces y modelos es del adaptador de cada delta; HO-18 lo produce WS33.2 existente | Adaptadores de los deltas; WS33.2 |

Estados de fila: ninguna fila cambió de estado. Los conteos de 2.7 (65 filas: COMP 38, LEC 13, NOAC 6, HUE 8) siguen válidos. S01 y S02 siguen COMP para la capacidad que nombran y los límites van rotulados [L] en la misma fila; no agregué ni renumeré filas ni huecos.

## 2. Justificación de encaje

### Decisión B (WS47 como nodo atómico, no dentro de WS45)

Criterio del Supervisor: leer WS45 y decidir si la guarda cabe sin cambiar su sentido.

- **WS45** (`dag.yaml:2883-2927` en rev. 9): «Verificar o completar la precondición». Reutiliza primero, inventario con ruta, símbolo y commit, pruebas focalizadas de que un estado previo obsoleto se rechaza sin cambios, «código solo si al ejecutar falta capacidad» y «no mezcla UI ni productor condicional». Su gate es `G_PAYLOAD_PRECONDITION` y su evidencia es la igualdad de payload.
- **La guarda de contenido** es otra garantía (OP 6.2): `save_document_payload` no la tiene, a diferencia de `create_document` y `track_document_file` (`create_document.py:60-61`, `track_document_file.py:47-48`). Es ausencia conocida, no condicional: no cabe en «verificar o completar si falta». Cambia código compartido por la CLI de sldb, pron y graph_ui local, y su aceptación es de otra propiedad.
- Meterla en WS45 cambiaría su sentido, su gate y su radio de cambio, y sería ampliarlo en silencio. Por eso: **WS47 atómico** (sldb, estimación S, `G_SLDB_WRITE` + `G_WRITE_CONTRACT`), independiente de WS45 (ambos dependen solo de WS12). No resuelve el gap de prevalidación de `update` del hallazgo 2 (otro) ni hay workaround de Deskops.
- Hasta que WS47 pase, la edición por campos de documentos con contenido no declarado queda no habilitada (WS19.1 y WS19.2 dependen de WS47).
- Residuo declarado: WS26.1, si guarda campos por `/save` `update`, también debería esperar WS47. Lo dejé como obligación de su TaskDoc (OP 6.7), sin arista nueva, para no ampliar invalidación; root puede añadirla.

### Decisión C (WS48, nodo propio de admisión, fuera de WS19.1)

- Se propone **WS48** (graph_ui, M, `G_UI_WRITE` + `G_WRITE_CONTRACT`), `depends_on` WS12. Dueño graph_ui porque la admisión ocurre en el servidor de la UI antes de invocar el canal, y porque `navegacion.md` §3.2 ya fija el patrón «configuración confiable fuera de la petición». Un solo punto de admisión que consultan todas las rutas de escritura.
- Dependen de WS48 los nueve consumidores que 10.1 y HO-03 ya nombraban: WS19.1, WS19.2, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39 y WS42. Así ack (WS25.1) y captura (WS25.2) no dependen de WS19.1 por accidente.
- OP 5.9 describe solo el contrato planificado: entradas (F1 vigente fuera de la petición, evidencia contraria disponible), salidas (admitida, con «declarado, sin evidencia contraria a las <hora>», o lectura/handoff con causa), reglas y límites. No hay servicio de identidad, autenticación ni coordinación, ni lock, ni CAS universal, ni 409 inventado. La ausencia de evidencia contraria no prueba exclusividad. Otro coordinador: lectura o handoff, como fija P03.
- No exigí `G_HUMAN_READ` en WS48 (no es una mutación; sus dependientes lo llevan). Es una decisión a revisar.

### Decisión D (WS46)

- **WS46** (deskops, M, `G_WRITE_CONTRACT`), `depends_on` WS12. WS25.2 pasa a depender de WS46 (y de WS48). La aceptación de WS46 es la «prueba»: se ejecutaría en la promoción, no aquí.
- Primero inventaría y prueba la composición pública (por ejemplo `POST /docs/create` con el `path` fijado bajo `desk/drawer/tasks/`, o DrawerService); solo si no cumple, completa lo que falte; sin wrapper ni modelo nuevo antes de demostrar que hacen falta. Candidato de drawer y protoátomo tienen pruebas separadas de origen, colisión y no-tarea-activa.
- La aceptación de WS25.2 se amplió: no se cumple declarando la captura no disponible. A diferencia del reply de WS25.1, cuya aceptación sí lo permite (HO-09 intacto).
- Una sola unidad (M) porque entrega una capacidad coherente de captura; si al promoverse resulta demasiado grande, dividir por destino es trivial. Es una decisión a revisar.

## 3. Nodos y dependencias tocados en `dag.yaml`

`dag.yaml` pasa a `revision: 10` con nota, y `status` de `final_plan_reviewed` a `final_plan_pending_current_reviews`: sin ese cambio `validate_plan.py` exige cero reseñas pendientes o desactualizadas (`assert not review_problems` solo para los otros dos estados). No toqué `context_review` de ningún nodo existente.

- **Nodos nuevos** (con `context_review: {evidence: [], required_protocol: ritual-context-review, status: pending}`, `promotion: not_authorized`, `node_role: delivery`): WS46 (`dag.yaml:2954`), WS47 (`:2994`), WS48 (`:3033`). IDs contiguos porque `validate_plan.py` exige que los nodos sin punto cubran WS01..WS48 y pertenezcan a un paquete: los agregué a `children` de PK05 con una frase en su `scope`.
- **`depends_on` añadidos:** WS19.1 (+WS47, +WS48), WS19.2 (+WS47, +WS48), WS25.1 (+WS48), WS25.2 (+WS46, +WS48), WS26.1 (+WS48), WS26.2 (+WS48), WS28 (+WS48), WS39 (+WS48), WS42 (+WS48).
- **Texto de aceptación o alcance:** WS19.1 (admisión de WS48, contenido no declarado espera WS47), WS19.2 (baja de RelationDoc vs referencia, canal S03, local no la habilita, protegidos, WS47 y WS48), WS25.2 (alcance y aceptación: depende de WS46, no se cumple declarando no disponible).
- **Gates:** `scope_nodes` de G_WRITE_CONTRACT (+WS46, WS47, WS48), G_UI_WRITE (+WS48) y G_SLDB_WRITE (+WS47). Verifiqué por script que `scope_nodes` coincide con los nodos que declaran cada gate. No creé gates nuevos: la dependencia entre nodos más los recibos por delta existentes bastan; un gate por productor es la alternativa más pesada.
- **Sin cambio:** WS12, WS45, WS33.2 (HO-18 se contrastó y no se duplicó), WS25.1 (sin cambio de texto, solo la dependencia), `execution_authorized: false`, `promotion: not_authorized`.

### Medición preliminar de invalidación (solo lectura, `context_review.py status`)

Línea base antes del parche: 0 obsoletas (verificada sobre una copia de la revisión 9). Con el parche: **35 nodos con «input changed» más 3 pendientes (WS46-WS48)**. De los 35, la mayor parte la causa el cambio de `scope_nodes` de los tres gates (los nodos que los citan, incluidos WS20, WS21, WS32.x, WS33.x, WS34.x, WS36, WS43 y WS45, que no son consumidores reales). Alternativa medida en una copia: si los tres nodos nuevos no declaran ningún gate (sin tocar `scope_nodes`), baja a **20 obsoletas más 3 pendientes**, a costa de dejar los nuevos fuera de la evaluación por delta de G_WRITE_CONTRACT y de los recibos G_UI_WRITE / G_SLDB_WRITE. Dejé la versión con gates; la elección es de root. Lista oficial de invalidación: la corre el Supervisor tras regenerar derivados.

## 4. Qué abrí y qué no

**Abrí (todo en solo lectura):** los archivos que mandaba el encargo (`review-source.md`, `preflight-disposition.md`, la TaskDoc, OP completo por tramos, los nodos de `dag.yaml` pedidos y los gates, `decisiones.md`, `navegacion.md` §3.2, `validate_plan.py`, `context_review.py`, `build_plan.py`). Fuentes de cada hallazgo: `SL/cli/serve/{save_plan,save_routes,docs_create_route,docs_routes}.py`, `SL/api/documents/{payload_save,payload_save_steps}.py`, `SL:tests/test_serve.py` (tramos `:180-300`, `:600-690`), `SL:tests/test_serve_edges_docs.py`; `DK/deskops/services/{closure,tasks,closeout_gates}.py`, `cli/commands/{operations,closeout}.py`, `operations.py:610-630`, `DK:tests/test_operational.py`; `GU/{persistence,serve,deskops_routes,views_routes}.py`, `GU:tests/test_mindmap_persistence.py` (tramo `:40-64`).

**No abrí / no verifiqué:** spec2viz; pron más allá de lo citado antes; `GU/sldb_adapter.py` (citado de OP original); `workspace/` sin commit (excluido); `navegacion.md` fuera de §3; las demás secciones de OP no corregidas las leí pero no las re-contrasté con fuente; los 13 tests del helper; ningún test se ejecutó. Las 65 filas de 2.x no se re-certificaron una por una: solo las vecinas de los hallazgos (W01, W19, W20, S01, S02, S05, U01, U02, X02, X03, X05). Los números de línea de `dag.yaml` citados en OP son de la revisión 9, salvo los nodos nuevos que cito aquí. El código de deskops en HEAD (`18a053ae`) no difiere del de `826ca4a0`: `git diff --stat 826ca4a0 HEAD -- deskops tests desk/lifecycle pyproject.toml` salió vacío.

**Pendiente del Supervisor:** regenerar derivados (`build_plan.py`: crea las fichas `task-ws46/47/48.md` que `validate_plan.py` exige; hoy fallaría por eso), medir invalidación oficial, enviar el gap de `/save` al inbox de sldb, revisión independiente, congelar y entregar a root.

## 5. Discrepancias con compromisos humanos

**Ninguna.** P03 (lectura o handoff con otro coordinador; lock solo de UI no basta) y T-P03.1 (la ausencia de señal no declara exclusividad) se conservan; P04, P05 y P06 no cambian; la base manual sigue difiriendo HO-04 y HO-06. Observaciones para root, no discrepancias:

1. WS47 y WS48 añaden dos deltas más cuyo recibo registra el receptor P01 (el solicitante). Es el mecanismo ya aceptado (P01, recepción técnica por delta), no un compromiso nuevo, pero aumenta el número de actas pendientes.
2. WS48 pide una afirmación vigente del responsable del desk (F1). Eso estaba ya en T-P03.1; solo se hace explícito quién la produce. No se inventó formato ni valor.
3. Decisiones de encaje que root puede querer revertir: gates en los nodos nuevos vs menor invalidación, WS46 como una sola unidad, WS48 sin `G_HUMAN_READ`, y la dependencia de WS26.1 con WS47 (dejada como obligación de TaskDoc).

## Lectura del Supervisor

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Leí `contratos/operaciones.md` completo, §§1-13, sobre los bytes de este parche, y el diff de `dag.yaml`. Contrasté en fuente la cadena de `/save` (`save_plan.py:49-54`, `save_routes.py:61-107`). Lo demás del cotejo es del Executor y de los Testers. Regeneré derivados con `build_plan.py`, `render_diagram.py` y `validate_plan.py`.

Residuos que anoto para root: U03 (`POST /api/desk/advance`) ya existe sin admisión y ningún nodo lo liga a WS48; WS19.2 no habilita la baja de RelationDoc en modo local.

## Ajuste del Supervisor tras Testers de bloques

Claude Opus 5.5, sin Executor. Evidencia en `renovacion-1/`. Reales y corregidos: §13.3, gemela de W01; W19, nota de test inexacta (`test_closeout.py:211` sí cierra sin TaskDoc, sin aseverar el gate); WS21 faltaba como consumidor de WS48, ahora en §5.7, §5.9, §10, HO-03 y `depends_on`; U03 ya no se presenta como condicionada: es ruta existente sin nodo que la reclame.
