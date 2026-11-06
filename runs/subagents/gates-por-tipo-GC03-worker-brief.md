# Encargo del worker: GC03 del plan gates-por-tipo (deskops)

Eres un worker de implementación. No ves la conversación del coordinador; todo lo que necesitas está aquí y en los archivos nombrados. Trabajas SOLO en el worktree `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`). Ese worktree ya contiene:
- GC01: tipos de tarea como modelos (`deskops/models/task_types.py`).
- GC02: ReviewDoc (`deskops/models/review.py`; `edit review` rechaza el veredicto).
- GC06: sin `advance --to`; `edit task` rechaza los campos del ciclo de vida.

## Entorno
```
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH
cd /home/robocop/proyectos/SLDB_1/deskops-wt-gates
PYTHONPATH=$PWD python -m pytest -q tests/<archivo>
```
El `deskops` del PATH es el checkout principal, no este worktree. En los tests, usa el código del worktree como hacen los tests existentes (`deskops.cli.main.main([...])` o `python -m deskops` con PYTHONPATH).

## Lee primero (entero)
1. El TaskDoc es el contrato. Está en el checkout principal: `/home/robocop/proyectos/SLDB_1/deskops/desk/tasks/task-gc03-comando-deskops-review-que-reemplaza-a-los-dos-scripts-de-revisión-en-frío.md`. Lee Goal, Scope (las **Precisiones del preflight (1)-(13)** al final del Scope MANDAN sobre el resto), Validation y Done When.
2. El script de referencia, que vas a reemplazar con un comando: `desk/drawer/plans/gates-por-tipo/context_review.py`. Es copia del script gobernado de sldb; toma de él SYSTEM, ARGV, KEEP, `neighbours()`, `Bundle`, `attempt_dir()` y `review()`. El script viejo `desk/drawer/plans/workspace-documental/context_review.py` sirve solo de contexto.
3. El ritual: `desk/rituals/context-review.md`, pasos 3, 5 y 8.
4. El plan: `desk/drawer/plans/gates-por-tipo/decisiones.md` (D2, D4, D9) y el nodo GC03 de `dag.yaml`.
5. El código existente:
   - `deskops/models/review.py` (ReviewDoc de GC02) y `deskops/models/runtime_profile.py`.
   - `deskops/models/board.py`; el Board es `desk/tasks/Board.md`.
   - `deskops/workspace.py` (init y desk update: cómo se siembran los perfiles `desk/runtimes/runtime-pi.md` y `runtime-claude.md`).
   - `deskops/cli/registry.py` (cómo se declara un comando, con help, epílogo y handler) y un handler parecido en `deskops/cli/commands/`.
   - `tests/test_context_review_helper.py`: lo vas a borrar, pero mira qué cubría.

## Qué entregar
- Comando `deskops review` con `node`, `preflight`, `bundle`, `status` y `dispose`, exactamente como dicen Goal y precisiones.
  - Servicio: `deskops/services/review.py`. Handler: `deskops/cli/commands/review.py`. Registro en `deskops/cli/registry.py`.
  - Salida con el envelope `--format text|json|yaml` como los demás comandos.
  - Opciones: `--engine`, `--max-attempts`, `--force`, `--reason`, `--timeout`, `--run`, `--root`.
- Evidencia por corrida en `runs/subagents/<run>/context-review/<clave>/<sha>/attempt-N/` con estos cinco archivos:
  - `input.md`: un `FILE:<ruta>` por fuente, en el orden documentado.
  - `manifest.json`: argv, modelo, perfil, selection_reason, fuentes con sha256, omitted_sources, y retry reason si hubo `--force`.
  - `output.md`.
  - `stderr.log`.
  - `receipt.json`: technical_ok, returncode, input_sha256, output_sha256, start y end.
- Un ReviewDoc por corrida, escrito con doc_io, con la ruta y el id de la precisión (10).
  - Una falla de transporte (exit distinto de 0, timeout o salida sin `REFORMULACION`) deja `technical_ok: false` en el recibo y el ReviewDoc con verdict `incomplete` y reason `technical`.
- `dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto>`:
  - Escribe verdict, reason, disposed_at y disposed_by (usa la identidad que deskops ya resuelve para el remitente o el operador).
  - Falla con exit 1 si el ReviewDoc no está en `pending`.
- `kind: node` en ReviewDoc (precisión 10) y `system_prompt` opcional en RuntimeProfileDoc (precisión 6). Actualiza los hashes de contrato con el mecanismo del repo (mira `tests/test_model_contract_snapshot.py`, que dice cómo se regenera).
- Perfil `runtime-pi-deepseek-flash`, sembrado por init y por `desk update --apply`. Debe ser idempotente y no pisar un perfil existente. Pruébalo en un desk temporal.
- Borra `tests/test_context_review_helper.py`. Sus casos útiles pasan a los tests nuevos.
- Tests nuevos (p. ej. `tests/test_review_command.py`), uno o más por cada línea de Done When.
  - Usa un ejecutable `pi` falso como fixture: un script en un directorio temporal puesto primero en PATH. Debe poder devolver una salida con REFORMULACION, salir con exit 1 o contar sus llamadas.
  - El test de node copia `desk/drawer/plans/gates-por-tipo/` a un desk temporal.
  - Ningún test llama al pi real ni usa la red.
- Help con epílogo y ejemplos. Regenera los goldens con `pytest tests/test_output_goldens.py::test_help_goldens --update-golden`, nunca a ojo. Ajusta `tests/test_command_registry.py` y `tests/test_cli_help_examples.py` si hace falta.
- Una entrada en `CHANGELOG.md` y una sección `deskops review` en `docs/operator-manual.md`.

## Reglas (no negociables)
- No toques el repo sldb.
- No escribas en `desk/` ni en `.sldb/` del worktree, ni a mano ni con deskops. Todo lo que tu comando escribe se prueba en desks temporales.
- No borres los scripts de `desk/drawer/plans/`: el retiro del de workspace-documental lo hace el coordinador con el CLI, y el de gates-por-tipo sigue en uso.
- No mandes la nota a sldb: la manda el coordinador.
- Ninguna bandera salta un gate (D2). `--force` solo repite una revisión con una razón registrada; no salta nada del ciclo de vida.
- Nada de Python que supla una regla que sldb debería evaluar. Si necesitas una regla que sldb no da, regístrala como hipótesis en el informe.
- No hagas commit, push ni git add.
- Toca solo los archivos de `files` del TaskDoc. Justifica cualquier otro en el informe.
- No corras la suite completa (tarda ~1 h; la corre el coordinador). Corre tus tests nuevos y estos vecinos:
  - `tests/test_review_doc.py`, `tests/test_model_contract_snapshot.py`, `tests/test_command_registry.py`, `tests/test_cli_help_examples.py`, `tests/test_output_goldens.py`, `tests/test_operator_manual.py`, `tests/test_packaging.py`.
  - Los tests de init y desk update que encuentres con grep de `runtime-pi` o `desk/runtimes`.
  - `tests/test_cli.py`.
  - Si una corrida agrupada pasa de 25 min, divídela.
- Hay un fallo previo en main que no es tuyo: `tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`. Cualquier otro fallo es tuyo hasta que pruebes lo contrario corriéndolo en `/home/robocop/proyectos/SLDB_1/deskops` (main).

## Informe final
Va en tu respuesta y en `runs/subagents/gates-por-tipo-GC03-worker-report.md`:
1. Archivos cambiados, creados y borrados.
2. Cada línea de Done When → el test que la cubre (`archivo::nombre`) y si pasa.
3. La última línea de pytest de cada corrida.
4. Hipótesis registradas, por ejemplo el hash de contrato igual al sha del input mientras no exista GO02.
5. Lo que no hiciste y por qué.
