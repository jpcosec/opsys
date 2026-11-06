# Encargo del worker: GC02 del plan gates-por-tipo (deskops)

Eres un worker de implementación. No ves la conversación del coordinador: todo lo que necesitas está aquí y en los archivos nombrados. Trabajas SOLO en el worktree `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`), que ya contiene GC01 (tipos de tarea: `deskops/models/task_types.py`, `TaskCodeDoc`, etc.).

## Entorno
```
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH
cd /home/robocop/proyectos/SLDB_1/deskops-wt-gates
PYTHONPATH=$PWD python -m pytest -q tests/<archivo>
```
El `deskops` del PATH es el checkout principal: en los tests usa el código del worktree (`python -m deskops` con PYTHONPATH, como hacen los tests existentes, p. ej. tests/test_task_types.py).

## Lee primero (entero)
1. El TaskDoc (contrato), en el checkout principal porque es más nuevo que el del worktree: `/home/robocop/proyectos/SLDB_1/deskops/desk/tasks/task-gc02-reviewdoc-como-recibo-anclado-al-contrato-de-la-tarea.md`. Goal, Scope con las **Precisiones del preflight (1)-(6)** (mandan sobre cualquier otra lectura), Implementation Path, Validation, Done When.
2. Plan: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates/desk/drawer/plans/gates-por-tipo/brief.md` (§Vocabulario: Recibo), `decisiones.md` (DC3), nodo GC02 de `dag.yaml`.
3. Patrón: `deskops/models/run.py` (RunDoc), `deskops/models/__init__.py`, `deskops/bootstrap.py` (MODEL_REFS), `deskops/workspace.py` (directorios del desk), `deskops/operations.py` (ARTIFACT_SUBJECTS, edit_artifact_field), `deskops/cli/registry.py`, `deskops/identity.py`, `deskops/doc_io.py`.
4. Cómo GC01 registró sus modelos en el store dueño: `git show d0e7bb05 --stat` y su informe `runs/subagents/gates-por-tipo-GC01-worker-report.md` §5.1 (`python -m sldb models add "deskops.models:<Cls>" --store .sldb --pythonpath .`, necesario para que los desks nuevos hereden el modelo).

## Qué entregar
Lo que dice el TaskDoc y cada línea de Done When, con un test por línea (desks temporales reales). En particular: ReviewDoc con __doc_anchors__ = ["subject"] y SIN subject en __references__ (precisión 1); el test de `sldb edges show` marcado `pytest.mark.xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07")`; sujeto `review` para `deskops edit review` que rechaza verdict/reason/disposed_at/disposed_by (precisión 3); `desk/reviews/` creado por init y desk update; fixture de hashes y goldens de help regenerados con el mecanismo del repo (`--update-golden` u otro que encuentres; nunca a ojo); CHANGELOG.

## Reglas (no negociables)
- No tocar el repo sldb ni ningún checkout suyo. Nada de Python que supla una regla o arista que sldb debería dar.
- No escribir a mano en `desk/` ni `.sldb/` del worktree; no correr deskops contra el desk del worktree. La única excepción es registrar el modelo en el store dueño con `python -m sldb models add ... --store .sldb --pythonpath .` (CLI), como hizo GC01.
- Ninguna bandera para saltar un gate.
- No commit, no push, no git add.
- Solo los archivos de `files` del TaskDoc (más tests nuevos). Si necesitas otro, justifícalo en el informe.
- No corras la suite completa. Corre tus tests y los vecinos: tests/test_task_types.py, tests/test_model_contract_snapshot.py, tests/test_federated_models.py, tests/test_cli.py, tests/test_cli_help_examples.py, tests/test_output_goldens.py, y los de edit y desk update que encuentres con grep.
- Un test que ya fallaba en main antes de GC01: tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions. Cualquier otro fallo es tuyo hasta que pruebes lo contrario corriéndolo en `/home/robocop/proyectos/SLDB_1/deskops` (main).

## Informe final (en tu respuesta y en runs/subagents/gates-por-tipo-GC02-worker-report.md)
1. Archivos cambiados/creados. 2. Cada línea de Done When → test (archivo::nombre) y si pasa. 3. Línea final de pytest de cada corrida. 4. Hipótesis y evidencia. 5. Lo que no hiciste y por qué.
