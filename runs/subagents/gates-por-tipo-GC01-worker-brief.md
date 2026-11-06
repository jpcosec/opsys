# Encargo del worker: GC01 del plan gates-por-tipo (deskops)

Eres un worker de implementación. No ves la conversación del coordinador: todo lo que necesitas está aquí y en los archivos que se nombran. Trabajas SOLO en el worktree `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`).

## Entorno

```
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH
cd /home/robocop/proyectos/SLDB_1/deskops-wt-gates
```

Para que los tests importen el código del worktree y no el del checkout principal: `PYTHONPATH=$PWD python -m pytest -q tests/<archivo>`. El `deskops` del PATH apunta al checkout principal: dentro de los tests usa la CLI vía el código del worktree (como hacen los tests existentes), no el binario del PATH.

## Lo que tienes que leer primero (entero)

1. El TaskDoc del nodo, que es el contrato: `desk/tasks/task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo.md`. Las secciones Goal, Scope (incluidas las **Precisiones del preflight (1)-(7)**, que mandan sobre cualquier otra lectura), Implementation Path, Validation y Done When.
2. El plan: `desk/drawer/plans/gates-por-tipo/brief.md`, `alcance.md`, `decisiones.md`, y el nodo GC01 de `dag.yaml`.
3. El código que nombra el alcance: `deskops/models/task.py`, `deskops/services/closeout_gates.py`, `deskops/services/tasks.py`, `deskops/operations.py` (creación, `verify_task_closeout`, `_add_closeout_facts`), `deskops/bootstrap.py` (`MODEL_REFS`, herencia de modelos en desks), `deskops/workspace.py`, `deskops/cli/registry.py` (`add task`, `desk update`).
4. Para la herencia de modelos en sldb: `../sldb/src/sldb` (`base_models`, `where_parse.py` predicado `model <= X`, `api/model_registry/`). sldb es solo lectura para ti.

## Qué entregar

Lo que dice el TaskDoc (Goal + Scope + Precisiones) y cumplir cada línea de Done When:

- `deskops/models/task_types.py` con las siete subclases, `task_type` como `Literal` con default, `__closeout_evidence__` y `__activation_receipts__` según la tabla de la precisión (1); `TaskDoc.__contract__` (precisión 2).
- Registro en `MODEL_REFS` y herencia en desks; tipos propios de un desk en `desk/models/*.py` registrados por `desk update --apply` (DC7).
- `add task --task-type`: solo tipos registrados (error que los lista), default `task.code` con aviso en el envelope; la tarea se guarda bajo el modelo de su tipo (`TaskCodeDoc:<id>`).
- Evidencia leída del tipo; `TASK_TYPE_EVIDENCE` y `evidence_for_task_type` borrados; `--evidence` como piso; override según la precisión (6); `children`/`goldens` no verificables todavía fallan nombrando el kind (precisión 3).
- Migración en `desk update --apply` según la precisión (4), idempotente y con reporte.
- Tests nuevos en `tests/` con desks temporales reales (como los tests existentes), uno o más por cada línea de Done When; `tests/fixtures/model_contract_hashes.json` y goldens de help regenerados con el mecanismo que ya usa el repo (revisa cómo los tests los regeneran; no los edites a ojo); `CHANGELOG.md`; `docs/workflow-policy-reference.md` con la tabla de tipos.

## Reglas (no negociables)

- No tocar el repo `sldb` (ni `../sldb`, ni ningún otro checkout). Si sldb no permite algo (en especial la hipótesis: "sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve"), NO lo suples con Python que reimplemente una regla: detente en ese punto, documenta la evidencia (comando, salida) en tu informe final y sigue con lo demás.
- No escribas a mano en `desk/` ni en `.sldb/` del worktree (ni con editor, ni sed, ni Python, ni rm), y no corras `deskops` ni `sldb` contra el desk del worktree: los comandos de deskops/sldb solo en desks temporales que creen los tests. Código, tests, docs y CHANGELOG se editan normal.
- Ninguna bandera para saltar un gate (D2).
- No hagas commit, ni push, ni `git add`. El coordinador revisa y commitea.
- Solo los archivos del `files` del TaskDoc (más tests nuevos en `tests/`). Si necesitas otro, dilo en el informe y justifícalo.
- No corras la suite completa (tarda ~55 min; la corre el coordinador). Corre los tests que tocas y los vecinos: `tests/test_cli.py`, `tests/test_cli_help_examples.py`, `tests/test_output_goldens.py`, los de closeout, modelos y bootstrap/desk update que encuentres con grep.

## Informe final (en tu última respuesta y también en `runs/subagents/gates-por-tipo-GC01-worker-report.md`)

1. Archivos cambiados y creados.
2. Cada línea de Done When → test que la prueba (archivo::nombre) y si pasa.
3. Tests corridos con su resultado literal (la línea final de pytest).
4. Hipótesis verificadas o no (en particular la de la subclase de un modelo federado), con evidencia.
5. Lo que no pudiste hacer y por qué.
