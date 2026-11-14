# Informe: deskops view board en menos de 2,5 s

## RESULTADO
Hecho, con una reserva sobre la meta en frío. En caliente (store construido, caché de composición de H11 escrita) la mediana de `deskops view board` baja de 3,78 s a 2,39 s (meta: 2,5 s o menos; alcanzada). Salida de `view board` y `view task` idéntica a la de antes. Llamadas a `open_store`: de 37 a 12 (meta: 15 o menos). En frío (sin caché de disco) `view board` falla igual antes y después con "Unknown view (H12)": no hay trabajo que medir; el cambio no lo empeora.

Qué cambia: el desk se lee una vez por corrida y se comparte entre tarjetas en el `ReadSnapshot` existente (sin estado global): registro de cada tarea (ruta, payload, payload con campos heredados; también cachea los padres heredados), `Model:name` de cada tarea (ya sin abrir el store por tarjeta: usa `doc_access.index_entry`), el rule graph de transiciones (`rule_graph(store, None)`, el mismo que construye sldb) y el contexto de closeout. `desk_graph` no recorre `runs/` (decenas de miles de archivos que ninguna superficie lee) salvo que una materialización declare un `target_identity` allí; en ese caso usa la configuración completa.

## COMMITS (rama wt/view-board, sin push)
- 0e212b4b0 view board lee una vez por corrida lo que antes rehacía por tarjeta (agente anterior)
- 2d2922e0 evidencia de view board: mediciones, conteo de llamadas del perfil y hashes de salida (sin los .prof)
- el commit de este informe y de suite.txt (el último de la rama)

Los `.prof` (baseline.prof, after.prof, ~870 KB cada uno) NO se versionan: el repo no versiona ningún `*.prof` (`git ls-files '*.prof'` vacío) y .gitignore no los menciona. Siguen en runs/subagents/boardperf/ sin trackear; el conteo de llamadas que extraen está en profile_counts.txt (generado por profile_counts.py).

## TESTS
Comando de cada archivo: `flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm timeout 900 systemd-run --user --scope -q -p MemoryMax=2G -- .venv/bin/python -m pytest -q -p no:cacheprovider <archivo>`, de a uno. Suite completa: 100 archivos, una línea por archivo en runs/subagents/boardperf/suite.txt.
- Archivos tocados: tests/test_view.py (16 puntos, sin fallos), tests/test_desk_graph_runs_target.py (2 passed), tests/test_view_goldens.py (1 passed; los goldens de tests/fixtures/golden/output/ no cambiaron).
- Fallos en la suite, todos descartados como causados por el cambio:
  - test_ci_integration.py (2): `python: command not found`; la suite corrió sin `.venv/bin` en PATH. Con PATH correcto: 2 passed.
  - test_cli.py::test_doctor_reports_invalid_documents (1): falla igual en main 9b3bb95a con el mismo sldb-runtime (espera "SLDB store check crashed...").
  - test_domain_tree.py (2): los 2 fallos preexistentes en main indicados por el coordinador.
  - test_legacy_task_states.py (3) y test_task_lifecycle_validator.py (1): los mismos fallos en main 9b3bb95a (esperan "Store check failed ('sldb stores check' exit code 1"); dependen de la versión de sldb-runtime.
- Cubiertos por tests: `_gates` convierte una falla de transiciones en el error de la tarjeta (`test_a_gate_read_failure_is_the_card_error`) y `_closeout` registra "verify_task_closeout failed" (`test_a_closeout_read_failure_is_the_card_error`); ambos en tests/test_view.py.
- No corrí ci-knowledge-check ni `graph missing`: no se pedían a este ejecutor y los pasos del CI son del coordinador.

## MEDICIONES
Layout (benchmark de H11, worktrees del contenedor): deskops 0e212b4b0 (baseline 9b3bb95aa), sldb 81f04add7b1d, spec2viz 22cd8137, pron 7f2e3085, scion 3993a6fa, sldb-h11c 1e3d346e. Carga de la máquina alta (load avg ~6-7) en ambas series.

| estado | baseline (mediana) | after (mediana) |
|---|---|---|
| caliente | 3,78 s (5 corridas: 3,71-3,93) | 2,39 s (7 corridas: 2,36-2,50) |
| frío | 2,41 s (falla: Unknown view H12) | 2,38 s (falla: Unknown view H12) |

Perfil (cProfile; profile_counts.txt), llamadas por corrida, baseline -> after:
- open_store: 37 -> 12 (1,18 s -> 0,42 s acumulado)
- desk_graph: 1 -> 1 (1,70 s -> 1,40 s)
- build_closeout_graph_context: 5 -> 5 (3,52 s -> 2,93 s acumulado; las 5 llamadas comparten el grafo del snapshot, la cifra incluye construir el grafo la primera vez)
- load_edge_index: 5 -> 4; select_documents: 24 -> 4; transition_findings: 4 llamadas (1,04 s -> 0,39 s); doc_status: 4 -> 0

Salida idéntica (output-hashes.txt, mismo desk y store, código 9b3bb95a vs 0e212b4b): board.json, task.json, board.txt y task.txt con el mismo sha256; diff vacío. Además tests/test_view_goldens.py (goldens de CC34, capturados antes de este cambio, tres columnas/nodos, sin modificarlos) pasa.

## HALLAZGOS
- Hipótesis para sldb: en frío `deskops view board` falla con "Unknown view (H12)" tanto antes como después del cambio. Parece que sin caché de composición la vista no se resuelve; conviene revisar en sldb si la caché es necesaria para registrar la vista (H12) o si el fallo es del arranque en frío. Esto bloquea medir frío.
- Hipótesis para sldb: `open_store` hace `migrate_store_layout` y `_already_canonical` en cada llamada (~1,3 s en el perfil original por 31 llamadas); memoizarlo por proceso sería ganancia directa. No se toca aquí.
- Restante del tiempo en caliente (2,39 s): construir el grafo del desk una vez (~1,4 s) y el índice de aristas; es trabajo de ProjectGraph/sldb.
- Pendiente de decisión del coordinador: omitir `runs/` en `desk_graph` es un cambio de comportamiento acotado (con test) que va más allá de compartir estado; no altera la respuesta del grafo porque ninguna superficie lee `runs/`.
- Los fallos preexistentes de la lista de TESTS dependen de sldb-runtime actual en main.

## DUDAS
- ¿Se acepta la exclusión de `runs/` en `desk_graph` (arriba)? Si no, la medición sube.
- Los `.prof` quedan sin versionar; si se quieren en el repo hay que decidirlo (870 KB cada uno).
- build_closeout_graph_context sigue con 5 llamadas por corrida (una por tarjeta con closeout): el contexto se comparte pero la función se invoca por tarjeta; se reutiliza el resultado desde el snapshot.
