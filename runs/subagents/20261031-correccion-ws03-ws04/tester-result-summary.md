# Informe del Tester — corrección WS03/WS04

Lectura de solo lectura. No ejecuté tests ni comandos; los hashes, `git log`/`git show` y el diff provienen de `tester-facts.log` y se marcan **dato del Supervisor**. Rutas de sldb/pron/spec2viz relativas a `../*/src/*`; graph_ui a `../UIs/graph_ui`.

## Comprobación por objeto

| Objeto | Evidencia real leída | Resultado |
|---|---|---|
| P1 frescura de `expected` | `../sldb/src/sldb/cli/serve/http_server.py:22` (`def build_handler`), `:23` (`get_store_context`); `save_routes.py:38` (`load_runtime_documents`), `:40-43`; `store/query.py:64-73` (`:71` `cached_store`); `store/runtime_cache.py:37-46` (`:40` hit, `:41` firma); `store/runtime_cache_signature.py:39-43` (`new_operation`), `:56-66` (`_stat`), `:69-76` (`leaf`, `:73` `trust_chain`), `:79-86` (`_leaves`), `:81-82` (sin barrido con `SLDB_TRUST_CHAIN`); `api/stores/open_store.py:40` (`new_operation`); `store_context.py:19-24` (bridge); `save_plan.py:49-50,57-58` (`payload != expected`, 409) | PASS |
| P1 ausencia de `new_operation` en `cli/serve/` | grep `new_operation\|open_store\|invalidate_runtime_cache\|get_store_context` en `cli/serve/`: solo `http_server.py:16,23` | PASS |
| P1 matiz de guardados de la API | `payload_save.py:35`, `create_document.py:43`, `untrack_document.py:45` llaman `open_store` | PASS |
| P1 dos hechos mantenidos | Texto conserva «no hay CAS por hash» y «`expected` es comparación optimista pública por valor»; `payload_save.py:16` sin estado esperado | PASS |
| P2 `+ Add relation` vs SPEC | `/home/jp/proyectos/softfactory_spec/SPEC.md:79-82` (§5.1, `:82` aristas semánticas sin archivo físico); `connect-dialog.js:9-17` (campo de referencia, «Se guardará el ID de destino en este campo»); `map-view.js:80-83` (`applyConnection` → `payload[field]`) | PASS |
| P2 no refuta al SPEC | ui.md §5: «no se refuta al SPEC con WS19.2» y ausencias «capacidad no cubierta o no comprobada» | PASS |
| P3 `task.txt` snapshot | `runs/subagents/20261031-workspace-ui/task.txt` existe con `Status: active`; `desk/tasks/` solo Board + 2 TaskDoc draft; `Board.md:35` «integrada y cerrada»; f16fcd1/134a665 = dato del Supervisor | PASS |
| P4 `ProjectionDoc` | `models/projection.py:14` (`class ProjectionDoc`), campos sin `where`; `world/projection_reader.py:22-38` (`__call__` por nombre / `all`); `world/lexicon.py:33,46` (`projection_models`), `:137-148`; `relation_words.py:27-30`, `alias_words.py:24`, `kernel/kernel.py:45` | PASS |
| P4 no equivalencia | La fila declara qué selecciona (stores, modelos, relaciones, alias, verbos), ausencia de `where` y de dirección/layout/notación; no equivale a `where` guardado ni a ViewDoc | PASS |
| P5 §5.2/§6 acotados | infra §5.2 intro acota «solo modelo, sin evaluador» al universo sldb/pron/spec2viz; §6 ítem 1 «no concluye que WS18 deba construir un evaluador… graph_ui ya es un consumidor» | PASS |
| P5 ui.md base graph_ui | `projection_views.py:48,57,85,107,113-114,127,134`; `views_routes.py:1-7,48-53,56-66,69-87`; `serve.py:147-154` (501 en `:149-150`), `:332-334`, `:382-389`; `sldb_adapter.py:384,391,398,407,427`; `tests/test_projection_views.py:18,47-166`; `tests/e2e_review_workbench_views.py:83-87,154,215,319` | PASS |
| P5 límite local 501 / tests no ejecutados | `serve.py:150` mensaje 501 remote; tests marcados «no ejecutadas: fuera de alcance» | PASS |
| P5 filas WS18/WS24 y separaciones | ui.md WS18 «solo referencia… no se afirma entregado ni aceptado»; WS24 nota ViewDoc opcional; `dag.yaml:1158-1180` (`owner_repo: spec2viz` en `:1167`), `dag.yaml:1492-1514`; modelo/evaluador/renderer/notación separados; «Ningún nodo se marca entregado» | PASS |
| P6 `/app.js` | `frontends/workspace/index.html:145` (`src="/app.js"`); `serve.py:24` (`WORKSPACE_DIR`), `:513` (`directory=…`), `:524-561` (`do_GET` solo `/api/…`), `:563-566` (fallback solo sin punto); `ls` sin `app.js` | PASS |
| P6 «sin dueño» / WS06 / no ejecutado | ui.md §4.2 define «sin reclamo en Board o TaskDoc observados»; «no es requisito previo de WS06… lo sería para adoptar… base ejecutable autorizada»; grep de `imposible\|prohibido\|crean cach\|hacerlo exigía` vacío en ambos archivos | PASS |
| Grep de afirmaciones sustituidas | «extraído del archivo»: solo `infra:3` negándolo; «sin evaluador»: solo frases acotadas (`infra:141`, `infra:3`); «cache fresca»: sin coincidencias; «estado vigente»: solo `ui:44` como negación | PASS |

## Hallazgos

- **Menores (no cambian conclusión):**
  - `infra §1` «Clave = ruta, `hash_c`, mtime y tamaño» omite que la clave real incluye `contract_hash`, nombre de store y de modelo (`runtime_cache.py:49-61` docstring).
  - `infra §4` cita `relation_words.py:27`; el filtro efectivo está en `:28-30` (línea 27 cierra el dict `allowed`).
  - `ui §3.1` cita `views_routes.py:20` para el registro del modelo; `:20` es `VIEW_MODEL_REF` y el registro está en `:48-53`.
- **Datos del Supervisor** (no verificados por mí): sha256 de ambos entregables, `git log/show` de 0eb7dd7, b9ab83c, 2a15356, f16fcd1, 134a665, y el `git diff --stat`.
- **No verificado:** hashes reales de los archivos; ejecución de tests, de la UI y de `git` (solo lectura estática disponible).

RESULTADO: PASS
