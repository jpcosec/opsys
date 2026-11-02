**Lectura propia** (solo lectura, sin ejecutar)
**Dato del Supervisor** (no recomputado por mí): `HEAD` deskops `e9cb4e82`; sha256 de `operaciones.md` `72b840…`; sha256 de `dag.yaml` `d6b940…`; stale 38; `build --check` verde.

| Objeto | Evidencia real (archivo:línea) | Resultado |
|---|---|---|
| 1. §5.7/§5.4/§5.9/§6.3/§8.3: 409 solo donde hay precondición; sin CAS universal | `operaciones.md:344` (“El 409 solo existe donde el canal ofrece una precondición”); `:350` (canales sin `expected`: rechazo/handoff, no 409); `:328` (precondición que ofrezca el canal); `:368` (“no agrega lock ni CAS”); `:390` limita la representación a escritura de payload por campos; `:498` ack sin 409. Búsqueda de `CAS` en el contrato: sin exigencia universal | PASS |
| 2. Cadena `update_target → prepare_step → prevalidate → apply_batch → apply_change`; S01/S02/§6.2/§9.4; test de payload inválido | `save_plan.py:49-54`: `update_target` devuelve `payload_error(...), None`; `save_routes.py:61-70`: `prepare_step` solo rechaza el segundo valor; `save_routes.py:79-88`: secuencial, 500 con `completed`, sin revertir; `save_routes.py:94-107`: `update` no usa `path`; `operaciones.md:126-127,386,530` corregidos; `test_serve.py:247` es `create`; `:262` son tres `create` con doble | PASS |
| 2b. Gap de SLDB capturado en inbox antes de workaround | `../sldb/desk/inbox/20261102-011823-unclear-post-save-no-rechaza-payload-invalido-de-update-antes-de-aplicar-y-el-lote-no-es-atomico.md:20`: intake real, `status: open`, “no reproducido en runtime” | PASS |
| 3. W01/§4.2/§3.3: garantía de evidencia por canal | `operaciones.md:95`: CLI `require=True`, API `require=False`; `:222`; `:270`; código: `cli/commands/operations.py:26`, `services/tasks.py:86`, `services/closeout_gates.py:77`; tests `tests/test_operational.py:34,58,78` llaman la API sin evidencia | PASS |
| 3b. Gemela en §13.3 | `operaciones.md:754`: “W01 exige evidencia declarada”, sin distinguir CLI/API; contradice la corrección de `:95`, `:222`, `:270` | **FAIL** |
| 4. S05: `/docs` vs `/docs/create`; §7.3/§9.5/HO-15 | `docs_create_route.py:13,36`: `_KEYS = ("model","name","payload")`, `path` descartado; `docs_routes.py:28-35,62-67,105-112`: `/docs/create` sí resuelve `path`; `operaciones.md:130,449,550,690` lo separan; tests `/docs` en `test_serve_edges_docs.py:63,77` | PASS |
| 5. §4.3.1: ausencia no demuestra cierre; trailers reales; sin consulta pública; sin archivo/modelo inventado | `operaciones.md:291`; `closure.py:87` (`manual`), `:323` (`Run-Dir`), `:155-157` (`superseded`), `:239-241` (`legacy-resolved`), `:625` (`record`); búsqueda de `Task-Id`/`Closeout-Mode`/`trailers:key`/`index.jsonl` en `deskops/**/*.py`: solo `services/closure.py` y textos de ayuda; no aparece modelo/archivo histórico inventado | PASS |
| 6. W19/§6.4/§9.3/§9.6: `_close` solo verifica si `run_gates AND task_path.exists() AND routed`; sin verify universal | `closure.py:390-392`; `:540-558`; `operaciones.md:113,514,565`; W20 `closure.py:169,252,359` | PASS |
| 6b. Precisión de la nota de tests en W19 | `operaciones.md:113` afirma `[L: ningún test cubre ese caso]`; `tests/test_closeout.py:211` cierra `task-x` sin TaskDoc ni Board (`_make_repo` en `:26` solo crea `seed.txt`), es decir, ejercita el caso “sin TaskDoc / fuera del Board” | **FAIL** |

**FAIL y corrección implicada**
- `operaciones.md:754`: cambiar “W01 exige evidencia declarada” por “la CLI de W01 la exige; `create_task_bundle` no; WS26.1 debe comprobarla si usa la API”.
- `operaciones.md:113`: sustituir `[L: ningún test cubre ese caso]` por una formulación exacta: `test_closeout.py:211` cubre el cierre sin TaskDoc/Board; lo no cubierto es el caso con TaskDoc existente fuera del Board y/o una aserción explícita de que `verify` no corrió.

**Cobertura exacta**
- Leí íntegras las secciones del contrato implicadas: §3.3, §4.2, §4.3.1, §5.4, §5.7, §5.9, §6.2–§6.4, §7.3, §8.3, §9.3–§9.6, §10.1–§10.2, §12 (HO-15), §13.1/§13.3.
- Abrí las citas de código y tests: `save_plan.py`, `save_routes.py`, `docs_create_route.py`, `docs_routes.py`, `payload_save.py`, `payload_save_steps.py`, `closure.py`, `tasks.py`, `closeout_gates.py`, `cli/commands/operations.py`, `operations.py`, `persistence.py`; `tests/test_serve.py`, `tests/test_serve_edges_docs.py`, `tests/test_operational.py`, `tests/test_closeout.py`, `tests/test_mindmap_persistence.py`, y el intake de sldb.
- No revisé las 65 filas ni los bloques de los hallazgos 7–8, que corresponden al otro Tester.

**No pude verificar**
- No ejecuté tests ni reproduje runtime; todo es lectura estática.
- No recomputé hashes ni verifiqué los commits citados.
- No validé la generación de derivados del DAG, la existencia de las fichas WS46/WS47/WS48, ni el estado real de entrega del inbox (solo leí el archivo, que está `open`).

RESULTADO: FAIL
