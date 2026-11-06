## REFORMULACION

Encargo ejecutable de tipo `task.code` en el repo deskops (workspace `desk`): actualizar el test obsoleto `tests/test_gitignore_policy.py` para que afirme la política vigente de `.gitignore`, en lugar de la anterior. Resultado esperado: el test renombrado `test_sldb_core_and_store_declaration_are_tracked_and_cache_is_ignored` pasa y verifica que `.sldb/store.yaml` y `.sldb/core/` no están ignorados y sí trackeados, que `.sldb_cache/` está ignorada y que nada bajo `.sldb/runtime/` está trackeado; más una línea en `CHANGELOG.md` (Unreleased/Fixed). Límites: solo esos dos archivos; no tocar `.gitignore`, `.sldb/`, `desk/` ni otros tests.

## AMBIGUEDADES

1. «una línea en Unreleased / Fixed»: no indica texto ni formato exacto; obligaría a inventar el contenido y la estructura de la sección del CHANGELOG.
2. «git diff --stat origin/main limitado a…»: asume que `origin/main` existe y es la base correcta; si no, obligaría a inventar la referencia de comparación.
3. «Aserciones con git check-ignore (no ignorados)»: no precisa si se valida código de salida 1 o salida vacía; obligaría a elegir el mecanismo concreto.

## DRY-RUN

Lecturas: `tests/test_gitignore_policy.py`, `CHANGELOG.md`, `.gitignore` (solo lectura) y consultas de estado git (`check-ignore`, `ls-files`). Cambios previstos: renombrar la función de test y su docstring; reescribir aserciones con `subprocess` y `cwd=ROOT` para las rutas indicadas; añadir la línea de CHANGELOG. Dependencias: `git`, `pytest`, checkout con la política descrita (main fe83364a), y que las rutas de `.sldb/` existan o no (irrelevante para `check-ignore`). Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_gitignore_policy.py`, `git diff --stat` acotado y comprobación de que `.gitignore` sigue intacto.

## FUTURO

El hallazgo de que `.sldb/runtime/` no está ignorado queda para decisión del dueño o de otro nodo que toque `.gitignore`; no se resuelve aquí. También corresponde al coordinador confirmar el estado de main y decidir cierre/merge tras las validaciones.
