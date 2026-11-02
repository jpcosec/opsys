No ejecuté nada. Todo lo siguiente es lectura estática de archivos; no afirmo comportamiento en runtime.

## DATO DEL SUPERVISOR
- `runs/subagents/20261101-ws12-operaciones/tester-facts.log`: HEAD deskops `92ed7ed6`, sldb `77bd6d00`, graph_ui `134a665`, pron `e1e9df0`, sha256 de `operaciones.md` `f91227ec…`. Los checks del Supervisor dieron exit 0.
- Discrepancia declarada: `operaciones.md:14` dice HEAD observado `826ca4a0…`; el log dice `92ed7ed6`. No verifiqué el commit de la corrida y las secciones 10–13 no dependen de él.

## LECTURA PROPIA — Sección 10

### 10.1

| Afirmación | Evidencia | Resultado |
|---|---|---|
| `G_WRITE_CONTRACT` y `G_UI_WRITE` son `per_delta` y `accepted_scope_nodes: []` | `dag.yaml:132-133,222-223`; `operaciones.md:548` | PASS |
| El recibo lo registra P01 en su repo; WS12 no crea actas | `operaciones.md:549`; `dag.yaml:195-224` | PASS |
| Deltas de deskops sin recepción nueva | `operaciones.md:550`; nodos WS32–WS34, WS43 sin `G_UI_WRITE`/`G_SLDB_WRITE` | PASS |
| «Su prueba es de `tests/` de deskops en un store temporal» aplicado a todos, incluido WS43 | `operaciones.md:550`; WS43 es documentación y su aceptación pide publicación/acta/commit, no tests en store temporal: `dag.yaml:2815-2822` | FAIL |
| Los agregados no tienen recibo propio y se cumplen por hijos | `operaciones.md:551`; `navegacion.md:397` | PASS |
| Lectura, intake, ack y captura no esperan Changes/modelos/Scion/raw-source | `operaciones.md:552`; `dag.yaml:744-749` | PASS |
| `G_CLOSEOUT` satisfied; `G_SOURCE` lo produce WS20; `G_PAYLOAD_PRECONDITION` lo produce WS45; `G_SLDB_WRITE` cubre WS20/WS45 | `operaciones.md:553`; `dag.yaml:33-49,51-62,225-242` | PASS |

### 10.2 — 26 IDs

| ID | Gate/cobertura declarada | Evidencia | Resultado |
|---|---|---|---|
| WS19 | agregado, hijos | `operaciones.md:561`; `dag.yaml:1260` | PASS |
| WS19.1 | G_WRITE_CONTRACT, G_UI_WRITE, G_PAYLOAD_PRECONDITION, G_HUMAN_READ | `operaciones.md:562`; `dag.yaml:1306-1316` | PASS |
| WS19.2 | ídem | `operaciones.md:563`; `dag.yaml:1350-1360` | PASS |
| WS20 | incluye G_SOURCE como gate consumido | `operaciones.md:564`; `dag.yaml:44-49` dice `produced_by: WS20`; `dag.yaml:1390-1397` solo requiere `G_SLDB_WRITE`, `G_WRITE_CONTRACT` | FAIL |
| WS21 | G_PAYLOAD_PRECONDITION; G_SOURCE solo editable | `operaciones.md:565`; `dag.yaml:1431-1440,1468-1473` | PASS |
| WS25 | agregado | `operaciones.md:566`; `dag.yaml:1618` | PASS |
| WS25.1 | G_WRITE_CONTRACT, G_UI_WRITE, G_HUMAN_READ | `operaciones.md:567`; `dag.yaml:1654-1663` | PASS |
| WS25.2 | ídem | `operaciones.md:568`; `dag.yaml:1688-1697` | PASS |
| WS26 | agregado | `operaciones.md:569`; `dag.yaml:1730` | PASS |
| WS26.1 | + G_CLOSEOUT | `operaciones.md:570`; `dag.yaml:1771-1781` | PASS |
| WS26.2 | ídem | `operaciones.md:571`; `dag.yaml:1808-1818` | PASS |
| WS28 | G_WRITE_CONTRACT, G_UI_WRITE, G_CLOSEOUT, G_HUMAN_READ | `operaciones.md:572`; `dag.yaml:1972-1982` | PASS |
| WS32 | agregado | `operaciones.md:573`; `dag.yaml:2138` | PASS |
| WS32.1 | G_WRITE_CONTRACT, G_CLOSEOUT, G_SCION | `operaciones.md:574`; `dag.yaml:2182-2192` | PASS |
| WS32.2 | ídem | `operaciones.md:575`; `dag.yaml:2231-2241` | PASS |
| WS33 | agregado | `operaciones.md:576`; `dag.yaml:2278` | PASS |
| WS33.1 | G_WRITE_CONTRACT, G_SCION | `operaciones.md:577`; `dag.yaml:2315-2325` | PASS |
| WS33.2 | ídem | `operaciones.md:578`; `dag.yaml:2355-2365` | PASS |
| WS34 | agregado | `operaciones.md:579`; `dag.yaml:2392` | PASS |
| WS34.1 | G_WRITE_CONTRACT, G_EXEC, G_SCION | `operaciones.md:580`; `dag.yaml:2427-2437` | PASS |
| WS34.2 | ídem | `operaciones.md:581`; `dag.yaml:2465-2475` | PASS |
| WS36 | + G_UI_WRITE | `operaciones.md:582`; `dag.yaml:2534-2544` | PASS |
| WS39 | G_WRITE_CONTRACT, G_UI_WRITE, G_HUMAN_READ | `operaciones.md:583`; `dag.yaml:2632-2642` | PASS |
| WS42 | ídem | `operaciones.md:584`; `dag.yaml:2747-2757` | PASS |
| WS43 | G_WRITE_CONTRACT, G_PRODUCT, G_HUMAN_MANUAL; «Tests y commit» | `operaciones.md:585`; gates coinciden en `dag.yaml:2794-2804`; «Tests» no está en la aceptación `dag.yaml:2815-2822` | FAIL |
| WS45 | G_WRITE_CONTRACT, G_SLDB_WRITE | `operaciones.md:586`; `dag.yaml:2883-2893` | PASS |

- Los 26 IDs coinciden exactamente con `scope_nodes` de `G_WRITE_CONTRACT`: `dag.yaml:130-157`. PASS.
- `G_UI_WRITE` son 14 IDs y `G_SLDB_WRITE` son WS20/WS45: `dag.yaml:217-241`; coincide con `operaciones.md:588-589`. PASS.
- No se crea acta: `operaciones.md:549` y `operaciones.md:18-19`. PASS.
- Recibos por delta, no conjuntos: `operaciones.md:548-551`. PASS.

## Sección 11

| Afirmación | Evidencia | Resultado |
|---|---|---|
| No fija valor numérico nuevo de timeout | `operaciones.md:592` | PASS |
| Clasificación aceptado/rechazado/vencido sin confirmación | `operaciones.md:601,614` | PASS |
| No hay inventario WS05 ni probe WS44; `auditoria/scion.md` y `scion-probe.md` ausentes | `operaciones.md:594`; `find` sin resultados en `auditoria/` | PASS |
| No activa Scion; cita `autorizaciones/scion.md` inexistente | `operaciones.md:592,618`; no hay `autorizaciones/` | PASS |
| `dag.yaml:2427` es el alcance de WS34.1 | `dag.yaml:2427` | PASS |
| Precedentes: `supervise --timeout-ms` observacional y tope de 10 s de lectura | `deskops/runtime/supervise.py:27-30,44-66`; `GU/serve.py:175` | PASS |
| HO-19 productor «corrección documental» no es nodo del DAG ni «sin productor» | `operaciones.md:646`; no existe nodo de corrección en `dag.yaml` | FAIL |

## Sección 12 — huecos

| Hueco | Clase / dueño / productor | Evidencia | Resultado |
|---|---|---|---|
| HO-01 | API/renderer; graph_ui; WS26.1, WS26.2, WS27.2, WS28, WS25.1, WS25.2, WS42 | `operaciones.md:627`; nodos existen en `dag.yaml` | PASS |
| HO-02 | API; graph_ui; WS19.1, WS19.2, WS26.1 | `operaciones.md:628`; `dag.yaml:1306,1350,1771` | PASS |
| HO-03 | política; graph_ui/deskops; sin productor | `operaciones.md:629` | PASS |
| HO-04 | API; sldb/deskops; sin productor | `operaciones.md:630` | PASS |
| HO-05 | política; sldb/graph_ui; sin productor | `operaciones.md:631`; tests citados existen: `sldb/tests/test_serve.py:1095`, `GU/tests/test_mindmap_persistence.py:54` | PASS |
| HO-06 | API; sldb; sin productor | `operaciones.md:632` | PASS |
| HO-07 | API; sldb/deskops; sin productor | `operaciones.md:633`; `refuse_*` solo en `create_document.py:60-61` y `track_document_file.py:47-48` | PASS |
| HO-08 | API; sldb; WS20 | `operaciones.md:634`; `dag.yaml:1390` | PASS |
| HO-09 | API; deskops; sin productor | `operaciones.md:635` | PASS |
| HO-10 | API; sldb/deskops/graph_ui; WS33.2 y resto sin productor | `operaciones.md:636`; `dag.yaml:2355` | PASS |
| HO-11 | API/prueba; deskops; sin productor | `operaciones.md:637` | PASS |
| HO-11b | API; deskops; sin productor | `operaciones.md:638` | PASS |
| HO-12 | API; deskops; sin productor | `operaciones.md:639` | PASS |
| HO-13 | API/renderer; graph_ui; WS27.1 | `operaciones.md:640`; `dag.yaml` nodo WS27.1 | PASS |
| HO-14 | consulta/renderer; graph_ui; WS26.2 | `operaciones.md:641`; búsqueda `overlap/solap/disjoint` solo `workspace.py:351` | PASS |
| HO-15 | API; graph_ui/sldb; sin productor | `operaciones.md:642` | PASS |
| HO-16 | API; deskops; WS34.1, WS34.2 | `operaciones.md:643`; `dag.yaml:2427,2465` | PASS |
| HO-17 | política; deskops; WS05 (inventario) | `operaciones.md:644`; WS05 existe en `dag.yaml` | PASS |
| HO-18 | API; deskops; WS33.2 depende y la operación no tiene productor | `operaciones.md:645` | PASS |
| HO-19 | política; deskops; «corrección documental» sin nodo DAG ni «sin productor» | `operaciones.md:646` | FAIL |

## Sección 13

### 13.1 — una fila por frase

| # | Dónde queda / evidencia | Resultado |
|---|---|---|
| 1 | `operaciones.md:653` → 1.2/1.5 existen | PASS |
| 2 | `operaciones.md:654` → secciones 2/3 existen | PASS |
| 3 | `operaciones.md:655` → 10.2 existe | PASS |
| 4 | `operaciones.md:656` → 10.1:549 | PASS |
| 5 | `operaciones.md:657` → 10.1:552 | PASS |
| 6 | `operaciones.md:658` → 10.1/10.2 | PASS |
| 7 | `operaciones.md:659` → 9.6/10.2 | PASS |
| 8 | `operaciones.md:660` → 6.6/10.2/HO-08 | PASS |
| 9 | `operaciones.md:661` → 6.3 | PASS |
| 10 | `operaciones.md:662` → 6.1 | PASS |
| 11 | `operaciones.md:663` → 6.4/5.5 | PASS |
| 12 | `operaciones.md:664` → 6.5 | PASS |
| 13 | `operaciones.md:665` → 7.3 | PASS |
| 14 | `operaciones.md:666` → 7.3/W11 | PASS |
| 15 | `operaciones.md:667` → 7.5/W14/X03/HO-11b | PASS |
| 16 | `operaciones.md:668` → 7.3/7.6/HO-11 | PASS |
| 17 | `operaciones.md:669` → 5.5/5.6 | PASS |
| 18 | `operaciones.md:670` → 1.2 | PASS |
| 19 | `operaciones.md:671` → 1.3/1.4/2 | PASS |
| 20 | `operaciones.md:672` → 2/12 | PASS |
| 21 | `operaciones.md:673` → 10.2 | PASS |
| 22 | `operaciones.md:674` → 6.3/6.5 | PASS |
| 23 | `operaciones.md:675` → 10.1 | PASS |
| 24 | `operaciones.md:676` → 7.1/7.3 | PASS |
| 25 | `operaciones.md:677` → Sección 11/HO-19 | PASS |
| — | Falta la frase de aceptación «Receptor P01 en repo dueño produce acta por delta al prepararlo» (`dag.yaml:769`): no aparece en la tabla de 13.1 | FAIL |

### 13.2 — T-P03.1

| Compromiso | Evidencia | Resultado |
|---|---|---|
| Definición operativa | `operaciones.md:688` → 5.2 | PASS |
| Formas de comprobarla | `operaciones.md:689` → 5.3/5.7 | PASS |
| Respuesta ante ausencia de evidencia | `operaciones.md:690` → 5.4 | PASS |
| La ausencia de señal no declara exclusividad | `operaciones.md:691` → 5.2/5.4 | PASS |
| Sin lock/detección; el lock UI no coordina | `operaciones.md:692` → 5.6/5.8/HO-03 | PASS |
| «Producida antes de habilitar… (cada delta cita 5.7)» | `operaciones.md:693`; solo WS19.1 cita 5.7 y WS19.2 por «Ídem» (`operaciones.md:562-563`); WS25.1, WS25.2, WS26.1, WS26.2, WS39, WS42 no lo citan | FAIL |

### 13.3 — remisiones de `promotion-notes.md`

| Nota | Evidencia | Resultado |
|---|---|---|
| Umbral de timeout | `promotion-notes.md:15`; `operaciones.md:697` | PASS |
| Valor por defecto de captura a drawer | `promotion-notes.md:16`; `operaciones.md:698` | PASS |
| Quién ejecuta la prueba real de captura | `promotion-notes.md:17`; `operaciones.md:699` | PASS |
| Adenda T-P03.1 | `promotion-notes.md:107`; `operaciones.md:700` | PASS |
| Adenda WS09: `atoms validate` crea andamiaje | `promotion-notes.md:113-115`; `operaciones.md:701` | PASS |
| «Adenda: `stores check` clasificado por efectos» | No hay mención de `stores check` en `promotion-notes.md` | FAIL |
| WS26.1 | `promotion-notes.md:43`; `operaciones.md:703` | PASS |
| WS26.2 | `promotion-notes.md:45`; `operaciones.md:704` | PASS |
| WS27.1 | `promotion-notes.md:111`; `operaciones.md:705` | PASS |
| WS27.2 | `promotion-notes.md:54-56`; `operaciones.md:706` | PASS |
| WS28 | `promotion-notes.md:58-60`; `operaciones.md:707` | PASS |
| WS33.2 / WS32.x: actor y ubicación del registro | `promotion-notes.md:65-68` habla de `confirmed` e integración, no de actor/registro; no hay nota de WS33.2 | FAIL |
| WS34.1 | `promotion-notes.md:71-72`; `operaciones.md:709` | PASS |
| WS39: efectos y errores de draft/validate/promote | `promotion-notes.md:80-82` habla de punto de entrada y estado vacío; no de efectos/errores | FAIL |
| WS45 | `promotion-notes.md:84-85`; `operaciones.md:711` | PASS |

### 13.4 — remisiones de `navegacion.md`

| Remisión | Evidencia | Resultado |
|---|---|---|
| §1: escritura, guardado, whitelist, conflictos, fallos parciales | `navegacion.md:19`; `operaciones.md:717` | PASS |
| §7.6/H-15: conflicto 409 | `navegacion.md:290,377`; `operaciones.md:718` | PASS |
| H-25: captura, ack, respuesta local, autoría, edición | `navegacion.md:385`; `operaciones.md:719` | PASS |
| §12.2: 14 nodos `G_UI_WRITE`; `G_SLDB_WRITE` WS20/WS45 | `navegacion.md:414-416`; `operaciones.md:720` | PASS |
| §4: edición de fuente espera WS20/WS21 | `navegacion.md:137`; `operaciones.md:721` | PASS |
| §5.4: lectura sin escrituras; `open_store` migra, `document_edges` reconstruye | `navegacion.md:183-187`; `operaciones.md:722` | PASS |
| §3.2: «una petición de lectura no crea ni migra el store» | `navegacion.md:93` solo dice que una entrada ausente no se sirve y no se crea/migra antes de abrir; `navegacion.md:83` y `operaciones.md:1.4` reconocen que `open_store` migra stores presentes | FAIL |

## FAIL y corrección implicada

1. `operaciones.md:564` (WS20): `G_SOURCE` figura como gate consumido; es producido por WS20 (`dag.yaml:44-49`). Corrección: quitarlo de «Gates que consume» y dejarlo como gate producido.
2. `operaciones.md:550,585` (WS43): se le atribuye prueba en `tests/` y store temporal; su aceptación es publicación/acta/commit en el desk real (`dag.yaml:2815-2822`). Corrección: excluir WS43 de esa regla o escribir su prueba propia.
3. `operaciones.md:646` (HO-19): productor «corrección documental… (no es un nodo del DAG)» no cumple el formato nodo DAG o «sin productor». Corrección: `sin productor en el DAG; la fija una corrección documental al preparar WS34.1/WS34.2`.
4. `operaciones.md:652-677` (13.1): falta la frase de aceptación de `dag.yaml:769` («Receptor P01 en repo dueño produce acta por delta al prepararlo»). Corrección: añadir fila y destino 10.1/10.2.
5. `operaciones.md:693` (13.2): «cada delta cita 5.7» es falso; solo WS19.1/WS19.2. Corrección: decir que 5.7 obliga a los deltas de UI que escriben y que 10.2 la cita en WS19.1/19.2.
6. `operaciones.md:700` (13.3): `stores check` no aparece en `promotion-notes.md`. Corrección: atribuirlo a D01/D05 o quitarlo de la tabla de promotion-notes.
7. `operaciones.md:710` (13.3): WS33.2/WS32.x «actor y ubicación del registro» no consta en `promotion-notes.md`. Corrección: atribuirlo a dag/T-P o retirarlo.
8. `operaciones.md:712` (13.3): WS39 «efectos y errores de draft/validate/promote» no consta en `promotion-notes.md`. Corrección: atribuirlo a S09/U05/5 o retirarlo.
9. `operaciones.md:723` (13.4): la frase sobre §3.2 generaliza de más; §3.2 solo cubre la entrada ausente. Corrección: citar la regla exacta y mantener el aviso MIG de 1.4/§5.4.

## No pude verificar
- No ejecuté tests ni comandos; no hay prueba de runtime.
- No recalculé el sha256 del contrato ni verifiqué el commit real de la corrida; el log del Supervisor y `operaciones.md:14` discrepan en HEAD.
- No abrí `result-summary.md` citado en 13.5.
- En 10.2 comprobé existencia de nodos y listas de gates; no audité la suficiencia sustantiva de cada cruce de cobertura.
- En HO-05 verifiqué nombre y línea de los tests, no su cuerpo ni ejecución.

RESULTADO: FAIL
