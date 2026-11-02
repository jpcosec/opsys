## DATO DEL SUPERVISOR

Leído de `runs/subagents/20261102-ws12-correccion/tester-facts.log`; no lo verifiqué con hashes ni ejecución:
- HEAD deskops: `e9cb4e82`
- sha256 `operaciones.md`: `72b84042525a…`
- sha256 `dag.yaml`: `d6b9405a6bdd…`
- stale medido: 38 entradas; `build --check` verde.

## LECTURA PROPIA

| Objeto | Evidencia real (archivo:línea) | Veredicto |
|---|---|---|
| 7 · WS25.2 no se cumple declarando «no disponible» | OP:458, OP:470-472; dag:1732-1738; X02 en OP:151 | PASS |
| 7 · WS46 prueba primero la composición pública | dag:2963-2985; OP:466-472 | PASS |
| 7 · X03/origen del protoátomo y prueba separada | OP:152; dag:2978-2987 | PASS |
| 8 · tres planos de «actor» separados | OP:594-595; OP:684 | PASS |
| 8 · sin bloqueo global del ack | OP:496; OP:684 | PASS |
| 8 · WS33.2 conserva actor humano identificado | dag:2394-2401 | PASS |
| A · HO-05: baja borra documento+índice; local solo destrackea; no equivalente | OP:679; OP:390; dag:1380-1387 | PASS |
| A · U01/S03 y tests citados | `persistence.py:101-115`; `sldb_adapter.py:299-310`; `delete_document.py:34-35`; `test_mindmap_persistence.py:45,54`; `test_serve.py:1095` | PASS |
| B · tres garantías distintas; WS47 atómico y WS45 no ampliado | OP:385, OP:422, OP:428; dag:2911-2953 frente a dag:2994-3032 | PASS |
| C · solo contrato de admisión, sin identidad/autenticación/coordinación | OP:358-370; dag:3044-3065 | PASS |
| C · sin dependencia accidental hacia WS19.1 | dag:3038-3040; dag:1676-1678; dag:1711-1714 | PASS |
| C · cobertura de consumidores de WS48 | OP:364, OP:594, OP:677; OP:390; dag:1452-1454 | **FAIL** |
| C · W04/U03 condicionado a WS48 | OP:272 frente a OP:364/594/677; sin nodo en el DAG | **FAIL** |
| D · WS46 pruebas por destino, sin wrapper/modelo impuesto | dag:2977-2987 | PASS |
| E · §9.5 ruta por ruta | `GU/serve.py:383-384,390-418,432-443`; `GU/deskops_routes.py:96-97,103-112`; `SL/.../docs_routes.py:105-112`; `docs_create_route.py:13,36,45` | PASS |
| E · HO-04, HO-06, HO-09, HO-18 | OP:678,680,683,693; dag:2381-2405 | PASS |
| DAG · forma de WS46/47/48 frente a vecinos | dag:2954-3073; existen `task-ws46/47/48.md` | PASS |
| DAG · gates y `scope_nodes` | dag:161-163,225,244; los tres nodos declaran su gate | PASS |
| DAG · `depends_on` y ciclos | dag:2959-2961,2999-3001,3038-3040; los nuevos solo dependen de WS12 | PASS |
| DAG · `context_review` existente | `patch-dag.diff:210,249,290`; solo aparece en nodos nuevos | PASS |
| DAG · `promotion` y `execution_authorized` | dag:18,2986-2987,3025-3026,3066-3067 | PASS |
| DAG · compromisos humanos P03–P06/T-P03.1 | `decisiones.md:29-36`; el diff no toca ese archivo | PASS |
| Citas `dag.yaml` de OP | OP:776 declara que son de rev9; en rev10 WS45 está en 2911-2953, no en 2883-2927 | PASS con nota |

## FAIL Y CORRECCIÓN IMPLICADA

- **FAIL C · WS21 omitido como consumidor de WS48.** WS21 escribe por campos (OP:390) y está en `G_UI_WRITE` (OP:610), pero falta en las listas de consumidores de WS48 (OP:364, OP:594, OP:677), en la fila 10.2 (OP:610) y en `depends_on` del DAG (dag:1452-1454). Corrección: añadir WS21 a las tres listas y `WS48` a su `depends_on`, o justificar por escrito por qué WS19 lo cubre y corregir 5.9 «ninguna la toma de WS19.1».
- **FAIL C · W04/U03 sin encaje.** OP:272 condiciona `POST /api/desk/advance` a la admisión de WS48, pero 5.9/10.1/HO-03 no lo listan y ningún nodo del DAG declara esa dependencia. Corrección: incluir U03 en el conjunto de consumidores y en el nodo que lo posea, o retirar la condición de OP:272 y declarar esa ruta fuera de los deltas habilitados.

## COBERTURA EXACTA

Leí: diffs completos; OP por tramos (1.5, 2.2–2.6, 3.3, 4.2–4.3, 5–8, 9.4–9.6, 10, 12, 13.5); `dag.yaml` (gates y nodos WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS33.2, WS39, WS42, WS45, WS46, WS47, WS48 y PK05); `decisiones.md`; fuentes y tests citados en las filas de arriba. No revisé las 65 filas ni las secciones no afectadas una por una.

## NO VERIFICADO

- Hashes y estado de `context_review.py`/`build_plan.py`: dato del Supervisor, no reproducido.
- Ninguna prueba se ejecutó ni se reprodujo runtime.
- No abrí todos los tests citados: de `test_serve.py` abrí `:247`, `:262`, `:1095`, no `:187`, `:213`, `:228` ni los de `/docs`; tampoco `test_serve_edges_docs.py`.
- No abrí spec2viz ni pron más allá de las citas del contrato.
- No certifico las 65 filas de la matriz por extensión.

RESULTADO: FAIL
