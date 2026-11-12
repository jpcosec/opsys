## REFORMULACION
Encargo ejecutable (task.code, no agregado): sustituir en los tests de deskops la ruta fija al sldb hermano por un helper común que lea `SLDB_SRC`. Propósito: que los tests no carguen el checkout principal de sldb (obsoleto, 115 commits atrás) cuando se ejecutan desde un worktree. Resultado: helper único (conftest o módulo de tests, a elección del worker), los 18 archivos listados sin repetir la línea fija, y CHANGELOG (más una línea en docs si existe sección de tests). Repo: deskops, superficies `tests/` y `CHANGELOG.md`. Límites: no tocar código de deskops; quedan fuera los tests de árbol falso con carpeta sldb (`test_scion_runtime` en su prueba del workspace y `test_doctor_model_registration`); los 4 pasos del CI los corre el coordinador.

## AMBIGUEDADES
1. «test_scion_runtime en su prueba del workspace» está a la vez en los 18 y en "Fuera". Obliga a inventar si se elimina el bloque fijo de todo el archivo (afectando esa prueba) o se trata por prueba.
2. «El worker elige y lo dice en el informe». No hay artifact "informe" definido; obliga a inventar dónde y con qué formato se registra la elección.
3. «la suite completa de a un archivo» / «las dos suites completas en verde». Obliga a inventar si la validación es ejecución archivo por archivo o la suite entera de una vez.

## DRY-RUN
Lecturas: los 18 archivos de test, `conftest.py`, `pyproject.toml` (pythonpath), `CHANGELOG.md` y docs de tests. Cambios previstos: crear helper que resuelva `SLDB_SRC` (fallo rápido si la ruta no existe; fallback a hermana solo si existe), editar los 18 archivos, actualizar CHANGELOG y, condicionalmente, docs. Dependencias: clon de sldb origin/main y copia de deskops en `/dev/shm`, más la variable de entorno. Validaciones futuras: grep vacío de la línea fija fuera del helper; suite en (a) con `SLDB_SRC` y (b) sin variable con sldb hermano; fallo con ruta inexistente; CI por el coordinador.

## FUTURO
Decide el worker: conftest vs módulo, y si los archivos borran el bloque o importan el helper. Ejecuta el coordinador: los 4 pasos del CI. Queda revisable la decisión del overlord (2026-11-11) y el mensaje de fallo rápido.
