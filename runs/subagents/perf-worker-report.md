# perf-worker: cada comando CLI de deskops tarda ~30 s desde CC32/CC35b

TaskDoc: `desk/tasks/task-rendimiento-cada-comando-cli-tarda-30-s-desde-cc32-cc35b.md` (task.debug).
Rama `wt/perf-cli`, base `7a875176`. Fecha: 2026-11-10.

**Veredicto (p3, b2): la causa está en sldb.** El tiempo lo domina `sldb.api.rules.rule_graph`,
que carga el índice de aristas **con todos los stores enlazados** (`load_edge_index(store, True)`)
para evaluar reglas sobre los documentos del store local. deskops no lo llama más de lo que su
API pide, salvo en `advance` (dos llamadas: `edges_holding` y luego `edges_blocked` u
`on_write`), y aun así la primera llamada sola cuesta ~25 s. No hay arreglo en deskops sin
reemplazar una evaluación de sldb (b3, regla 7), así que **no hay commit de código**. La tabla
«con el arreglo» queda pendiente de la tarea en sldb.

## p1. Medición

Montaje: copias detached en `/dev/shm/perfcopies/{pre-cc32,pre-cc35b,main}` (`6afc78b0^`,
`b2673b36^`, `7a875176`); junto a ellas, enlaces simbólicos `sldb`, `spec2viz`, `pron`, `scion`
a los repos reales, para que la federación de stores sea la misma que en un checkout real. Por
versión, un desk nuevo hecho con `python -m deskops init` de esa versión
(`PYTHONPATH=<copia>`), con una tarea `task.code`. sldb es el mismo en las tres
(`sldb-runtime`), así que la diferencia es de deskops: qué API de sldb llama.
Recibos: `tests/activation_receipts.accept_receipts` de la copia (no existe antes de CC32).
Script y crudos: `~/proyectos/SLDB_1/coord2-ccconfig/perf/` (`measure.sh`, `<versión>/`).

Tiempo total (`/usr/bin/time`, s) e import (`-X importtime`, mayor acumulado, s):

| comando | antes de CC32 (`6afc78b0^`) | antes de CC35b (`b2673b36^`) | main hoy (`7a875176`) | con el arreglo |
|---|---|---|---|---|
| `add task` | 1.35 (imp 0.64) | 1.36 (imp 0.63) | **30.11** (imp 0.62) | pendiente (sldb) |
| `show task` | 1.19 (imp 0.64) | **29.16** (imp 0.62) | **29.27** (imp 0.61) | pendiente (sldb) |
| `next` | 1.06 (imp 0.63) | **28.55** (imp 0.61) | **28.82** (imp 0.61) | pendiente (sldb) |
| `advance task` (bloqueada) | 1.42 ¹ | **32.98** | **32.51** | pendiente (sldb) |
| `advance task` (con recibos) | — ¹ | **32.58** | **34.66** | pendiente (sldb) |

¹ Antes de CC32 no hay regla de activación: `advance` avanza directo a `ritual-testing`.

El import no cambió (~0.62 s). La regresión es de ejecución:
- **CC32** la trae a `show`/`next`/`advance` (findings de `on_transition`).
- **CC35a/CC35b** la extienden a `add task`. La escritura del Board pasa por `sldb.api.transaction.update`, que corre `check_rules_on_write` → `rule_graph`.

Además, cada `advance` que escribe la tarea paga otro `rule_graph` por `on_write`.

## p2. Causa raíz

Llamadas por comando en main (cProfile; tiempos bajo profiler, ~2× el real):

| comando | `rule_graph` | `load_edge_index` | `live_stale` | quién llama |
|---|---|---|---|---|
| `add task` | 1 (61.5 s) | 2 | 8 | `transaction.update` del Board → `check_on_write` |
| `show task` | 1 (61.2 s) | 3 | 9 | `TaskService._lifecycle_gates` → `sldb.api.transition_findings` |
| `next` | 1 | 3 | 9 | ídem |
| `advance` bloqueada | 2 (72.4 s) | 7 | 19 | `edges_holding` (61.4 s) + `edges_blocked` (12.3 s) |
| `advance` con recibos | 2 (72.6 s) | 6 | 18 | `edges_holding` (62.6 s) + `on_write` de la tarea (11.9 s) |

Qué lee de disco `rule_graph(store)` (`sldb/api/rules/rule_graph.py:84`):
`load_edge_index(store, True)` → `compose_edge_index` sobre `federated_stores(store, True)`.
En un desk recién creado la federación es transitiva: el desk enlaza el store dueño de deskops
(`deskops init` → `bootstrap._ensure_owner_link`, desde antes de CC32), y ese store enlaza
`sldb`, `spec2viz`, `pron` y `scion`, que vuelven a enlazar `deskops`:

| store | archivos en `.sldb` |
|---|---|
| (local, el desk) | 69 |
| deskops (dueño) | 419 |
| sldb | 3061 |
| spec2viz | 516 |
| pron | 718 |
| scion | 44 |
| deskops (checkout principal) | 1141 |

Medición directa en un proceso (`edge-index-probe.txt`):
- `load_edge_index(include_linked=False)`: **0.27 s**, 521 nodos, 993 aristas.
- `load_edge_index(include_linked=True)`: **27.09 s** en frío y 3.15 s en caliente (mismo proceso), con 28 927 nodos y 159 433 aristas.
- `rule_graph`, después de invalidar `_COMPOSED` pero con los shards ya parseados: 10.42 s. En caliente: 3.47 s.
- Documentos locales sobre los que se evalúan las reglas: **21**.

El tiempo se reparte así (cProfile de `show task`):
- ~9 600 lecturas de shards (`load_edges_shard`): yaml en Python puro, 30 s bajo profiler.
- `model_copy`/`deepcopy` de pydantic en `_cached_shard`: 266 218 copias, 24.7 s.
- `live_stale`: rehashea en cada llamada los archivos de todos los stores federados, 12.3 s por 9 llamadas.

Es decir: para evaluar reglas sobre 21 documentos locales, sldb parsea y copia el índice de
~29 000 nodos de seis stores ajenos, en cada proceso.

## p3 / b2 / b3. Dónde se arregla

- La función que domina el tiempo acumulado (`rule_graph` → `compose_edge_index`, `_cached_shard`, `yaml_load`, `live_stale`) está en el paquete `sldb/`. Por b2, **es de sldb**.
- deskops llama una vez por comando a la API pública, como corresponde (`transition_findings`, `edges_holding`, `edges_blocked`, `transaction.update`). El único doble cargo es el de `advance` (holding + blocked/on_write, ~12 s extra en caliente). Esas API no aceptan un grafo ya cargado, así que compartirlo desde deskops sería reimplementar la evaluación o esconder el costo con una caché propia, lo que b3 prohíbe. Además, aunque se quitara, la primera llamada sigue en ~25 s.
- El enlace al store dueño no es nuevo (precede a CC32) y es como deskops hereda sus modelos. Quitarlo cambiaría la semántica de init, fuera del alcance.

Propuesta para la tarea de sldb (hipótesis; la decide sldb):
1. Que `rule_graph` cargue los stores enlazados solo si alguna regla del store los recorre. O bien que componga solo los nodos alcanzables desde los documentos locales.
2. Que `_cached_shard` no haga `deepcopy` por lectura.
3. `yaml.CSafeLoader` para los shards.
4. Que `live_stale` no rehashee la federación entera en cada `load_edge_index` del mismo proceso.

Aceptación esperada: `show task` en un desk nuevo cerca de 1.2 s (+50 % → ≤ 1.8 s, b1).

## p4. Aceptación

Pendiente de la tarea en sldb: la columna «con el arreglo» y los tests (`test_activation_rules` y `test_lifecycle_end_to_end` < 90 s) se miden cuando el arreglo de sldb esté integrado. No corrí la suite: sin arreglo de código no hay semántica que validar en esta rama.

## p5. main-en-verde

Cualquier timeout de CI en `test_activation_rules` o `test_lifecycle_end_to_end` y, en general, en tests que hacen `advance`, `show`, `next` o `add task` sobre un desk inicializado tiene esta causa. El CI no tiene los repos hermanos al lado, así que la federación es menor, pero el store dueño de deskops entra igual. Hay que coordinarlo con main-en-verde vía el coordinador del plan. No hay nada que arreglar dos veces en deskops.

## Apéndice: top 15 por tiempo acumulado (cProfile, `sort cumulative`)

ncalls, cumtime (s), función.

#### pre-cc32 · add-task
```
1933/1          2.553  {built-in method builtins.exec}
1               2.553  <string>:1(<module>)
1               2.553  <frozen runpy>:201(run_module)
1               2.552  <frozen runpy>:65(_run_code)
1               2.552  deskops/__main__.py:1(<module>)
1               1.585  deskops/cli/main.py:224(main)
1               1.585  deskops/cli/main.py:93(run)
1401/37         0.976  <frozen importlib._bootstrap>:1349(_find_and_load)
1363/7          0.975  <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
1343/10         0.974  <frozen importlib._bootstrap>:911(_load_unlocked)
1310/10         0.974  <frozen importlib._bootstrap_external>:989(exec_module)
2818/19         0.974  <frozen importlib._bootstrap>:480(_call_with_frames_removed)
1               0.966  deskops/cli/main.py:1(<module>)
1               0.963  deskops/cli/parser.py:1(<module>)
1               0.962  deskops/cli/registry.py:1(<module>)
```
#### pre-cc32 · show-task
```
1829/1          2.227  {built-in method builtins.exec}
1               2.227  <string>:1(<module>)
1               2.227  <frozen runpy>:201(run_module)
1               2.227  <frozen runpy>:65(_run_code)
1               2.227  deskops/__main__.py:1(<module>)
1               1.278  deskops/cli/main.py:224(main)
1               1.278  deskops/cli/main.py:93(run)
1443/79         0.957  <frozen importlib._bootstrap>:1349(_find_and_load)
1362/6          0.957  <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
1342/9          0.956  <frozen importlib._bootstrap>:911(_load_unlocked)
1309/9          0.956  <frozen importlib._bootstrap_external>:989(exec_module)
2816/17         0.956  <frozen importlib._bootstrap>:480(_call_with_frames_removed)
1               0.948  deskops/cli/main.py:1(<module>)
1               0.945  deskops/cli/parser.py:1(<module>)
1               0.944  deskops/cli/registry.py:1(<module>)
```
#### pre-cc32 · next
```
1827/1          1.895  {built-in method builtins.exec}
1               1.895  <string>:1(<module>)
1               1.895  <frozen runpy>:201(run_module)
1               1.894  <frozen runpy>:65(_run_code)
1               1.894  deskops/__main__.py:1(<module>)
1368/4          0.959  <frozen importlib._bootstrap>:1349(_find_and_load)
1360/4          0.959  <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
1340/7          0.959  <frozen importlib._bootstrap>:911(_load_unlocked)
2812/13         0.958  <frozen importlib._bootstrap>:480(_call_with_frames_removed)
1307/7          0.958  <frozen importlib._bootstrap_external>:989(exec_module)
1               0.957  deskops/cli/main.py:1(<module>)
1               0.954  deskops/cli/parser.py:1(<module>)
1               0.953  deskops/cli/registry.py:1(<module>)
1               0.937  deskops/cli/main.py:224(main)
1               0.937  deskops/cli/main.py:93(run)
```
#### pre-cc32 · advance-blocked
```
1905/1          2.723  {built-in method builtins.exec}
1               2.723  <string>:1(<module>)
1               2.723  <frozen runpy>:201(run_module)
1               2.723  <frozen runpy>:65(_run_code)
1               2.723  deskops/__main__.py:1(<module>)
1               1.784  deskops/cli/main.py:224(main)
1               1.784  deskops/cli/main.py:93(run)
1               0.977  deskops/cli/commands/operations.py:21(run)
1               0.977  deskops/operations.py:176(advance_task)
1               0.977  deskops/services/tasks.py:275(advance_task)
1471/107        0.947  <frozen importlib._bootstrap>:1349(_find_and_load)
1362/6          0.947  <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
1342/9          0.946  <frozen importlib._bootstrap>:911(_load_unlocked)
1309/9          0.945  <frozen importlib._bootstrap_external>:989(exec_module)
2816/17         0.945  <frozen importlib._bootstrap>:480(_call_with_frames_removed)
```
#### pre-cc35b · add-task
```
1933/1          2.538  {built-in method builtins.exec}
1               2.538  <string>:1(<module>)
1               2.538  <frozen runpy>:201(run_module)
1               2.537  <frozen runpy>:65(_run_code)
1               2.537  deskops/__main__.py:1(<module>)
1               1.603  deskops/cli/main.py:224(main)
1               1.603  deskops/cli/main.py:93(run)
1402/38         0.944  <frozen importlib._bootstrap>:1349(_find_and_load)
1363/7          0.944  <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
1343/10         0.943  <frozen importlib._bootstrap>:911(_load_unlocked)
1310/10         0.942  <frozen importlib._bootstrap_external>:989(exec_module)
2818/19         0.942  <frozen importlib._bootstrap>:480(_call_with_frames_removed)
1               0.934  deskops/cli/main.py:1(<module>)
1               0.931  deskops/cli/parser.py:1(<module>)
1               0.930  deskops/cli/registry.py:1(<module>)
```
#### pre-cc35b · show-task
```
1846/1         64.371  {built-in method builtins.exec}
1              64.371  <string>:1(<module>)
1              64.371  <frozen runpy>:201(run_module)
1              64.371  <frozen runpy>:65(_run_code)
1              64.371  deskops/__main__.py:1(<module>)
1              63.433  deskops/cli/main.py:224(main)
1              63.433  deskops/cli/main.py:93(run)
1              62.634  deskops/cli/commands/operations.py:22(run)
1              62.634  deskops/operations.py:173(show_task)
1              62.634  deskops/services/tasks.py:155(show_task)
1              62.509  deskops/services/tasks.py:165(_lifecycle_gates)
1              62.062  deskops/services/tasks.py:187(_transition_findings)
1              62.012  deskops/lifecycle.py:205(transition_findings)
1              62.012  sldb/api/rules/rules_on_transition.py:23(transition_findings)
3              61.358  sldb/api/edges/edge_reading.py:14(load_edge_index)
```
#### pre-cc35b · next
```
1846/1         64.497  {built-in method builtins.exec}
1              64.497  <string>:1(<module>)
1              64.497  <frozen runpy>:201(run_module)
1              64.496  <frozen runpy>:65(_run_code)
1              64.496  deskops/__main__.py:1(<module>)
1              63.572  deskops/cli/main.py:224(main)
1              63.572  deskops/cli/main.py:93(run)
1              62.777  deskops/cli/commands/operations.py:22(run)
1              62.776  deskops/operations.py:179(next_action_report)
1              62.776  deskops/services/tasks.py:214(next_action_report)
1              62.629  deskops/services/tasks.py:187(_transition_findings)
1              62.580  deskops/lifecycle.py:205(transition_findings)
1              62.579  sldb/api/rules/rules_on_transition.py:23(transition_findings)
1              61.597  sldb/api/rules/rule_graph.py:84(rule_graph)
2              61.505  sldb/api/edges/edge_reading.py:14(load_edge_index)
```
#### pre-cc35b · advance-blocked
```
1846/1         76.426  {built-in method builtins.exec}
1              76.426  <string>:1(<module>)
1              76.426  <frozen runpy>:201(run_module)
1              76.426  <frozen runpy>:65(_run_code)
1              76.426  deskops/__main__.py:1(<module>)
1              75.512  deskops/cli/main.py:224(main)
1              75.512  deskops/cli/main.py:93(run)
1              74.716  deskops/cli/commands/operations.py:22(run)
1              74.716  deskops/operations.py:176(advance_task)
1              74.716  deskops/services/tasks.py:291(advance_task)
1              74.533  deskops/lifecycle.py:254(advance)
2              74.093  sldb/api/edges/edges_holding.py:46(transition)
2              73.898  sldb/api/rules/rules_on_transition.py:23(transition_findings)
7              73.172  sldb/api/edges/edge_reading.py:14(load_edge_index)
7              72.874  sldb/store/edge_index/compose.py:24(compose_edge_index)
```
#### pre-cc35b · advance-receipts
```
1922/1         76.440  {built-in method builtins.exec}
1              76.440  <string>:1(<module>)
1              76.440  <frozen runpy>:201(run_module)
1              76.440  <frozen runpy>:65(_run_code)
1              76.440  deskops/__main__.py:1(<module>)
1              75.509  deskops/cli/main.py:224(main)
1              75.509  deskops/cli/main.py:93(run)
1              74.711  deskops/cli/commands/operations.py:22(run)
1              74.711  deskops/operations.py:176(advance_task)
1              74.711  deskops/services/tasks.py:291(advance_task)
6              72.874  sldb/api/edges/edge_reading.py:14(load_edge_index)
6              72.616  sldb/store/edge_index/compose.py:24(compose_edge_index)
2              72.510  sldb/api/rules/rule_graph.py:84(rule_graph)
19359          64.528  sldb/store/io/shards.py:31(_cached_shard)
14435          62.667  sldb/store/io/shards.py:86(load_edges_shard)
```
#### main · add-task
```
1982/1         64.359  {built-in method builtins.exec}
1              64.359  <string>:1(<module>)
1              64.359  <frozen runpy>:201(run_module)
1              64.359  <frozen runpy>:65(_run_code)
1              64.359  deskops/__main__.py:1(<module>)
1              63.424  deskops/cli/main.py:224(main)
1              63.424  deskops/cli/main.py:93(run)
1              62.620  deskops/cli/commands/operations.py:22(run)
1              62.603  deskops/operations.py:164(create_task_bundle)
1              62.603  deskops/services/tasks.py:94(create_task_bundle)
1              61.971  deskops/services/tasks.py:115(_append_task_to_board)
1              61.960  deskops/doc_access.py:389(write_doc)
1              61.828  deskops/doc_access.py:321(update_tracked_doc)
1              61.771  sldb/api/documents/transaction.py:80(update)
1              61.771  sldb/api/documents/transaction_ops.py:33(update)
```
#### main · show-task
```
1846/1         63.293  {built-in method builtins.exec}
1              63.293  <string>:1(<module>)
1              63.293  <frozen runpy>:201(run_module)
1              63.293  <frozen runpy>:65(_run_code)
1              63.293  deskops/__main__.py:1(<module>)
1              62.371  deskops/cli/main.py:224(main)
1              62.371  deskops/cli/main.py:93(run)
1              61.578  deskops/cli/commands/operations.py:22(run)
1              61.578  deskops/operations.py:173(show_task)
1              61.578  deskops/services/tasks.py:155(show_task)
1              61.378  deskops/services/tasks.py:165(_lifecycle_gates)
1              60.843  deskops/services/tasks.py:187(_transition_findings)
1              60.794  deskops/lifecycle.py:205(transition_findings)
1              60.793  sldb/api/rules/rules_on_transition.py:23(transition_findings)
3              60.182  sldb/api/edges/edge_reading.py:14(load_edge_index)
```
#### main · next
```
1846/1         64.505  {built-in method builtins.exec}
1              64.505  <string>:1(<module>)
1              64.505  <frozen runpy>:201(run_module)
1              64.505  <frozen runpy>:65(_run_code)
1              64.505  deskops/__main__.py:1(<module>)
1              63.585  deskops/cli/main.py:224(main)
1              63.585  deskops/cli/main.py:93(run)
1              62.788  deskops/cli/commands/operations.py:22(run)
1              62.788  deskops/operations.py:179(next_action_report)
1              62.788  deskops/services/tasks.py:214(next_action_report)
1              62.490  deskops/services/tasks.py:187(_transition_findings)
1              62.440  deskops/lifecycle.py:205(transition_findings)
1              62.440  sldb/api/rules/rules_on_transition.py:23(transition_findings)
1              61.442  sldb/api/rules/rule_graph.py:84(rule_graph)
2              61.349  sldb/api/edges/edge_reading.py:14(load_edge_index)
```
#### main · advance-blocked
```
1846/1         76.246  {built-in method builtins.exec}
1              76.246  <string>:1(<module>)
1              76.245  <frozen runpy>:201(run_module)
1              76.245  <frozen runpy>:65(_run_code)
1              76.245  deskops/__main__.py:1(<module>)
1              75.313  deskops/cli/main.py:224(main)
1              75.313  deskops/cli/main.py:93(run)
1              74.517  deskops/cli/commands/operations.py:22(run)
1              74.516  deskops/operations.py:176(advance_task)
1              74.516  deskops/services/tasks.py:291(advance_task)
1              74.250  deskops/lifecycle.py:254(advance)
2              73.785  sldb/api/edges/edges_holding.py:46(transition)
2              73.579  sldb/api/rules/rules_on_transition.py:23(transition_findings)
7              72.897  sldb/api/edges/edge_reading.py:14(load_edge_index)
7              72.593  sldb/store/edge_index/compose.py:24(compose_edge_index)
```
#### main · advance-receipts
```
1922/1         77.153  {built-in method builtins.exec}
1              77.153  <string>:1(<module>)
1              77.153  <frozen runpy>:201(run_module)
1              77.152  <frozen runpy>:65(_run_code)
1              77.152  deskops/__main__.py:1(<module>)
1              76.227  deskops/cli/main.py:224(main)
1              76.227  deskops/cli/main.py:93(run)
1              75.426  deskops/cli/commands/operations.py:22(run)
1              75.425  deskops/operations.py:176(advance_task)
1              75.425  deskops/services/tasks.py:291(advance_task)
6              72.992  sldb/api/edges/edge_reading.py:14(load_edge_index)
6              72.733  sldb/store/edge_index/compose.py:24(compose_edge_index)
2              72.601  sldb/api/rules/rule_graph.py:84(rule_graph)
19389          65.039  sldb/store/io/shards.py:31(_cached_shard)
14451          63.161  sldb/store/io/shards.py:86(load_edges_shard)
```
