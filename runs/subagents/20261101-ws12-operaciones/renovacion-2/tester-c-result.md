No ejecuté nada. Todo lo que sigue es lectura estática, sin runtime ni pruebas.

## DATO DEL SUPERVISOR (`tester-facts.log`)

- HEAD deskops `3dcefa4f`; sldb `77bd6d00`; graph_ui `134a665`; spec2viz `10df4f0`; pron `e1e9df0`.
- sha256 de `operaciones.md`: `6a58a2f2…`.
- `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status`: exit 0.
- Discrepancia: el contrato 1.3 dice que se commiteó como `92ed7ed6` (`operaciones.md:32`); el log dice HEAD `3dcefa4f`. No verifiqué git.

## 10.1 Reglas

| Afirmación | Evidencia | Res. |
|---|---|---|
| `G_WRITE_CONTRACT` y `G_UI_WRITE` son `per_delta` y `accepted_scope_nodes: []` | `dag.yaml:122-157,195-224`; `operaciones.md:549` | PASS |
| P01 registra en su repo; WS12 no crea actas interrepo | `operaciones.md:550`; `decisiones.md:25` | PASS |
| Deltas de deskops sin recepción nueva | `operaciones.md:551`; WS32-WS34 y WS43 no requieren `G_UI_WRITE`/`G_SLDB_WRITE` | PASS |
| «Su prueba es de `tests/` de deskops en store temporal… salvo WS43» aplicado a todos | `operaciones.md:551`; WS34.1 exige agente real `dag.yaml:2444`; WS34.2 exige agente real `dag.yaml:2481`; WS33.1 exige contrato público real `dag.yaml:2334`; WS33.2 decisión humana `dag.yaml:2372`; el propio 10.2 dice «agente real» en `operaciones.md:582-583` | **FAIL** |
| Agregados sin recibo propio; se cumplen por hijos | `operaciones.md:553`; `navegacion.md:398-403` | PASS |
| Lectura/intake/ack/captura no esperan Changes/modelos/Scion/raw-source | `operaciones.md:554`; `dag.yaml:745` | PASS |
| `G_CLOSEOUT` satisfied; `G_SOURCE`→WS20; `G_PAYLOAD_PRECONDITION`→WS45; `G_SLDB_WRITE` cubre WS20/WS45 | `dag.yaml:33-49,51-61,225-241` | PASS |

## 10.2 Tabla de 26 IDs

| ID | Evidencia DAG | Res. |
|---|---|---|
| WS19 | `dag.yaml:1260`; requiere 4 gates en `1267-1274`; la fila pone «—» | **FAIL (gate)** |
| WS19.1 | `dag.yaml:1306-1316` | PASS |
| WS19.2 | `dag.yaml:1350-1360` | PASS |
| WS20 | `dag.yaml:1390-1397`: consume `G_WRITE_CONTRACT`+`G_SLDB_WRITE`, produce `G_SOURCE` | PASS |
| WS21 | `dag.yaml:1431-1440,1462-1472` | PASS |
| WS25 | `dag.yaml:1618`; requiere 3 gates en `1624-1630`; la fila pone «—» | **FAIL (gate)** |
| WS25.1 | `dag.yaml:1654-1663` | PASS |
| WS25.2 | `dag.yaml:1688-1697` | PASS |
| WS26 | `dag.yaml:1730`; requiere 4 gates en `1736-1742`; la fila solo pone `G_CLOSEOUT (hijos)` | **FAIL (gate)** |
| WS26.1 | `dag.yaml:1771-1781` | PASS |
| WS26.2 | `dag.yaml:1808-1818` | PASS |
| WS28 | `dag.yaml:1972-1982` | PASS |
| WS32 | `dag.yaml:2138`; requiere 3 gates en `2144-2150`; la fila pone «—» | **FAIL (gate)** |
| WS32.1 | `dag.yaml:2182-2192` | PASS |
| WS32.2 | `dag.yaml:2231-2241` | PASS |
| WS33 | `dag.yaml:2278`; requiere 2 gates en `2284-2289`; la fila pone «—» | **FAIL (gate)** |
| WS33.1 | `dag.yaml:2315-2325` | PASS |
| WS33.2 | `dag.yaml:2355-2365` | PASS |
| WS34 | `dag.yaml:2392`; requiere 3 gates en `2398-2404`; la fila pone «—» | **FAIL (gate)** |
| WS34.1 | `dag.yaml:2427-2437` | PASS |
| WS34.2 | `dag.yaml:2465-2475` | PASS |
| WS36 | `dag.yaml:2534-2544` | PASS |
| WS39 | `dag.yaml:2632-2642` | PASS |
| WS42 | `dag.yaml:2747-2757` | PASS |
| WS43 | `dag.yaml:2794-2804`; aceptación `2815-2822` | PASS |
| WS45 | `dag.yaml:2883-2893` | PASS |

- Los 26 IDs coinciden exactamente con `scope_nodes` de `G_WRITE_CONTRACT`: `dag.yaml:130-157`. PASS.
- `G_UI_WRITE` son 14 IDs y `G_SLDB_WRITE` WS20/WS45: `dag.yaml:217-241`; coincide con `operaciones.md:589-590`. PASS.
- Recibos por delta y no conjuntos: `operaciones.md:549-551`. PASS.
- No se crea acta: `operaciones.md:14,550`. PASS.

## 11. Ramal E

| Afirmación | Evidencia | Res. |
|---|---|---|
| No fija valor numérico nuevo | `operaciones.md:592-596` | PASS |
| Clasificación aceptado/rechazado/vencido sin confirmación | `operaciones.md:601-606,610-614` | PASS |
| No activa Scion; condiciona a `G_SCION`/`G_EXEC` | `operaciones.md:592-621`; `dag.yaml:63-77` | PASS |
| Cita `autorizaciones/scion.md` inexistente y lo declara | `operaciones.md:605`; no existe `autorizaciones/scion.md` | PASS |
| No hay inventario WS05 ni probe WS44 y lo declara | `operaciones.md:594`; no existen `auditoria/scion.md` ni `auditoria/scion-probe.md`; sí existen los nodos WS05/WS44 (`dag.yaml:454,2844`) | PASS |
| Precedentes 15 s/30 s/10 s/2 s y `supervise` observacional | `../UIs/graph_ui/frontends/mindmap/serve.py:100,111,124,175`; `workspace_routes.py:471`; `deskops/runtime/supervise.py:27-30,44-66` | PASS |
| `dag.yaml:2427` es WS34.1 | `dag.yaml:2427` | PASS |
| HO-19 «sin productor» y corrección documental | `operaciones.md:648`; no hay nodo de timeout | PASS |

## 12. Huecos

| Hueco | Evidencia | Res. |
|---|---|---|
| HO-01 | `operaciones.md:629`; WS26.1, WS26.2, WS27.2, WS28, WS25.1, WS25.2, WS42 existen | PASS |
| HO-02 | `operaciones.md:630`; WS19.1, WS19.2, WS26.1 existen | PASS |
| HO-03 | `operaciones.md:631`; sin productor | PASS |
| HO-04 | `operaciones.md:632`; sin productor | PASS |
| HO-05 | `operaciones.md:633`; tests `../sldb/tests/test_serve.py:1095` y `../UIs/graph_ui/tests/test_mindmap_persistence.py:54` existen y prueban borrado/preservación | PASS |
| HO-06 | `operaciones.md:634`; sin productor | PASS |
| HO-07 | `operaciones.md:635`; `deskops/operations.py:1318-1327` rechaza contenido no declarado; sin productor | PASS |
| HO-08 | `operaciones.md:636`; WS20 | PASS |
| HO-09 | `operaciones.md:637`; sin productor | PASS |
| HO-10 | `operaciones.md:638`; WS33.2 y resto sin productor | PASS |
| HO-11 | `operaciones.md:639`; sin productor | PASS |
| HO-11b | `operaciones.md:640`; sin productor; `deskops/domain_tree.py:129` no recibe provenance | PASS |
| HO-12 | `operaciones.md:641`; sin productor | PASS |
| HO-13 | `operaciones.md:642`; WS27.1 | PASS |
| HO-14 | `operaciones.md:643`; WS26.2; búsqueda `overlap/solap/disjoint` solo `deskops/workspace.py:351` | PASS |
| HO-15 | `operaciones.md:645`; guardas `Origin` condicionales en `deskops_routes.py:96-98` y `serve.py:383-385,432-434`; `views_routes.py:29-32,75` elige `store` | PASS |
| HO-16 | `operaciones.md:645`; WS34.1/WS34.2 | PASS |
| HO-17 | `operaciones.md:646`; WS05 existe; «corrección» no es nodo, pero el productor primario sí es real | PASS |
| HO-18 | `operaciones.md:647`; WS33.2 depende; operación sin productor | PASS |
| HO-19 | `operaciones.md:648`; sin productor en el DAG | PASS |

## 13.1 Aceptación de WS12, frase por frase

| # | Destino | Res. |
|---|---|---|
| 1 | `operaciones.md:13,52` | PASS |
| 2 | secciones 2 y 3, `operaciones.md:54,193` | PASS |
| 3 | `operaciones.md:557-588` | PASS |
| 4 | `operaciones.md:550` | PASS |
| 5 | `operaciones.md:554`; `dag.yaml:745` | PASS |
| 6 | `operaciones.md:549,557-588` | PASS |
| 7 | `operaciones.md:514-525,571-573` | PASS |
| 8 | `operaciones.md:397-399,566,636` | PASS |
| 9 | `operaciones.md:363-386` | PASS |
| 10 | `operaciones.md:349-355` | PASS |
| 11 | `operaciones.md:388-391,331-333` | PASS |
| 12 | `operaciones.md:393-395` | PASS |
| 13 | `operaciones.md:411-421` | PASS |
| 14 | `operaciones.md:411-421,103` | PASS |
| 15 | `operaciones.md:427-429,150,640` | PASS |
| 16 | `operaciones.md:411-433,639` | PASS |
| 17 | `operaciones.md:331-341` | PASS |
| 18 | `operaciones.md:14` | PASS |
| 19 | `operaciones.md:20-48`; columnas de sección 2 | PASS |
| 20 | `operaciones.md:54,623` | PASS |
| 21 | `operaciones.md:566-567,588` | PASS |
| 21b | `operaciones.md:550,557-588`; `dag.yaml:769` | PASS |
| 22 | `operaciones.md:363-395` | PASS |
| 23 | `operaciones.md:550-551`; spec2viz explícito en `operaciones.md:14` | PASS |
| 24 | `operaciones.md:403-405,411-421` | PASS |
| 25 | `operaciones.md:592-621,648` | PASS |

## 13.2 T-P03.1

| Compromiso | Evidencia | Res. |
|---|---|---|
| Definición operativa | `operaciones.md:301-305` | PASS |
| Formas de comprobarla | `operaciones.md:307-317,339-341` | PASS |
| Respuesta ante ausencia de evidencia | `operaciones.md:319-329` | PASS |
| Ausencia de señal no declara exclusividad | `operaciones.md:305,319-329` | PASS |
| Sin lock/detección; lock UI no coordina | `operaciones.md:335-341,631` | PASS |
| Producida antes de habilitar consumidores; 10.1 y WS19.1 | `operaciones.md:552,564,688-694` | PASS |

## 13.3 `promotion-notes.md`

| Nota | Evidencia | Res. |
|---|---|---|
| Umbral de timeout | `promotion-notes.md:15`; `operaciones.md:702` | PASS |
| Valor por defecto de captura | `promotion-notes.md:16`; `operaciones.md:703` | PASS |
| Quién ejecuta prueba real | `promotion-notes.md:17`; `operaciones.md:704` | PASS |
| T-P03.1 obligatorio | `promotion-notes.md:118`; `operaciones.md:705` | PASS |
| `atoms validate` crea andamiaje | `promotion-notes.md:127`; `operaciones.md:706` | PASS |
| `stores check` no consta en promotion-notes | sin coincidencias en `promotion-notes.md`; `preflight-disposition.md:7`; `runs/subagents/20261101-ws09-correccion/preflight-input.md:60`; `operaciones.md:707` | PASS |
| WS26.1 | `promotion-notes.md:47`; `operaciones.md:708`; `deskops/models/task.py:120-123` | PASS |
| WS26.2 | `promotion-notes.md:50`; `operaciones.md:709` | PASS |
| WS27.1 | `promotion-notes.md:53`; `operaciones.md:710` | PASS |
| WS27.2 | `promotion-notes.md:56`; `operaciones.md:711` | PASS |
| WS28 | `promotion-notes.md:59`; `operaciones.md:712` | PASS |
| WS33.2/WS32.x no consta | `promotion-notes.md:66,69` no hablan de actor/ubicación; `dag.yaml:2182,2231,2355`; `operaciones.md:713` | PASS |
| WS34.1 | `promotion-notes.md:72`; `operaciones.md:714` | PASS |
| WS39 no consta | `promotion-notes.md:81` solo punto de entrada; `dag.yaml:2648-2651`; `operaciones.md:715` | PASS |
| WS45 | `promotion-notes.md:85`; `operaciones.md:716` | PASS |

## 13.4 `navegacion.md`

| Remisión | Evidencia | Res. |
|---|---|---|
| §1 | `navegacion.md:19`; `operaciones.md:722` | PASS |
| §7.6/H-15 | `navegacion.md:290,377`; `operaciones.md:723` | PASS |
| H-25 | `navegacion.md:385`; `operaciones.md:724` | PASS |
| §12.2 | `navegacion.md:414-416`; `operaciones.md:725` | PASS |
| §4 | `navegacion.md:137`; `operaciones.md:726` | PASS |
| §5.4 | `navegacion.md:183-187`; `operaciones.md:727`; `W04` en `operaciones.md:98` | PASS |
| §3.2 y «efectos de cada fila rotulados» | `navegacion.md:93`; `operaciones.md:728`; pero R09 `operaciones.md:72`, R10 `:73` y D04 `:86` dicen cuerpos no abiertos/efectos no clasificados | **FAIL** |

## FAIL y corrección implicada

1. `operaciones.md:551` — «Su prueba es de `tests/` de deskops en un store temporal… salvo WS43» contradice `dag.yaml:2444,2481` (WS34.1/2 exigen agente real) y `dag.yaml:2334,2372` (WS33.1/2 exigen contrato público/decisión), y contradice la propia fila 10.2 `operaciones.md:582-583`. Corrección: excluir WS34.1/WS34.2 del store temporal y decir «agente real bajo G_EXEC/G_SCION»; precisar también WS33.1/WS33.2.
2. `operaciones.md:563,568,571,575,578,581` — la columna «Gates que consume» de los agregados pone «—» o solo `G_CLOSEOUT (hijos)`, pero `dag.yaml:1267-1274,1624-1630,1736-1742,2144-2150,2284-2289,2398-2404` muestra que WS19/WS25/WS26/WS32/WS33/WS34 consumen varios gates. Corrección: listar los gates reales de cada agregado o renombrar la columna a «gate propio».
3. `operaciones.md:728` — «Los efectos transitivos (MIG, ALOG, ASC) de cada fila de lectura y diagnóstico están rotulados» es falso: R09 `operaciones.md:72`, R10 `:73` y D04 `:86` declaran cuerpos no abiertos o efectos no clasificados. Corrección: decir «de cada fila abierta» y marcar R09/R10/D04 como no comprobadas.

## No pude verificar

- Runtime de cualquier operación o test; no ejecuté nada.
- sha256 ni commit real de la corrida; el log del Supervisor y `operaciones.md:32` discrepan en HEAD (`3dcefa4f` vs `92ed7ed6`).
- La suficiencia sustantiva de cada «Cobertura» de 10.2; comprobé existencia de nodos y gates.
- Todos los cuerpos de las filas R01-R12/D01-D05; solo abrí R09, R10 y D04 para comprobar la afirmación de 13.4.
- El comportamiento real de `open_store`, `document_edges`, `Origin` y `path`/`store` más allá de la lectura estática.

RESULTADO: FAIL
