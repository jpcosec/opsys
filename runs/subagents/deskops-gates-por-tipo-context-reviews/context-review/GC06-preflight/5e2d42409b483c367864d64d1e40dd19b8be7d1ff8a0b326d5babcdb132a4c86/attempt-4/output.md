## REFORMULACION
Encargo del nodo GC06 (TaskDoc, tipo code): cerrar en el repo **deskops** las vías de escape del ciclo de vida. Resultado esperado: retirar la opción `--to` de `deskops advance` (registry y `tasks.py:179-192`), de modo que su uso falle con error de uso (exit 2) y el help no la mencione; y hacer que `edit task` rechace `status`, `current_node`, `task_type`, `closeout_evidence` e `history` con exit 1 y un mensaje que nombre quién escribe cada campo, dejando el resto editable. Incluye actualizar golden de help, `docs/operator-manual.md`, entrada breaking en `CHANGELOG.md`, ack del inbox 20261029-213633 y suite `pytest tests` verde en robocop2. Límites: no tocar sldb; nada escrito a mano en `desk/` ni `.sldb/`; worktree `deskops-wt-gates`, rama `wt/gates-por-tipo`, nunca push a main ni `git add -A`; fuera de alcance los demás nodos GC y brief §Fuera de alcance.

## AMBIGUEDADES
1. «un error que dice quién escribe cada campo (advance y closeout; add task para task_type)»: no fija el mapeo campo→escritor (¿status/current_node/history por advance?, ¿closeout_evidence por closeout?) ni el texto; obligaría a inventar ambos.
2. «blocked → nada que escribir»: no aclara si `advance` conserva algún camino para blocked ni con qué mensaje; obligaría a inventar comportamiento.
3. «el resto de campos sigue editable»: no enumera ese resto; obligaría a inventar el conjunto permitido.
4. «se cierra con ack»: no indica comando ni formato del ack; obligaría a inventar el procedimiento.
5. «cerrar → closeout commit; superseded → closeout supersede»: no dice si esos subcomandos ya existen o deben crearse; obligaría a inventar alcance.
6. «con task_activates aún sin condición (hasta GC05)»: presupone semántica de `task_activates` y GC05, ausentes del input.

## DRY-RUN
Un ejecutor futuro leería `deskops/cli/registry.py`, `deskops/services/tasks.py`, `deskops/operations.py` (`edit_artifact_field`), `deskops/cli/commands/operations.py`, `tests/`, `tests/fixtures/golden/help/`, `docs/operator-manual.md`, el inbox y `CHANGELOG.md`. Cambios previstos: quitar `--to` del parser/registry y su rama en tasks; añadir guardas de los cinco campos con exit 1; actualizar golden, doc, CHANGELOG y ack. Dependencias: GC01, entorno robocop2, worktree/rama indicados. Validaciones futuras: los comandos de §Validation y `PYTHONPATH=$PWD python -m pytest -q tests`.

## FUTURO
GC01 aporta el contrato de tipos; GC05 habilitará la condición de `task_activates`; un humano decide mapeo campo→escritor y textos si no quedan fijados, aprueba el ack del inbox y acepta la entrada breaking; si sldb no fija una regla necesaria, se registra hipótesis y, si bloquea, se manda nota a sldb sin tocar ese repo.
