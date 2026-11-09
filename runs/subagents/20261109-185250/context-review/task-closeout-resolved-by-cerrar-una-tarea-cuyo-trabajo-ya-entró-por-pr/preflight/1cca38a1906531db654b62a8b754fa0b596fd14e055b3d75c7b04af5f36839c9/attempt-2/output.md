## REFORMULACION

**Propósito:** añadir `deskops closeout resolved-by` para cerrar tareas cuyo trabajo ya entró por PR, sin exigir un átomo por archivo. **Resultado:** método `close_resolved_by` en `closure.py`; despacho y registro del subcomando; dos goldens de ayuda; `tests/test_closeout_resolved_by.py`; manual y CHANGELOG; commit único con `Closeout-Mode: resolved-by`, trailers de refs/tests y status `resolved`. **Repo:** deskops en `/mnt/ssd/proyectos/SLDB_1/deskops-desk-cc` (origin/main `1cc19364`). **Límites:** no tocar `verify_task_closeout`, `closeout_gates.py`, `operations.py`, `services/tasks.py` ni `close_superseded`/`close_retired`/`close_with_run`; sin átomos ni materialization; solo cambian los dos goldens indicados.

## AMBIGUEDADES

1. «deskops_closeout_resolved-by.txt o el nombre que use el arnés»: no fija el nombre del golden nuevo; obligaría a inventar o adivinar la convención del arnés.
2. «--paths y --message con la misma semántica que en supersede»: no define esa semántica; obligaría a inventar qué hacen o a depender de leer `close_superseded`, fuera de este input.
3. «sea commit ancestro de HEAD»: no dice HEAD de qué repositorio/root; obligaría a inventar el repo de referencia.
4. «test_cli desde una copia en /dev/shm»: no indica ruta ni procedimiento de copia; obligaría a inventar cómo ejecutarlo.

## DRY-RUN

Sin ejecutar nada, un ejecutor futuro leería: `closure.py` (`close_superseded` :121-200, `_close`, `_ref_resolves`), `cli/commands/closeout.py` (`_supersede` :52 y despacho :27-37), `registry.py` :1567-1595, `closeout_gates.py` solo lectura, goldens de ayuda, `test_closeout.py`, manual y CHANGELOG. Cambios previstos: `close_resolved_by`; despacho y entrada de registro; golden de closeout modificado y golden nuevo; test nuevo; docs. Dependencias: git del desk, `reference_points_to_commit`/`reference_points_to_url`/`reference_points_to_test`, `doc_access.write_doc`, `_close(run_gates=False)` e `index_entry` con mode `resolved-by`. Validaciones futuras: pytest uno a uno (`test_closeout_resolved_by`, `test_closeout`, `test_command_registry`, `test_cli_help_examples`, `test_output_goldens`, `test_cli` desde copia), `git diff` para confirmar archivos intactos y `--update-golden` limitado a los dos goldens.

## FUTURO

El coordinador puede revisar las decisiones r1-r6, marcadas «REVISABLES». CC33 reescribe el closeout y decide si resolved-by escribe recibos `evidence`. Un humano/revisor valida diff, manual y CHANGELOG; el arnés confirma el nombre definitivo del golden.
