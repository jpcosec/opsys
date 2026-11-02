## Separación de fuentes

**LECTURA PROPIA** (abiertos en esta sesión): `GU/views/workflow/deskops/deskops-view.js`, `GU/deskops_routes.py`, `SL/cli/serve/save_plan.py`, `SL/cli/serve/save_routes.py`, `DK/deskops/operations.py`, `DK/deskops/services/drawer.py`, `DK/deskops/models/task.py`, `DK/deskops/services/closeout_gates.py`, contrato `operaciones.md`, `dag.yaml`, los dos diffs.

**DATO DEL SUPERVISOR**: `tester-p2-facts.log` solo contiene HEAD `3b4a6c35` y los sha256 de contrato y DAG; no aporta hallazgos.

## Tabla

| Objeto | Evidencia real | Resultado |
|---|---|---|
| U03: vista ya usa botón y POST | `GU/views/workflow/deskops/deskops-view.js:27-30,51` | PASS |
| U03: rechazo servidor antes de `advance_task`; sin lifecycle nuevo | `GU/deskops_routes.py:111-116`; contrato `operaciones.md:142,273,371`; `dag.yaml:3073-3089` | PASS |
| §4.2 U03 ya no “ruta latente”; §5.9, WS48 y U03 coinciden | `operaciones.md:273,365,371`; `dag.yaml:3073-3089` | PASS |
| WS26.1 `depends_on` WS47 y `requires` `G_PAYLOAD_PRECONDITION` | `dag.yaml:1799-1808` | PASS |
| Obligación ligada al guardado por `update`, no a creación | `operaciones.md:270,392`; `dag.yaml:1813-1819` | PASS |
| Coherencia DAG: enumeración de consumidores de `G_PAYLOAD_PRECONDITION` sigue omitiendo WS26.1 | `dag.yaml:7` y `dag.yaml:3366` frente a `dag.yaml:1807` y `operaciones.md:54` | **FAIL** |
| WS26.2 hereda por dependencia; sin ciclos | `dag.yaml:1849-1856`; `operaciones.md:622` | PASS |
| W01 descrita como creación más Board, nunca parcial | `operaciones.md:95,271`; `dag.yaml:1863-1868` | PASS |
| Frase residual hace que WS26.1 invoque la creación activa | `operaciones.md:95`: “Quien invoque la API (graph_ui, **WS26.1**) … antes de crear” | **FAIL** |
| W06 no se presenta como edición de candidato | `operaciones.md:100,225,270`; `DK/deskops/operations.py:284-286`; `_editable_artifact` `:1235-1245` | PASS |
| Gemela residual: “WS26.1 solo vincula pills” | `operaciones.md:230` frente a `:225,270` y al nuevo scope WS26.1 | **FAIL** |
| Sin API de promoción inventada | `operaciones.md:270`; `dag.yaml:1818`; `operaciones.md:521` | PASS |
| HO-03: sin registro nuevo del coordinador; deskops solo consulta | `operaciones.md:683`; `dag.yaml:3078-3084` | PASS |
| Prompt Scion no es señal | `operaciones.md:314`; `dag.yaml:3080-3081` | PASS |
| Revocación, caducidad y respuesta ante error | `operaciones.md:314,322-330`; `dag.yaml:3086-3089` | PASS |
| §6.3 fila CLI/ack frente a §8 | `operaciones.md:412` frente a `:492-504` | PASS |
| S01/S02/U01/§6.2/§9.4: validación de `update` se ejecuta pero no se propaga | `save_plan.py:49-54`; `save_routes.py:61-70,94-107`; `operaciones.md:126-127,140,388,536` | PASS |
| Sin gemela de “no valida payload de update” en esas secciones | búsqueda en contrato: solo `W03/W05/W09` con otros objetos | PASS |
| WS47: update seguro se aplica; sin merge prometido; inspecciona archivo previo; regresión `expected` | `operaciones.md:430-438`; `dag.yaml:3030-3047`; `DK/deskops/operations.py:1297-1326` | PASS |
| Gaps §4.2 (a) candidato no rastreado | `operaciones.md:270`; `drawer.py:117-134`: `transaction.record` solo guarda bytes, no rastrea | PASS, gap real |
| Gaps §4.2 (b) `closeout_evidence` sin vocabulario | `deskops/models/task.py:165-172`; `closeout_gates.py:23,64-67`; S02/W03 no lo validan | PASS, gap real |
| Gaps §4.2 (c) pills como lista entera | `operaciones.md:225`; `bind_pill_to_task` solo `desk/tasks/`; W02 reemplaza listas completas | PASS, gap real |
| Diff no toca `context_review` de nodo existente | hunks en `dag.yaml` solo `revision_note`, WS26.1, WS26.2, WS47, WS48 y `hierarchy`; `context_review` de WS26.1/26.2/47/48 queda intacto | PASS, con estado `reviewed` obsoleto ya declarado en `revision_note` |

## FAIL y corrección implicada

1. **WS26.1 sigue apareciendo como invocador de la creación activa** — `operaciones.md:95` dice que “graph_ui, WS26.1” debe comprobar evidencia “antes de crear”. Corregir a WS26.2.
2. **Atribución residual de pills a WS26.1** — `operaciones.md:230` dice “WS26.1 solo vincula pills”; contradice que `bind pill` no alcanza candidatos y que WS26.1 edita `pills` como campo. Sustituir por “WS26.1 edita el campo `pills` del candidato como lista completa; `bind` es de tarea activa (W06)”.
3. **Enumeración del gate incompleta en DAG** — `dag.yaml:7` y `dag.yaml:3366` enumeran consumidores de `G_PAYLOAD_PRECONDITION` sin WS26.1, mientras `dag.yaml:1807` lo declara `requires`. Añadir WS26.1 (y la herencia de WS26.2) o corregir la enumeración.

## Cobertura

Verificados los siete ajustes y los puntos extra sobre los archivos citados; no se revisaron las 65 filas del DAG ni se ejecutó código. La cobertura es focal: contrato completo en las secciones 1.5, 2.3–2.5, 3.3, 4.2, 5.3–5.9, 6.2–6.7, 8, 9.3–9.4, 10.2 y 12; DAG en WS26.1, WS26.2, WS47, WS48, gates y jerarquía; código en las citas abiertas.

RESULTADO: FAIL
