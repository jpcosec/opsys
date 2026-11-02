# Corrección de WS12, congelación para revisión root

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Nada ejecutado en runtime. No es aprobación de nadie. Contrato en borrador. `G_WRITE_CONTRACT` sigue pendiente. **Sin renovar nada, sin closeout: la tarea sigue activa.**

- `contratos/operaciones.md` sha256 `b26aa96cccfc6c084d6bfb6ef5323a1d5d10771ae5195ba32e376ab254872128`
- `dag.yaml` revisión 10, sha256 `6870a6304af3fadeeb62a6339683a113128713ef94adcd3b66e9d3093029c9e5`
- `patch-contrato.diff` sha256 `d96b8049cbbe92d14d4d5327e81d9d29cbfafe9c6f34ab742cf01fc1cb66de32`, `patch-dag.diff` sha256 `b9609cf076b70a98bb0bd6f0df2022a9979a0573aaaf0e7fd30698958aea8a60`, ambos desde `4e46f60d`
- Matriz hallazgo → cambio → productor → consumidor: `result-summary.md`, sección 1. Sus números de línea son anteriores a los ajustes de Tester; las secciones valen.

## Propuesta canónica

| Nodo | Repo | Decisión | Consumidores |
|---|---|---|---|
| WS46, captura con origen | deskops | D, HO-11, HO-11b | WS25.2 |
| WS47, guarda de contenido no declarado | sldb | B, HO-07 | WS19.1, WS19.2; WS21 por WS19 |
| WS48, admisión de escritura | graph_ui | C, HO-03 | WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39, WS42 |

Sin gates nuevos. `scope_nodes`: G_WRITE_CONTRACT 29, G_UI_WRITE 15, G_SLDB_WRITE 3. Sin ciclos, comprobado por script. WS12, WS45 y WS33.2 sin cambios. HO-05 lo produce WS19.2, ampliando su aceptación. Hijos de PK05: los tres nuevos.

Encaje B: nodo atómico WS47 y no WS45, porque cambiaría su sentido, gate y radio. Justificación en §6.5 y `result-summary.md`.

## Invalidación medida (`stale-medido.log`, sin renovar)

**35 «input changed» y 3 pendientes (WS46, WS47, WS48)**, sobre 76 nodos: ROOT, PK05, PK07, WS12, WS13, WS19, WS19.1, WS19.2, WS20, WS21, WS22, WS24, WS25, WS25.1, WS25.2, WS26, WS26.1, WS26.2, WS27, WS28, WS30, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2, WS34, WS34.1, WS34.2, WS36, WS39, WS42, WS43, WS45.

El Executor reporta que la mayor parte viene de cambiar `scope_nodes`, que arrastra a nodos no consumidores (WS20, WS21, WS32.x, WS33.x, WS34.x, WS36, WS43, WS45), y que sin gates en los nodos nuevos serían 20 más 3. **Esa cifra es suya, no la medí, y fue antes de añadir WS21.** Dejarlos fuera de la evaluación por delta no me parece buena opción, pero es tu decisión.

`validate --check`: ver `freeze-validation.log`. `dag.yaml` pasó a `status: final_plan_pending_current_reviews`, sin lo cual el validador exige cero pendientes. Hay que devolverlo tras renovar.

## Evidencia y sus bytes

| Revisión | Cobertura | Bytes | Resultado |
|---|---|---|---|
| Supervisor | §§1-13 leídas completas; cadena de `/save` en fuente; diff de `dag.yaml` | `e9cb4e82` más el diff posterior | Sin leer filas de código fuera de lo citado |
| Tester A | Hallazgos 1-6 y gemelas | `72b84042` | FAIL, 2 reales, `renovacion-1/` |
| Tester B | 7, 8, A-E, propuesta DAG | `72b84042`, dag `d6b9405a` | FAIL, 2 reales, `renovacion-1/` |
| Tester focal | Los cuatro FAIL | contrato final, dag `d6b9405a` | FAIL: **mi script abortó antes de escribir `dag.yaml`** y commiteé igual; lo vio el Tester. `renovacion-2/` |
| Tester focal | Los mismos | **finales** | PASS |

No certifica las 65 filas: solo bloques afectados, sin Tester completo sobre bytes finales. Tester deepseek-flash sin shell ni git. Conteos de 2.7 sin cambio: COMP 38, LEC 13, NOAC 6, HUE 8, del Executor.

## Intake

`sldb/desk/inbox/20261102-011823-unclear-post-save-no-rechaza-payload-invalido-de-update-…`, entregado, sin commit en sldb. Rotulado como lectura estática, sin reproducir, sin proponer reparación. Es el único.

## Para root

1. Discrepancia con compromisos humanos: ninguna identificada.
2. Encajes a revisar: gates en nodos nuevos frente a menor invalidación; WS46 como una sola unidad; WS48 sin `G_HUMAN_READ`; WS26.1 con WS47, dejado como obligación de TaskDoc.
3. U03 (`POST /api/desk/advance`) existe hoy sin admisión y ningún nodo la reclama. Se declara límite; no se habilita.
4. WS19.2: en modo local la baja de RelationDoc no se habilita y se declara. Revisa si encaja con lo comprometido.
5. HO-03 nombra dueño deskops para el «registro del coordinador»; WS48 es de graph_ui. No hay nodo deskops para eso.

## Propuesta de revisión fresca, sin lanzar

pi deepseek-flash, sin herramientas ni historial, SYSTEM v2 del helper leído y no modificado. Dos entradas independientes: **WS19.1** (contrato completo, nodos WS19.1, WS47, WS48, WS45) y **WS25.2** (contrato completo, nodos WS25.2, WS46, WS48). Reformulación, ambigüedades y dry-run; ni Tester ni status del helper. Recibos con PID. Costo: dos ejecuciones.
