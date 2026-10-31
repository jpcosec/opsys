# Handoff — checkpoint WS02–WS04 para revisión de Codex

> **Nota de supersesión, 2026-10-31.** Este handoff se conserva como evidencia de esa ronda; no se reescribió. La revisión independiente sustituyó varias de sus afirmaciones, entre ellas las de ViewDoc «solo modelo», `task.txt` como discrepancia, `frontends/workspace/` como requisito previo y el pedido de otra ronda con herramientas. Vale `handoff-correccion.md`, en esta misma carpeta, y WS03/WS04 no están aprobadas como insumo final hasta su revisión.

Fecha: 2026-10-31. Autor: Claude, pane `w3Y:p1`. Activación: `activation.md` en esta carpeta. Repo: `deskops`, sin push (27 commits adelante de `origin/main`, incluidos los de sesiones anteriores).

**Estado: capa WS02–WS04 cerrada por el gate oficial. No avancé a la capa siguiente: WS06, WS07 y lo demás siguen sin tocar, a la espera de esta revisión.**

## Qué cambió

| Tarea | Entregable | Commit entregable | Cierre | Tester |
|---|---|---|---|---|
| WS02 | `desk/drawer/plans/workspace-documental/auditoria/deskops.md` + anexos en el run | `eed699b2` | `0861f9b4` | PASS en ronda 2 |
| WS03 | `.../auditoria/infraestructura.md` | `09552469` | `9dd027c5` | FAIL, FAIL, PASS en ronda 3 |
| WS04 | `.../auditoria/ui.md` | `7810358d` | `ad3a21be` | FAIL, PASS en ronda 2 |

Promoción `0b336419`; TaskDocs fijadas tras revisiones `215bf624`. Runs: `runs/subagents/20261031-ws02-auditoria-deskops/`, `20261031-ws03-auditoria-infraestructura/`, `20261031-ws04-auditoria-ui/`. Cada uno contiene preflight y cold v1–v4 con recibos, `preflight-disposition.md`, `testing-handoff.md`, `validation.log` e informes de Tester por ronda.

Sin cambios en código de `deskops/`, `tests/`, `docs/`, `dag.yaml`, `reconciliacion.md` ni `decisiones.md` (`git diff --stat 2286b976..HEAD` sobre esas rutas vacío, antes del commit de este handoff). Ningún cambio en otros repos.

## Workflow aplicado

1. Creación en drawer: las fichas ya estaban versionadas. Promoción con `deskops add task`, pills ligadas, commit.
2. Preflight TaskDoc-only y cold-bundle por tarea: 24 procesos Pi deepseek-flash low, `--no-tools`, `--no-session`, stdin DEVNULL. Corregí las TaskDoc entre rondas con `deskops edit task` y resolví v4 en la disposición.
3. Executors independientes, uno por lane: subagentes Claude Sonnet. Scion no se usó.
4. Testers Pi deepseek-flash en panes Herdr `w3Y:p9`, `w3Y:pA`, `w3Y:pB`, con procesos nuevos en cada ronda.
5. Closeout por tarea con `deskops closeout commit --run-dir`: «declaró commit, document; encontré commit, document».
6. Integración de fase: `phase-closeout.md` en esta carpeta.

## Hallazgos para la capa siguiente

Contratos y huecos, con detalle y citas en cada auditoría. Todo salvo lo marcado viene de leer código.

- **No existe CAS por hash ni revisión en sldb.** La única verificación optimista es HTTP y compara el payload completo con `expected` (`save_plan.py:50,58`); la API y el CLI no verifican. `brief.md:40`, `dag.yaml` ≈1252 y `reconciliacion.md:15` hablan de hash CAS o CAS. Afecta directamente WS19 y G_SOURCE.
- **El lock de archivo cubre índices, no el Markdown** (`payload_save.py:47-48`). `SAVE_LOCK` es de proceso. Un escritor externo se pierde sin aviso. Esto confirma P03, «lock solo UI no basta».
- `sldb docs update` usa su propio camino (`doc.py`), sin journal.
- `version` = `content_hash` se entrega en algunas lecturas, no en `GET /document` ni `sldb docs show`, y `/save` no lo compara.
- pron compara `hash_c` del índice, no del archivo. Su deshacer sí detecta cambios a nivel documento, y omite la escritura (`move_undo.py:54-84`).
- **ViewDoc es solo modelo**: `spec2viz/sldb_models.py:348`, registrado, sin documentos ni evaluador, ausente en sldb y pron. `brief.md:24` lo llama «contrato existente». Afecta WS18.
- Corpus sin CLI; sin consultas guardadas.
- graph_ui: 39 filas, ninguna marcada entregada. Tiene su propia copia de la comprobación `expected`/409 en `frontends/mindmap/persistence.py:101-102`, fuera del workspace.
- **`../UIs/graph_ui/frontends/workspace/` está sin commit y sin dueño declarado**, es un servidor paralelo con proyección `changes` y su `index.html` apunta a `/app.js`, que no existe ahí. Hay que resolverlo antes de cualquier delta del workspace.
- Los dos tickets draft de graph_ui comparten `serve.py`, `views/workspace/` y `docs/workspace-ui.md`, y sus tests no existen: no pueden correr en paralelo.
- `task.txt` de `task-workspace-multiproyeccion` en graph_ui la declara activa; Board y reconciliación la dan por cerrada.
- SPEC externo desactualizado: cabecera con 44 candidatas y revisión 5; hoy 63 y revisión 8. Sus §6.1 y §6.2 ya están resueltas por el plan. Falta time slider y D0.
- deskops: `DeskopsOperations()` escribe `.deskops.log` al construirse; `validate_atoms` puede crear andamiaje; `retire` no hace commit; `closeout commit` borra el archivo de la tarea; 2 de 8 materializaciones de `store.yaml` no están en el índice local.

La detección de estas discrepancias no modifica el plan. `brief.md`, `dag.yaml` y `reconciliacion.md` quedan como estaban para que WS06 y el solicitante decidan.

## Riesgos y límites de esta evidencia

- **Testers de solo lectura.** Mi lanzamiento con `read,bash,write` fue bloqueado por el clasificador del modo auto ([Create Unsafe Agents]) y no lo rodeé. Corrieron con `read,grep,find,ls` y su salida se guardó como informe. Esto se aparta de la nota de que el Tester necesita herramientas para comprobar evidencia. Por eso los hashes, `git log`, `git status` y `--help` son datos del Supervisor (`tester-*-facts.log`), no prueba independiente, y figuran como NO VERIFICADO o «dato del Supervisor» en los informes.
- **Sin ejecución de comportamiento.** Concurrencia y mutadores se dedujeron leyendo código. La UI no se ejecutó.
- **`commands.log` no es captura en vivo.** WS02 y WS04 los reconstruyeron a mano. WS02 lo declara en su primera línea, pero el Tester aún marcó 2 líneas de prosa, 2 comandos con elipsis y scripts en `/tmp/ws02aud/` no archivados. Los resultados se re-derivan de las fuentes; el log en sí no reproduce nada.
- **`result-summary.md` de WS04 quedó desactualizado:** conserva el hash inicial `2496605c…` y el «enlace roto», ya refutado. Vale `auditoria/ui.md`; el resumen se conserva como evidencia histórica de esa ronda.
- **Residuales WS03 aceptados por la ronda 3, sin corregir:** citas imprecisas en `payload_save_steps.py:44-52`, rangos de `doc.py`, `wait=True` y una frase sobre el journal. Ninguno cambia conclusiones. Listados en `tester-result-summary.md` de ese run.
- **Residual WS04:** `ui.md:86` llama `str.split` a un `splitlines()`. Atribuciones de la lista `PS` y varios commits menores quedaron NO VERIFICADO por el Tester; el Executor las revisó con `git log`.
- **`testing-handoff.md`:** el hash congelado inicial quedó sustituido por una nota agregada al final; en WS02 y WS04 la ronda 2 lo marcó antes de esa nota.
- Errores detectados durante el trabajo: el Tester v1 de WS03 se equivocó sobre `--format` en `sldb docs update --help`, y la salida real lo aclaró. Mi búsqueda inicial de ViewDoc miró `spec2viz/src`, que no existe, y concluí mal que no aparecía; la auditoría lo corrigió.
- **Límite de las revisiones baratas:** v4 aún listó detalles. Los resolví por disposición sin una ronda v5, para evitar perseguir ruido. Esa decisión es del coordinador y está por escrito en cada `preflight-disposition.md`.
- Sesión Codex activa pudo escribir en deskops durante esta capa; todos mis commits usaron rutas explícitas.

## Validación final

Ejecutado por el Supervisor, salida en `phase-closeout.md`:

```
python desk/drawer/plans/workspace-documental/build_plan.py --check      # exit 0
python desk/drawer/plans/workspace-documental/validate_plan.py --check   # exit 0
python desk/drawer/plans/workspace-documental/context_review.py status   # all reviews current
deskops doctor --root .                                                  # healthy, 5 alertas
deskops list tasks --root .                                              # sin WS02-04 activas
```

Mi recuento propio contra fuentes: 113 comandos, 24 métodos, 17 modelos, 192 filas con 0 hashes distintos, 39 filas WS04. La suite pytest no corrió en esta capa porque no cambió código; su última corrida completa, del 2026-10-31 antes de esta capa, dio 3 fallos preexistentes, uno ya corregido.

## Qué pido revisar

1. Que cada auditoría cumple su `done_when`, abriendo filas al azar. Prioridad: secciones 2 y 3 de `infraestructura.md`.
2. Si aceptas Testers de solo lectura con datos del Supervisor, o exiges otra ronda con herramientas, lo que requeriría permiso del solicitante.
3. Si las discrepancias del plan (CAS, ViewDoc) deben ir por WS06 o reabrir contrato antes.
