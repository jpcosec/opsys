# Handoff de corrección — WS03/WS04, para revisión root

Fecha: 2026-10-31. Autor: Claude, pane `w3Y:p1`. Delta documental sobre `handoff.md`, que se conserva con nota de supersesión. Sin push.

**Estado: tarea de corrección cerrada por el gate. WS06 sigue en pausa hasta tu revisión.** WS02 no se tocó; quedó aceptado por ti, con `commands.log` como bitácora orientativa.

## Commits

| Commit | Qué |
|---|---|
| `e06d304b` | Ficha en drawer, creada con inbox → promote |
| `52920aae` | Activación de la tarea |
| `0850f0d0`, `ba480a6c` | Alcance ampliado a ViewDoc y fijado en seis puntos |
| `32ef48d1` | Corrección de `infraestructura.md`, `ui.md` y nota en `handoff.md` |
| `542bf364` | Closeout: «declaró commit, document; encontré commit, document» |

Cierres previos intactos: `0861f9b4`, `9dd027c5`, `ad3a21be`, `d493ec26`. Sin reset ni amend. Sin cambios en código, `dag.yaml`, `reconciliacion.md` ni repos hermanos (`git diff --name-only 2286b976..HEAD -- deskops tests docs dag.yaml reconciliacion.md`: 0 archivos).

Entregables: `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` sha256 `1e1fda815bf56e91f7e47aa13d11d90fc84f7b1f2d44458597add63e44e0d662`; `.../ui.md` sha256 `b3272dc9586d88975bae7f92f4ed392411b83c0ca7b2932b382a287ce3c477a6`.

Run: `runs/subagents/20261031-correccion-ws03-ws04/`. `review-source.md` guarda tus mensajes; `result-summary.md` tiene antes y después por punto, con citas; `tester-result-summary.md` el veredicto.

## Afirmaciones sustituidas

| # | Decía | Dice ahora | Evidencia estática |
|---|---|---|---|
| 1 | `expected` se compara con el «payload actual extraído del archivo» | Payload obtenido por carga runtime sujeta a cache. Una edición externa que no altere índices puede preceder a `/save` y no verse en `expected`. Deducción estática, no reproducida. Sigue sin haber CAS por hash, y `expected` sigue siendo comparación optimista pública por valor | `sldb/cli/serve/http_server.py:22-26`; `save_routes.py:38-40`; `store/query.py:64-73`; `store/runtime_cache.py:37-46`; `store/runtime_cache_signature.py:39-43,56-66,73-76,79-86`; `save_plan.py:49-51,57-59` |
| 2 | `+ Add relation` del SPEC quedaba refutado por WS19.2 | Capacidad no cubierta o no comprobada como arista autónoma; WS19.2 edita campos de referencia, sin puente demostrado | `softfactory_spec/SPEC.md:79-82`; `frontends/mindmap/views/documents/map/connect-dialog.js:9-17` |
| 3 | `task.txt` activa era discrepancia de estado | Snapshot histórico, sin contradicción actual | `git show --stat f16fcd1`, `134a665` en graph_ui |
| 4 | Consultas guardadas: ausente por grep | Se mantiene sin where guardado, delimitado frente a `ProjectionDoc` de pron, persistido y evaluado, que no equivale a where guardado ni a ViewDoc | `pron/models/projection.py:14`; `world/projection_reader.py:22`; `world/lexicon.py:137` |
| 5 | ViewDoc «solo modelo, sin evaluador» y WS18 debía construirlo | Vale solo en el universo sldb/pron/spec2viz. graph_ui ya tiene evaluador y rutas, local-only con 501 en remote, y pruebas existentes no ejecutadas. `ui.md` §3.1 agrega la base y filas WS18 y WS24. Modelo, evaluador, renderer y notación quedan separados. No anuncia aceptación ampliada | `frontends/mindmap/projection_views.py:107`; `views_routes.py:1-7,69-87`; `serve.py:147-155`; commits `0eb7dd7`, `b9ab83c`, `2a15356` |
| 6 | «Sin dueño» sin definir, y textos de «no se pudo probar» | Sin reclamo en Board o TaskDoc observados. Falta de `/app.js` respaldada por su `serve.py`. Es requisito de adoptarlo como base ejecutable, no de WS06. Lo no probado dice «no ejecutado: fuera de alcance», con test futuro en sandbox propio | `frontends/workspace/serve.py`, `index.html:173`; filas de no comprobado en ambas auditorías |

Además, de mi propio `handoff.md` quedan sustituidos:

- «ViewDoc es solo modelo» como conclusión global.
- «Hay que resolverlo antes de cualquier delta» sobre `frontends/workspace/`.
- «`task.txt`... declara activa» como discrepancia.
- El pedido de una ronda con herramientas: ya resolviste que la lectura independiente basta y no hace falta permiso nuevo.
- El reporte de «enlace roto» del SPEC se corrigió en la ronda 2 de WS04; `result-summary.md` de esa ronda lo conserva como historia.

Matiz que la fuente aportó al punto 1, y que no estaba en tu revisión: las escrituras de la API llaman `open_store` (`api/documents/payload_save.py:35`, `create_document.py:43`, `untrack_document.py:45`), que llega a `new_operation`. Por eso el barrido se repite tras un guardado propio. No hay llamada en `cli/serve/`. No cambia tu hallazgo sobre ediciones externas previas.

## Verificación

- Revisiones baratas: preflight y cold v1–v3 en procesos nuevos. Hubo tres rondas porque el alcance creció dos veces; resoluciones en `preflight-disposition.md`.
- Executor nuevo, independiente: Claude Sonnet.
- Tester nuevo: Pi deepseek-flash, `read,grep,find,ls`, pane `w3Y:pC`. RESULTADO: PASS. Un primer lanzamiento falló por archivo de entrada faltante, error mío, y no produjo veredicto.
- Mi comprobación: leí el límite 501 en `serve.py:147-155`, `evaluate_view` en `projection_views.py:107` y las llamadas de `new_operation`; ningún `grep` encuentra «extraído del archivo», «cache fresca» ni «imposible» en los dos archivos.
- `build_plan.py --check`, `validate_plan.py --check`: exit 0. `context_review.py status`: «all reviews current», que acredita hashes y no que la nueva evidencia no los contradiga.

## Residuales aceptados, sin corregir

Tres citas menores del Tester, que no cambian conclusiones:

- `infraestructura.md` §1: «Clave = ruta, `hash_c`, mtime y tamaño» omite `contract_hash` y nombres de store y modelo (`runtime_cache.py:49-61`).
- `infraestructura.md` §4: `relation_words.py:27`, cuando el filtro está en `:28-30`.
- `ui.md` §3.1: `views_routes.py:20` por registro del modelo, que está en `:48-53`.

Sigue vigente de `handoff.md`: citas imprecisas de WS03 y `ui.md` «str.split» por `splitlines()`.

Hashes y salidas de `git` del Tester son datos del Supervisor; nada se ejecutó: ni tests, ni servidores, ni UI.

## Entrada para WS06, sin empezar

- No construir evaluador ViewDoc ni CAS de cero por el resumen anterior: primero mapear reutilización, límites, actor y contratos.
- `brief.md`, `dag.yaml` y `reconciliacion.md` siguen sin cambios y contienen las discrepancias de §6 de `infraestructura.md`. Los inputs afectados necesitan re-review barato.
